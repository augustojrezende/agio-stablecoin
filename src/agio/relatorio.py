"""Gráficos e tabelas do TCC, gerados a partir dos dados e dos resultados.

    agio testar && agio robustez && agio relatorio

Grava as figuras em docs/figuras/ e as tabelas em docs/resultados_tabelas.md.
O texto que interpreta cada resultado fica em docs/resultados.md (escrito à
mão); este módulo só regenera números e gráficos, para que o relatório
acompanhe qualquer nova rodada.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

from agio import armazenamento as arm

DOCS = arm.RAIZ.parent / "docs"
FIGURAS = DOCS / "figuras"
RESULTADOS = arm.RAIZ / "resultados"
EVENTOS = arm.RAIZ / "manual" / "eventos.csv"

CORES = {"fiscal": "#c0392b", "externo": "#2471a3", "monetario": "#7d3c98",
         "politico": "#d68910", "regulatorio": "#148f77", "placebo": "#7f8c8d"}
NOMES_TIPO = {"fiscal": "Fiscal", "externo": "Externo", "monetario": "Monetário (Copom)",
              "politico": "Político", "regulatorio": "Regulatório"}


def _plt():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"figure.dpi": 150, "axes.spines.top": False,
                         "axes.spines.right": False, "font.size": 9})
    return plt


def _ler(caminho: Path, datas: tuple[str, ...] = ("data",)) -> pd.DataFrame | None:
    if not caminho.exists():
        print(f"  (sem {caminho.name}; parte do relatório fica de fora)")
        return None
    df = pd.read_csv(caminho)
    for c in datas:
        if c in df:
            df[c] = pd.to_datetime(df[c])
    return df


def _salvar(fig, nome: str, legenda: str, lista: list) -> None:
    FIGURAS.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(FIGURAS / nome)
    lista.append((nome, legenda))


# --- Figuras ---------------------------------------------------------------

def fig_serie(plt, figs):
    alinhado = _ler(arm.TRATADO / "agio_diario.csv")
    fech = _ler(arm.TRATADO / "agio_fechamento_diario.csv")
    if alinhado is None:
        return
    fig, ax = plt.subplots(figsize=(9, 3.6))
    if fech is not None:
        ax.plot(fech["data"], fech["agio_pct"], color="#bbbbbb", lw=0.6,
                label="Fechamento (21h), comparação")
    ax.plot(alinhado["data"], alinhado["agio_pct"], color="#1a5276", lw=0.7,
            label="Janela da PTAX (10h-13h), medida principal")
    med = alinhado.set_index("data")["agio_pct"].rolling(60, min_periods=30).median()
    ax.plot(med.index, med.values, color="#e67e22", lw=1.4, label="Mediana móvel de 60 dias úteis")
    ax.axhline(0, color="black", lw=0.6)
    ax.set_ylabel("Ágio sobre a PTAX (%)")
    ax.set_title("Ágio do USDT em reais sobre o dólar oficial")
    ax.legend(loc="upper right", frameon=False)
    _salvar(fig, "01_serie_agio.png",
            "Ágio diário do USDT/BRL sobre a PTAX de venda: medida alinhada à janela da PTAX, "
            "medida de fechamento e mediana móvel (o 'normal' usado no ágio anormal).", figs)
    plt.close(fig)


def fig_janela_vs_fechamento(plt, figs):
    painel = _ler(arm.TRATADO / "painel_diario.csv")
    if painel is None or "agio_fechamento_pct" not in painel:
        return
    p = painel.dropna(subset=["agio_pct", "agio_fechamento_pct"])
    fig, ax = plt.subplots(figsize=(4.6, 4.2))
    ax.scatter(p["agio_fechamento_pct"], p["agio_pct"], s=4, alpha=0.4, color="#1a5276")
    lim = [min(p["agio_fechamento_pct"].min(), p["agio_pct"].min()),
           max(p["agio_fechamento_pct"].max(), p["agio_pct"].max())]
    ax.plot(lim, lim, color="black", lw=0.6, ls="--")
    r = p["agio_pct"].corr(p["agio_fechamento_pct"])
    ax.set_xlabel("Ágio de fechamento, 21h (%)")
    ax.set_ylabel("Ágio na janela da PTAX (%)")
    ax.set_title(f"Efeito do horário de medição (correlação {r:.2f})")
    _salvar(fig, "02_janela_vs_fechamento.png",
            "Cada ponto é um dia. Fora da diagonal estão os dias em que o horário de medição muda "
            "o ágio; os maiores desvios caem em dias de choque, o que motivou a medida alinhada.", figs)
    plt.close(fig)


def fig_corretoras(plt, figs):
    por_fonte = _ler(arm.TRATADO / "agio_por_fonte.csv")
    if por_fonte is None:
        return
    fig, ax = plt.subplots(figsize=(9, 3.2))
    for fonte, g in por_fonte.groupby("fonte"):
        ax.plot(g["data"], g["agio_pct"], lw=0.6, label=fonte)
    largo = por_fonte.pivot_table(index="data", columns="fonte", values="agio_pct")
    titulo = "Ágio por corretora (janela da PTAX)"
    if largo.shape[1] >= 2:
        titulo += f", correlação {largo.corr().iloc[0, 1]:.2f}"
    ax.axhline(0, color="black", lw=0.6)
    ax.set_ylabel("Ágio (%)")
    ax.set_title(titulo)
    ax.legend(frameon=False)
    _salvar(fig, "03_agio_por_corretora.png",
            "Ágio calculado separadamente em cada corretora. A Binance concentra o volume, "
            "por isso o indicador consolidado é, na prática, o da Binance.", figs)
    plt.close(fig)


def fig_anormal_eventos(plt, figs, base, eventos):
    fig, ax = plt.subplots(figsize=(9, 3.6))
    ax.plot(base["data"], base["agio_anormal"], color="#555555", lw=0.5)
    nao = eventos[eventos["agendado"] == "nao"] if "agendado" in eventos else eventos
    for _, e in nao.iterrows():
        ax.axvline(e["data"], color=CORES.get(e["tipo"], "black"), lw=0.8, alpha=0.8)
    for tipo in sorted(nao["tipo"].unique()):
        ax.plot([], [], color=CORES.get(tipo, "black"), label=NOMES_TIPO.get(tipo, tipo))
    ax.axhline(0, color="black", lw=0.6)
    ax.set_ylabel("Ágio anormal (p.p.)")
    ax.set_title("Ágio anormal e choques não agendados")
    ax.legend(frameon=False, ncol=3, loc="upper left")
    _salvar(fig, "04_agio_anormal_eventos.png",
            "Ágio do dia menos a mediana dos 60 dias úteis anteriores. Linhas verticais: eventos "
            "não agendados da lista (anúncios fiscais, choques externos, normas do BC).", figs)
    plt.close(fig)


def fig_dolar(plt, figs, base):
    b = base.dropna(subset=["d_dolar", "agio_anormal"])
    coef = np.polyfit(b["d_dolar"], b["agio_anormal"], 1)
    fig, ax = plt.subplots(figsize=(4.6, 4.2))
    ax.scatter(b["d_dolar"], b["agio_anormal"], s=4, alpha=0.35, color="#1a5276")
    x = np.linspace(b["d_dolar"].min(), b["d_dolar"].max(), 50)
    ax.plot(x, np.polyval(coef, x), color="#c0392b", lw=1.4,
            label=f"reta simples, sem controles: inclinação {coef[0]:.3f}")
    ax.axhline(0, color="black", lw=0.5)
    ax.axvline(0, color="black", lw=0.5)
    ax.set_xlabel("Variação do dólar oficial no dia (%)")
    ax.set_ylabel("Ágio anormal (p.p.)")
    ax.set_title("Repasse incompleto do câmbio")
    ax.legend(frameon=False)
    _salvar(fig, "05_dolar_e_agio.png",
            "Quando o dólar oficial sobe, o ágio cai: o USDT acompanha só parte do movimento "
            "no mesmo dia. A reta é simples, sem controles; na regressão com controles o "
            "coeficiente é cerca de −0,13, e o ágio continua caindo nos dois dias seguintes. "
            "O ponto mais à direita é 26/10/2026 (dólar +8,8% após o segundo turno), dado "
            "real conferido no noticiário.", figs)
    plt.close(fig)


def fig_trajetorias(plt, figs, base, eventos, coluna, nome, titulo, ylabel, legenda,
                    tipos=("fiscal", "externo", "monetario")):
    from agio.analise import trajetoria_evento
    fig, eixos = plt.subplots(1, len(tipos), figsize=(9, 3.2), sharey=True)
    for ax, tipo in zip(np.atleast_1d(eixos), tipos):
        lista = eventos[eventos["tipo"] == tipo]
        if lista.empty:
            continue
        tr = trajetoria_evento(base, lista, coluna)
        ax.fill_between(tr["dia"], tr["placebo_p025"], tr["placebo_p975"],
                        color=CORES["placebo"], alpha=0.25, label="Faixa de 95% das datas sorteadas")
        ax.plot(tr["dia"], tr["media"], color=CORES[tipo], lw=1.6, marker="o", ms=2.5,
                label="Média nos eventos")
        ax.axvspan(-1, 3, color="#f9e79f", alpha=0.35, zorder=0)
        ax.axvline(0, color="black", lw=0.6)
        ax.axhline(0, color="black", lw=0.4)
        ax.set_title(f"{NOMES_TIPO[tipo]} (n = {int(tr['n_eventos'].iloc[0])})")
        ax.set_xlabel("Dias úteis em relação ao evento")
    np.atleast_1d(eixos)[0].set_ylabel(ylabel)
    np.atleast_1d(eixos)[0].legend(frameon=False, fontsize=7, loc="lower left")
    fig.suptitle(titulo)
    _salvar(fig, nome, legenda, figs)
    plt.close(fig)


def fig_robustez(plt, figs):
    rob = _ler(RESULTADOS / "robustez.csv", datas=())
    if rob is None:
        return
    from scipy import stats
    variaveis = [("d_juro_bp", "Juro real 10 anos (por bp)"),
                 ("d_vix_ant", "VIX do dia anterior (por ponto)")]
    fig, eixos = plt.subplots(1, 2, figsize=(9, 3.8), sharey=True)
    y = np.arange(len(rob))[::-1]
    for ax, (v, titulo) in zip(eixos, variaveis):
        coef = rob[f"{v}_coef"]
        if f"{v}_ep" in rob:
            ep = rob[f"{v}_ep"]
        else:  # rodadas antigas sem erro padrão: recupera pelo p-valor
            ep = coef.abs() / stats.norm.isf(rob[f"{v}_p"] / 2)
        cor = np.where(rob[f"{v}_p"] < 0.05, "#c0392b", "#7f8c8d")
        ax.errorbar(coef, y, xerr=1.96 * ep, fmt="none", ecolor=cor, elinewidth=1.2)
        ax.scatter(coef, y, color=cor, s=14, zorder=3)
        ax.axvline(0, color="black", lw=0.6)
        ax.set_title(titulo)
        ax.set_xlabel("Coeficiente e intervalo de 95%")
    eixos[0].set_yticks(y)
    eixos[0].set_yticklabels(rob["especificacao"], fontsize=7)
    fig.suptitle("Robustez: ágio anormal (vermelho = significativo a 5%)")
    _salvar(fig, "08_robustez.png",
            "Mesma regressão em 9 especificações. O VIX do dia anterior é positivo e "
            "significativo em quase todas; o juro real não é positivo e significativo em nenhuma.", figs)
    plt.close(fig)


# --- Tabelas ---------------------------------------------------------------

def _tabela_md(df: pd.DataFrame, casas: int = 4) -> str:
    df = df.copy()
    for c in df.select_dtypes("number"):
        df[c] = df[c].map(lambda v: "" if pd.isna(v) else f"{v:.{casas}f}")
    linhas = ["| " + " | ".join(df.columns) + " |", "|" + " --- |" * len(df.columns)]
    linhas += ["| " + " | ".join(str(v) for v in r) + " |" for r in df.itertuples(index=False)]
    return "\n".join(linhas)


def tabelas() -> str:
    partes = [f"# Tabelas de resultados\n\n*Gerado por `agio relatorio` em {date.today():%d/%m/%Y}. "
              "Não edite: rode o comando de novo. A interpretação está em `resultados.md`.*\n"]
    titulos = {"agio_anormal": "Ágio anormal (p.p.)",
               "negocios_anormal": "Número de negócios anormal (log)",
               "ticket_anormal": "Ticket médio anormal (log)"}
    partes.append("## Regressões (MQO, erros de Newey-West com 5 defasagens)\n")
    for y, t in titulos.items():
        df = _ler(RESULTADOS / f"regressao_{y}.csv", datas=())
        if df is not None:
            partes += [f"### {t}\n", _tabela_md(df), ""]
    df = _ler(RESULTADOS / "regressao_repasse.csv", datas=())
    soma = _ler(RESULTADOS / "regressao_repasse_soma.csv", datas=())
    if df is not None:
        partes += ["### Repasse do câmbio (dólar no dia e 3 dias antes)\n", _tabela_md(df), ""]
        if soma is not None:
            partes += ["Soma das defasagens:\n", _tabela_md(soma), ""]
    partes.append("## Estudo de evento (janela de −1 a +3 dias úteis)\n")
    for sufixo, rotulo in [("", "lista completa"), ("_sem_sobrepostos", "sem eventos sobrepostos")]:
        for y in ["agio_anormal", "agio_ajustado_dolar", "negocios_anormal"]:
            df = _ler(RESULTADOS / f"eventos_grupos_{y}{sufixo}.csv", datas=())
            if df is None:
                continue
            partes += [f"### {y}, {rotulo}\n", _tabela_md(df, 3), ""]
            comp = _ler(RESULTADOS / f"eventos_comparacao_{y}{sufixo}.csv", datas=())
            if comp is not None:
                partes += ["Domésticos x externos:\n", _tabela_md(comp, 3), ""]
    hip = _ler(RESULTADOS / "hipoteses.csv", datas=())
    if hip is not None:
        partes += ["## Hipóteses do pré-registro (amostra de descoberta)\n",
                   "*V3 a V5 surgiram nesta amostra: aqui são exploratórias. "
                   "A confirmação é na validação (`pre-registro.md`).*\n", _tabela_md(hip), ""]
    rob = _ler(RESULTADOS / "robustez.csv", datas=())
    if rob is not None:
        cols = ["especificacao", "n"] + [c for c in rob.columns if c.endswith(("_coef", "_p"))]
        partes += ["## Robustez (ágio anormal)\n", _tabela_md(rob[cols]), ""]
    ev = _ler(EVENTOS, datas=())
    if ev is not None:
        resumo = ev.groupby(["tipo", "agendado"]).size().rename("n").reset_index()
        partes += ["## Lista de eventos\n", f"{len(ev)} eventos em `dados/manual/eventos.csv` "
                   "(regra em `decisoes.md`).\n", _tabela_md(resumo, 0), ""]
    return "\n".join(partes)


def gerar() -> None:
    plt = _plt()
    figs: list[tuple[str, str]] = []
    print("Gerando figuras...")
    fig_serie(plt, figs)
    fig_janela_vs_fechamento(plt, figs)
    fig_corretoras(plt, figs)
    base = _ler(RESULTADOS / "base_teste.csv")
    eventos = _ler(EVENTOS)
    if base is not None and eventos is not None:
        fig_anormal_eventos(plt, figs, base, eventos)
        fig_dolar(plt, figs, base)
        fig_trajetorias(plt, figs, base, eventos, "agio_ajustado_dolar", "06_trajetoria_agio.png",
                        "Ágio anormal ajustado pelo dólar em torno dos eventos",
                        "Ágio ajustado (p.p.)",
                        "Média diária em torno de cada tipo de evento (faixa amarela: janela do "
                        "teste, −1 a +3) contra a faixa de 95% de datas sorteadas.")
        fig_trajetorias(plt, figs, base, eventos, "negocios_anormal", "07_trajetoria_negocios.png",
                        "Número de negócios anormal em torno dos eventos", "Negócios anormal (log)",
                        "Participação em torno dos eventos contra datas sorteadas. A participação "
                        "cresce com o mercado, por isso a comparação é com a faixa placebo, não com zero.")
    fig_robustez(plt, figs)

    texto = tabelas()
    if figs:
        texto += "\n## Figuras\n\n" + "\n\n".join(
            f"**{n}.** {leg}\n\n![{leg}](figuras/{n})" for n, leg in figs) + "\n"
    (DOCS / "resultados_tabelas.md").write_text(texto, encoding="utf-8")
    print(f"{len(figs)} figuras em {FIGURAS}")
    print(f"Tabelas em {DOCS / 'resultados_tabelas.md'}")
