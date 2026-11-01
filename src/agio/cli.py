"""Linha de comando.

    agio coletar --inicio 2026-01-01           # baixa tudo até hoje
    agio coletar --inicio 2026-01-01 --fim 2026-10-30
    agio calcular                              # gera o ágio a partir do tratado
    agio grafico                               # salva dados/grafico_agio.png
    agio coletar-horario --inicio 2020-10-01   # candles horários -> preço na janela da PTAX
    agio importar-trends                       # lê os CSVs de dados/manual/google_trends
"""

from __future__ import annotations

import argparse
from datetime import date

import pandas as pd

from agio import armazenamento as arm
from agio.comportamento import painel_diario, sinais_mercado
from agio.fontes import bcb, binance, google_trends, mercadobitcoin
from agio.indicador import calcular_agio, consolidar
from agio.janela import preco_janela_ptax

PASTA_TRENDS = arm.RAIZ / "manual" / "google_trends"

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
    args = p.parse_args()
    if args.comando == "coletar":
        coletar(args.inicio, args.fim)
    elif args.comando == "coletar-horario":
        coletar_horario(args.inicio, args.fim)
    elif args.comando == "calcular":
        calcular()
    elif args.comando == "importar-trends":
        importar_trends()
    else:
        grafico()


if __name__ == "__main__":
    main()
