"""Linha de comando.

    agio coletar --inicio 2026-01-01           # baixa tudo até hoje
    agio coletar --inicio 2026-01-01 --fim 2026-10-30
    agio calcular                              # gera o ágio a partir do tratado
    agio grafico                               # salva dados/grafico_agio.png
    agio coletar-horario --inicio 2020-10-01   # candles horários -> preço na janela da PTAX
    agio importar-trends                       # lê os CSVs de dados/manual/google_trends
    agio coletar-controles                     # juro real (Tesouro Direto) e VIX (FRED/Cboe)
    agio coletar-controles --so-vix            # só o VIX
    agio testar                                # regressão e estudo de evento -> dados/resultados
    agio robustez                              # mesma regressão em especificações alternativas
    agio relatorio                             # gráficos e tabelas -> docs/figuras, docs/resultados_tabelas.md
    agio testar --inicio 2026-11-02            # validação fora da amostra (docs/pre-registro.md)
    agio episodio --inicio 2026-06-01 --fim 2026-08-15   # diagnóstico de um episódio
    agio oferta-usdt                           # exploratório: oferta global de USDT (DefiLlama)
"""

from __future__ import annotations

import argparse
import json
from datetime import date

import pandas as pd

from agio import armazenamento as arm
from agio.comportamento import painel_diario, sinais_mercado
from agio.fontes import bcb, binance, defillama, fred, google_trends, mercadobitcoin, tesouro
from agio.indicador import calcular_agio, consolidar
from agio.janela import preco_janela_ptax

PASTA_TRENDS = arm.RAIZ / "manual" / "google_trends"
ARQUIVO_EVENTOS = arm.RAIZ / "manual" / "eventos.csv"
PASTA_RESULTADOS = arm.RAIZ / "resultados"

CORRETORAS = {
    "binance": (binance, "USDTBRL"),
    "mercadobitcoin": (mercadobitcoin, "USDT-BRL"),
}

# Como pedir candles horários a cada corretora.
HORARIO = {
    "binance": {"intervalo": "1h"},
    "mercadobitcoin": {"resolucao": "1h"},
}


def coletar(inicio: date, fim: date) -> None:
    rotulo = f"{inicio:%Y%m%d}-{fim:%Y%m%d}"

    bruto = bcb.baixar_ptax(inicio, fim)
    arm.salvar_bruto("bcb_ptax", bruto, rotulo)
    ptax = arm.atualizar_tratado("ptax", bcb.tratar_ptax(bruto), ["data"])
    print(f"PTAX: {len(ptax)} dias na base")

    bruto = bcb.baixar_sgs(bcb.SELIC_DIARIA, inicio, fim)
    arm.salvar_bruto("bcb_selic", bruto, rotulo)
    selic = arm.atualizar_tratado("selic", bcb.tratar_sgs(bruto, "selic_dia_pct"), ["data"])
    print(f"Selic: {len(selic)} dias na base")

    lotes = []
    for nome, (modulo, simbolo) in CORRETORAS.items():
        try:
            bruto = modulo.baixar(simbolo, inicio, fim)
        except RuntimeError as erro:
            print(f"{nome}: falhou ({erro}); seguindo com as demais")
            continue
        arm.salvar_bruto(nome, bruto, rotulo)
        df = modulo.tratar(bruto, nome)
        print(f"{nome}: {len(df)} candles no período")
        lotes.append(df)
    if lotes:
        precos = arm.atualizar_tratado("precos_usdt_brl", pd.concat(lotes), ["data", "fonte"])
        print(f"Preços: {len(precos)} linhas na base")


def coletar_horario(inicio: date, fim: date) -> None:
    """Candles horários de cada corretora, resumidos no preço da janela da PTAX."""
    rotulo = f"{inicio:%Y%m%d}-{fim:%Y%m%d}"
    lotes = []
    for nome, (modulo, simbolo) in CORRETORAS.items():
        try:
            bruto = modulo.baixar(simbolo, inicio, fim, **HORARIO[nome])
        except RuntimeError as erro:
            print(f"{nome}: falhou ({erro}); seguindo com as demais")
            continue
        arm.salvar_bruto(f"{nome}_1h", bruto, rotulo)
        horas = modulo.tratar_horario(bruto, nome)
        janela = preco_janela_ptax(horas)
        print(f"{nome}: {len(horas)} candles horários, {len(janela)} dias com janela da PTAX")
        lotes.append(janela)
    if lotes:
        base = arm.atualizar_tratado("precos_janela_ptax", pd.concat(lotes), ["data", "fonte"])
        print(f"Preços na janela da PTAX: {len(base)} linhas na base")


def coletar_controles(juro: bool = True, vix: bool = True) -> None:
    """Juro real de 10 anos (Tesouro Direto) e VIX (FRED ou Cboe), histórico completo."""
    hoje = f"{date.today():%Y%m%d}"
    if juro:
        print("Baixando o histórico do Tesouro Direto (cerca de 14 MB)...")
        texto = tesouro.baixar()
        arm.salvar_bruto_texto("tesouro_direto", texto, hoje)
        tabela = tesouro.juro_real_10a(tesouro.tratar(texto))
        tabela.to_csv(arm.TRATADO / "juro_real_10a.csv", index=False)
        print(f"Juro real 10 anos: {len(tabela)} dias "
              f"({tabela['data'].min()} a {tabela['data'].max()})")
    if vix:
        print("Baixando o VIX (FRED; se demorar, Cboe)...")
        try:
            fonte, texto, tabela = fred.baixar_vix()
        except RuntimeError as erro:
            print(f"VIX: falhou nas duas fontes ({erro}); rode `agio coletar-controles --so-vix` mais tarde.")
            return
        arm.salvar_bruto_texto(f"{fonte}_vix", texto, hoje)
        tabela.to_csv(arm.TRATADO / "vix.csv", index=False)
        print(f"VIX ({fonte}): {len(tabela)} dias")


def testar(inicio: date | None = None, fim: date | None = None) -> None:
    """Teste formal. Com --inicio/--fim, roda só naquele período (validação).

    O ágio anormal usa sempre o histórico completo (mediana dos 60 dias
    anteriores); o recorte acontece depois, e os eventos fora do período saem.
    """
    from agio.analise import (ajustar_pelo_dolar, estudo_evento, montar_base, periodo,
                              quadro_hipoteses, regressao, regressao_repasse)

    def opcional(nome):
        try:
            return arm.ler_tratado(nome)
        except FileNotFoundError:
            print(f"Sem {nome}; rode `agio coletar-controles` para incluir.")
            return None

    base = montar_base(arm.ler_tratado("agio_diario"), arm.ler_tratado("painel_diario"),
                       arm.ler_tratado("ptax"), arm.ler_tratado("precos_usdt_brl"),
                       opcional("juro_real_10a"), opcional("vix"))
    eventos = pd.read_csv(ARQUIVO_EVENTOS)
    pasta = PASTA_RESULTADOS
    if inicio or fim:
        base = periodo(base, inicio, fim).reset_index(drop=True)
        datas_ev = pd.to_datetime(eventos["data"])
        if inicio:
            eventos = eventos[datas_ev >= pd.Timestamp(inicio)]
        if fim:
            eventos = eventos[datas_ev.loc[eventos.index] < pd.Timestamp(fim)]
        pasta = PASTA_RESULTADOS / f"periodo_{inicio or 'inicio'}_{fim or 'fim'}"
        print(f"Período: {base['data'].min():%d/%m/%Y} a {base['data'].max():%d/%m/%Y}, "
              f"{len(base)} dias, {len(eventos)} eventos.")
    base["agio_ajustado_dolar"] = ajustar_pelo_dolar(base)
    pasta.mkdir(parents=True, exist_ok=True)
    base.to_csv(pasta / "base_teste.csv", index=False)

    relatorio = []
    guardado = {}
    for y, titulo in [("agio_anormal", "Ágio anormal (p.p.)"),
                      ("negocios_anormal", "Número de negócios anormal (log)"),
                      ("ticket_anormal", "Ticket médio anormal (log)")]:
        modelo, tabela = regressao(base, y)
        tabela.to_csv(pasta / f"regressao_{y}.csv", index=False)
        guardado[f"reg_{y}"] = tabela
        relatorio += [f"\n=== Regressão: {titulo} ===", str(modelo.summary())]

    modelo, tabela, soma = regressao_repasse(base)
    tabela.to_csv(pasta / "regressao_repasse.csv", index=False)
    pd.DataFrame([soma]).to_csv(pasta / "regressao_repasse_soma.csv", index=False)
    relatorio += ["\n=== Repasse do câmbio: ágio anormal ~ dólar no dia e 3 dias antes ===",
                  tabela.round(4).to_string(index=False),
                  "Soma das defasagens (volta do ágio nos dias seguintes): "
                  + ", ".join(f"{k}={v:.4f}" for k, v in soma.items())]

    if eventos.get("fonte", pd.Series(dtype=str)).astype(str).str.contains("A CONFIRMAR").any():
        print("Atenção: dados/manual/eventos.csv ainda tem eventos marcados como A CONFIRMAR.")
    listas = [("", eventos)]
    if "sobreposto" in eventos:
        # Copom e Fed costumam decidir na mesma semana: a versão sem sobrepostos
        # isola cada choque de eventos de outro tipo na mesma janela.
        listas.append(("_sem_sobrepostos", eventos[eventos["sobreposto"] == "nao"]))
    for sufixo, lista in listas:
        if lista.empty:
            continue
        for y in ["agio_anormal", "agio_ajustado_dolar", "negocios_anormal"]:
            por_evento, grupos, comp = estudo_evento(base, lista, y)
            guardado[f"ev_{y}{sufixo}"] = (grupos, comp)
            por_evento.to_csv(pasta / f"eventos_{y}{sufixo}.csv", index=False)
            grupos.to_csv(pasta / f"eventos_grupos_{y}{sufixo}.csv", index=False)
            titulo = f"{y}{' (sem sobrepostos)' if sufixo else ''}"
            relatorio += [f"\n=== Estudo de evento: {titulo} ===",
                          f"Datas placebo disponíveis: {grupos.attrs.get('n_placebo')}",
                          grupos.round(3).to_string(index=False)]
            if comp:
                pd.DataFrame([comp]).to_csv(pasta / f"eventos_comparacao_{y}{sufixo}.csv",
                                            index=False)
                relatorio.append("Domésticos x externos: " + ", ".join(
                    f"{k}={v:.3f}" for k, v in comp.items()))
    if "ev_negocios_anormal" in guardado:
        alfa = 0.01 if (fim and fim <= date(2027, 10, 30)) else 0.05
        isolados = guardado.get("ev_agio_ajustado_dolar_sem_sobrepostos", (None, None))[0]
        quadro = quadro_hipoteses(guardado["reg_agio_anormal"], soma,
                                  guardado["ev_negocios_anormal"][0],
                                  guardado["ev_agio_anormal"][1], isolados, alfa=alfa)
        quadro.to_csv(pasta / "hipoteses.csv", index=False)
        relatorio += [f"\n=== Hipóteses do pré-registro (alfa = {alfa:.0%}; ver docs/pre-registro.md) ===",
                      quadro.round(4).to_string(index=False)]
        if not (inicio or fim):
            relatorio.append("Amostra completa: V3 a V5 são exploratórias aqui; "
                             "a confirmação é na amostra de validação.")
    texto = "\n".join(relatorio)
    (pasta / "relatorio.txt").write_text(texto, encoding="utf-8")
    print(texto)
    print(f"\nResultados salvos em {pasta}")


def oferta_usdt(coletar: bool = True) -> None:
    """EXPLORATÓRIO (fora do pré-registro): oferta global de USDT e o ágio.

    Coleta a oferta diária na DefiLlama e roda a regressão do ágio anormal
    com a variação de 5 dias da oferta como variável a mais, na amostra de
    descoberta (até 30/10/2026). Resultado em dados/resultados/exploratorio_*.
    """
    from agio.analise import montar_base, periodo, regressao_oferta_usdt

    if coletar:
        print("Baixando a oferta de USDT (DefiLlama)...")
        bruto = defillama.baixar()
        arm.salvar_bruto("defillama_usdt", bruto, f"{date.today():%Y%m%d}")
        tabela = defillama.tratar(bruto)
        tabela.to_csv(arm.TRATADO / "usdt_oferta.csv", index=False)
        print(f"Oferta de USDT: {len(tabela)} dias ({tabela['data'].min()} a {tabela['data'].max()})")
    oferta = arm.ler_tratado("usdt_oferta")

    def opcional(nome):
        try:
            return arm.ler_tratado(nome)
        except FileNotFoundError:
            return None

    base = montar_base(arm.ler_tratado("agio_diario"), arm.ler_tratado("painel_diario"),
                       arm.ler_tratado("ptax"), arm.ler_tratado("precos_usdt_brl"),
                       opcional("juro_real_10a"), opcional("vix"))
    base = periodo(base, fim=date(2026, 10, 31))  # só a amostra de descoberta
    modelo, tabela, _ = regressao_oferta_usdt(base, oferta)
    PASTA_RESULTADOS.mkdir(parents=True, exist_ok=True)
    tabela.to_csv(PASTA_RESULTADOS / "exploratorio_oferta_usdt.csv", index=False)
    texto = ("=== EXPLORATÓRIO (fora do pré-registro): ágio anormal e oferta global de USDT ===\n"
             "var_oferta_usdt = variação % da oferta em 5 dias, com 1 dia de defasagem; "
             "sinal esperado: negativo.\n" + str(modelo.summary()))
    (PASTA_RESULTADOS / "exploratorio_oferta_usdt.txt").write_text(texto, encoding="utf-8")
    print(texto)

    o = oferta.assign(data=lambda d: pd.to_datetime(d["data"])).set_index("data")["usdt_oferta_bi"]
    mensal = o.resample("ME").last()
    print("\nOferta de USDT no fim de cada mês de 2026 (US$ bi):")
    print(mensal[mensal.index.year == 2026].round(1).to_string())


def relatorio() -> None:
    from agio.relatorio import gerar
    gerar()


# Início previsto das obrigações de informação da Resolução BCB 521. Atenção:
# a Resolução 574 (18/06/2026) adiou para 03/11/2026 o reporte de operações
# com ativos virtuais no câmbio; ver docs/decisoes.md.
DATA_REGULACAO = date(2026, 5, 4)


def _horas_do_bruto(nome: str) -> pd.DataFrame:
    """Relê os candles horários guardados em dados/bruto, sem nova coleta."""
    modulo = CORRETORAS[nome][0]
    arquivos = sorted((arm.BRUTO / f"{nome}_1h").glob("*.json"))
    lotes = [modulo.tratar_horario(json.loads(a.read_text(encoding="utf-8")), nome)
             for a in arquivos]
    lotes = [l for l in lotes if not l.empty]
    if not lotes:
        return pd.DataFrame()
    return pd.concat(lotes).drop_duplicates(["inicio_utc", "fonte"], keep="last")


def robustez() -> None:
    """Repete a regressão do ágio anormal em especificações alternativas.

    A pergunta é se o resultado principal (juro real fraco, VIX significativo)
    depende de escolhas de medida, de corretora, de período ou de poucos dias
    extremos.
    """
    from agio.analise import (CONTROLES, montar_base, periodo, resumo_especificacao,
                              winsorizar)

    def opcional(nome):
        try:
            return arm.ler_tratado(nome)
        except FileNotFoundError:
            return None

    ptax = arm.ler_tratado("ptax")
    painel = arm.ler_tratado("painel_diario")
    precos = arm.ler_tratado("precos_usdt_brl")
    juro, vix = opcional("juro_real_10a"), opcional("vix")

    def base_de(agio_diario):
        return montar_base(agio_diario, painel, ptax, precos, juro, vix)

    principal = base_de(arm.ler_tratado("agio_diario"))
    linhas = [
        resumo_especificacao("1. Principal (janela 10h-13h, MQO + Newey-West)", principal),
        resumo_especificacao("2. Winsorizado 1%/99%",
                             winsorizar(principal, ["agio_anormal"] + CONTROLES)),
        resumo_especificacao("3. Regressão robusta (Huber)", principal, metodo="huber"),
        resumo_especificacao("4. Ágio de fechamento (21h)",
                             base_de(arm.ler_tratado("agio_fechamento_diario"))),
    ]

    por_fonte = arm.ler_tratado("agio_por_fonte")
    for fonte in sorted(por_fonte["fonte"].unique()):
        so = por_fonte[por_fonte["fonte"] == fonte][["data", "agio_pct"]]
        linhas.append(resumo_especificacao(f"5. Só {fonte}", base_de(so)))

    linhas.append(resumo_especificacao(f"6a. Antes de {DATA_REGULACAO:%d/%m/%Y}",
                                       periodo(principal, fim=DATA_REGULACAO)))
    linhas.append(resumo_especificacao(f"6b. A partir de {DATA_REGULACAO:%d/%m/%Y}",
                                       periodo(principal, inicio=DATA_REGULACAO)))

    lotes = []
    for nome in CORRETORAS:
        horas = _horas_do_bruto(nome)
        if not horas.empty:
            lotes.append(preco_janela_ptax(horas, hora_fim=14))
    if lotes:
        janela = calcular_agio(pd.concat(lotes), ptax, coluna_preco="preco_janela",
                               coluna_volume="volume_janela")
        linhas.append(resumo_especificacao("7. Janela 10h-14h (inclui a consulta das 13h)",
                                           base_de(consolidar(janela))))
    else:
        print("Sem candles horários em dados/bruto; a especificação 7 ficou de fora.")

    tabela = pd.DataFrame(linhas)
    PASTA_RESULTADOS.mkdir(parents=True, exist_ok=True)
    tabela.to_csv(PASTA_RESULTADOS / "robustez.csv", index=False)

    colunas = ["especificacao", "n"] + [c for c in tabela.columns
                                         if c.endswith(("_coef", "_p"))]
    texto = ("=== Robustez: ágio anormal (coeficiente e p-valor) ===\n"
             + tabela[colunas].to_string(index=False, float_format=lambda v: f"{v:.4f}"))
    (PASTA_RESULTADOS / "robustez.txt").write_text(texto, encoding="utf-8")
    print(texto)
    print(f"\nResultados salvos em {PASTA_RESULTADOS / 'robustez.csv'}")


def importar_trends() -> None:
    buscas = google_trends.importar_pasta(PASTA_TRENDS)
    buscas.to_csv(arm.TRATADO / "google_trends.csv", index=False)
    print(f"Google Trends: {buscas['data'].nunique()} dias, termos: "
          f"{', '.join(sorted(buscas['termo'].unique()))}")


def calcular() -> None:
    precos = arm.ler_tratado("precos_usdt_brl")
    ptax = arm.ler_tratado("ptax")

    # Ágio de fechamento (candle diário, 21h): mantido para comparação.
    fech = calcular_agio(precos, ptax)
    fech.to_csv(arm.TRATADO / "agio_fechamento_por_fonte.csv", index=False)
    dia_fech = consolidar(fech)
    dia_fech.to_csv(arm.TRATADO / "agio_fechamento_diario.csv", index=False)

    # Ágio alinhado à PTAX (10h-13h): medida principal quando disponível.
    try:
        janela = arm.ler_tratado("precos_janela_ptax")
        agio = calcular_agio(janela, ptax, coluna_preco="preco_janela",
                             coluna_volume="volume_janela")
        medida = "alinhado à janela da PTAX (10h-13h)"
    except FileNotFoundError:
        agio = fech
        medida = "de fechamento (rode `agio coletar-horario` para o alinhado)"
    agio.to_csv(arm.TRATADO / "agio_por_fonte.csv", index=False)
    dia = consolidar(agio)
    dia.to_csv(arm.TRATADO / "agio_diario.csv", index=False)
    print(f"Ágio {medida}: {len(dia)} dias úteis.")

    if agio is not fech:
        comp = dia.merge(dia_fech[["data", "agio_pct"]], on="data",
                         suffixes=("", "_fechamento"))
        comp["diferenca"] = comp["agio_pct"] - comp["agio_pct_fechamento"]
        print(f"Correlação alinhado x fechamento: {comp['agio_pct'].corr(comp['agio_pct_fechamento']):.3f}")
        print("Dias em que o horário mais mudou o resultado:")
        print(comp.reindex(comp["diferenca"].abs().sort_values(ascending=False).index)
              .head(8)[["data", "agio_pct", "agio_pct_fechamento"]].to_string(index=False))

    sinais = sinais_mercado(precos)
    sinais.to_csv(arm.TRATADO / "sinais_comportamento.csv", index=False)
    try:
        buscas = arm.ler_tratado("google_trends")
    except FileNotFoundError:
        buscas = None
        print("Sem Google Trends ainda; rode `agio importar-trends` para incluir as buscas.")
    painel = painel_diario(dia, sinais, buscas)
    painel = painel.merge(dia_fech[["data", "agio_pct"]].rename(
        columns={"agio_pct": "agio_fechamento_pct"}), on="data", how="left")
    painel.to_csv(arm.TRATADO / "painel_diario.csv", index=False)
    print(f"Painel diário (ágio + comportamento): {len(painel)} dias.")
    print(painel.tail(10).to_string(index=False))


def grafico() -> None:
    import matplotlib.pyplot as plt

    df = pd.read_csv(arm.TRATADO / "agio_por_fonte.csv", parse_dates=["data"])
    rotulo = "janela 10h-13h" if "preco_janela" in df.columns else "fechamento 21h"
    fig, ax = plt.subplots(figsize=(10, 4))
    for fonte, g in df.groupby("fonte"):
        ax.plot(g["data"], g["agio_pct"], label=fonte, linewidth=1)
    ax.axhline(0, color="grey", linewidth=0.8)
    ax.set_ylabel("Ágio sobre a PTAX (%)")
    ax.set_title("Ágio do USDT em reais sobre a PTAX (" + rotulo + ")")
    ax.legend()
    fig.tight_layout()
    saida = arm.RAIZ / "grafico_agio.png"
    fig.savefig(saida, dpi=150)
    print(f"Gráfico salvo em {saida}")


def main() -> None:
    p = argparse.ArgumentParser(prog="agio")
    sub = p.add_subparsers(dest="comando", required=True)
    c = sub.add_parser("coletar")
    c.add_argument("--inicio", type=date.fromisoformat, required=True)
    c.add_argument("--fim", type=date.fromisoformat, default=date.today())
    h = sub.add_parser("coletar-horario")
    h.add_argument("--inicio", type=date.fromisoformat, required=True)
    h.add_argument("--fim", type=date.fromisoformat, default=date.today())
    sub.add_parser("calcular")
    sub.add_parser("grafico")
    sub.add_parser("importar-trends")
    cc = sub.add_parser("coletar-controles")
    so = cc.add_mutually_exclusive_group()
    so.add_argument("--so-vix", action="store_true", help="coleta só o VIX")
    so.add_argument("--so-juro", action="store_true", help="coleta só o juro real")
    t = sub.add_parser("testar")
    t.add_argument("--inicio", type=date.fromisoformat, default=None,
                   help="só dias a partir desta data (validação fora da amostra)")
    t.add_argument("--fim", type=date.fromisoformat, default=None,
                   help="só dias antes desta data")
    sub.add_parser("relatorio")
    ou = sub.add_parser("oferta-usdt", help="exploratório: oferta global de USDT e o ágio")
    ou.add_argument("--sem-coleta", action="store_true", help="usa a oferta já baixada")
    ep = sub.add_parser("episodio", help="diagnóstico de um período de ágio fora do normal")
    ep.add_argument("--inicio", type=date.fromisoformat, required=True)
    ep.add_argument("--fim", type=date.fromisoformat, required=True)
    sub.add_parser("robustez")
    args = p.parse_args()
    if args.comando == "coletar":
        coletar(args.inicio, args.fim)
    elif args.comando == "coletar-horario":
        coletar_horario(args.inicio, args.fim)
    elif args.comando == "calcular":
        calcular()
    elif args.comando == "importar-trends":
        importar_trends()
    elif args.comando == "coletar-controles":
        coletar_controles(juro=not args.so_vix, vix=not args.so_juro)
    elif args.comando == "testar":
        testar(args.inicio, args.fim)
    elif args.comando == "relatorio":
        relatorio()
    elif args.comando == "oferta-usdt":
        oferta_usdt(coletar=not args.sem_coleta)
    elif args.comando == "episodio":
        from agio.episodio import rodar
        rodar(args.inicio, args.fim)
    elif args.comando == "robustez":
        robustez()
    else:
        grafico()


if __name__ == "__main__":
    main()
