"""Diagnóstico de um episódio: o ágio alto é real ou é problema de medição?

    agio episodio --inicio 2026-06-01 --fim 2026-08-15

Para cada dia do período mostra, lado a lado, o que pode explicar um ágio
fora do normal:

- se aparece nas duas corretoras ou só em uma (problema local x mercado);
- se aparece na janela da PTAX e no fechamento (horário x nível);
- se o preço do USDT subiu ou se a PTAX caiu (de que lado veio o ágio);
- volume, horas com negócio na janela, número de negócios, pressão
  compradora e ticket médio (liquidez e comportamento).

Grava `dados/resultados/episodio_<inicio>_<fim>.csv` e um gráfico em
`docs/figuras/episodio_<inicio>_<fim>.png`.
"""

from __future__ import annotations

from datetime import date

import pandas as pd

from agio import armazenamento as arm

RESULTADOS = arm.RAIZ / "resultados"
FIGURAS = arm.RAIZ.parent / "docs" / "figuras"


def _opcional(nome: str) -> pd.DataFrame | None:
    try:
        return arm.ler_tratado(nome)
    except FileNotFoundError:
        print(f"  (sem {nome})")
        return None


def montar(inicio: date, fim: date, contexto_dias: int = 90) -> pd.DataFrame:
    """Uma linha por dia útil, com o normal calculado nos 60 dias antes."""
    ptax = arm.ler_tratado("ptax")[["data", "ptax_venda"]]
    base = ptax.copy()

    janela = _opcional("agio_por_fonte")
    if janela is not None:
        largo = janela.pivot_table(index="data", columns="fonte", values="agio_pct")
        largo.columns = [f"agio_janela_{c}" for c in largo.columns]
        base = base.merge(largo.reset_index(), on="data", how="left")
        if "preco_janela" in janela:
            preco = janela.pivot_table(index="data", columns="fonte", values="preco_janela")
            preco.columns = [f"preco_janela_{c}" for c in preco.columns]
            base = base.merge(preco.reset_index(), on="data", how="left")

    fech = _opcional("agio_fechamento_por_fonte")
    if fech is not None:
        largo = fech.pivot_table(index="data", columns="fonte", values="agio_pct")
        largo.columns = [f"agio_fech_{c}" for c in largo.columns]
        base = base.merge(largo.reset_index(), on="data", how="left")

    consolidado = _opcional("agio_diario")
    if consolidado is not None:
        base = base.merge(consolidado[["data", "agio_pct"]].rename(
            columns={"agio_pct": "agio_consolidado"}), on="data", how="left")

    horas = _opcional("precos_janela_ptax")
    if horas is not None:
        h = horas.pivot_table(index="data", columns="fonte",
                              values=["horas_janela", "volume_janela"])
        h.columns = [f"{a}_{b}" for a, b in h.columns]
        base = base.merge(h.reset_index(), on="data", how="left")

    sinais = _opcional("sinais_comportamento")
    if sinais is not None:
        s = sinais[sinais["fonte"] == "binance"][
            ["data", "num_negocios", "pressao_compradora", "ticket_medio_brl"]]
        base = base.merge(s, on="data", how="left")

    oferta = _opcional("usdt_oferta")
    if oferta is not None:
        base = base.merge(oferta, on="data", how="left")
        base["usdt_oferta_bi"] = base["usdt_oferta_bi"].ffill()

    base = base.sort_values("data").reset_index(drop=True)
    base["var_ptax_pct"] = 100 * base["ptax_venda"].pct_change()
    for c in [c for c in base.columns if c.startswith("agio_")] + ["num_negocios"]:
        if c in base:
            base[f"{c}_normal"] = base[c].shift(1).rolling(60, min_periods=30).median()

    inicio_ctx = pd.Timestamp(inicio) - pd.Timedelta(days=contexto_dias)
    datas = pd.to_datetime(base["data"])
    base = base[(datas >= inicio_ctx) & (datas < pd.Timestamp(fim))].copy()
    base["no_episodio"] = pd.to_datetime(base["data"]) >= pd.Timestamp(inicio)
    return base.reset_index(drop=True)


def resumo(base: pd.DataFrame) -> str:
    """Comparação do episódio com os 90 dias anteriores, em texto."""
    antes, durante = base[~base["no_episodio"]], base[base["no_episodio"]]
    linhas = ["Média nos 90 dias antes x durante o episódio:"]
    colunas = [c for c in base.columns if (c.startswith(("agio_", "horas_janela", "volume_janela"))
               and not c.endswith("_normal")) or c in
               ("num_negocios", "pressao_compradora", "ticket_medio_brl", "var_ptax_pct",
                    "usdt_oferta_bi")]
    for c in colunas:
        linhas.append(f"  {c:32s} {antes[c].mean():>12.3f} {durante[c].mean():>12.3f}")
    duas = [c for c in base.columns if c.startswith("agio_janela_")]
    if len(duas) >= 2:
        d = durante[duas].dropna()
        linhas.append(f"Correlação entre corretoras no episódio: {d[duas[0]].corr(d[duas[1]]):.2f} "
                      f"({len(d)} dias com as duas)")
    perguntas = [
        "Leitura:",
        "  - Ágio alto nas duas corretoras -> fenômeno de mercado; só em uma -> problema local.",
        "  - Alto na janela e no fechamento -> nível; só na janela -> horário ou pouca liquidez.",
        "  - horas_janela ou volume_janela muito menores -> preço de poucos negócios.",
        "  - Pressão compradora > 0,5 e mais negócios -> procura; ticket menor -> varejo.",
    ]
    return "\n".join(linhas + perguntas)


def grafico(base: pd.DataFrame, caminho) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    datas = pd.to_datetime(base["data"])
    fig, eixos = plt.subplots(3, 1, figsize=(9, 7.5), sharex=True)
    ax = eixos[0]
    for c in [c for c in base.columns if c.startswith(("agio_janela_", "agio_fech_"))
              and not c.endswith("_normal")]:
        estilo = "-" if "janela" in c else ":"
        ax.plot(datas, base[c], estilo, lw=1, label=c.replace("agio_", ""))
    ax.axhline(0, color="black", lw=0.5)
    ax.set_ylabel("Ágio (%)")
    ax.legend(frameon=False, fontsize=7, ncol=2)
    ax.set_title("Episódio: ágio por corretora e horário")

    ax = eixos[1]
    ax.plot(datas, base["ptax_venda"], color="black", lw=1, label="PTAX de venda")
    for c in [c for c in base.columns if c.startswith("preco_janela_")]:
        ax.plot(datas, base[c], lw=0.8, label=c.replace("preco_janela_", "USDT "))
    ax.set_ylabel("R$ por dólar")
    ax.legend(frameon=False, fontsize=7)

    ax = eixos[2]
    if "num_negocios" in base:
        ax.bar(datas, base["num_negocios"], color="#7f8c8d", width=1, label="Negócios (Binance)")
        ax.set_ylabel("Negócios por dia")
    if "pressao_compradora" in base:
        ax2 = ax.twinx()
        ax2.plot(datas, base["pressao_compradora"], color="#c0392b", lw=1, label="Pressão compradora")
        ax2.axhline(0.5, color="#c0392b", lw=0.5, ls="--")
        ax2.set_ylabel("Pressão compradora")
    for a in eixos:
        a.axvspan(datas[base["no_episodio"]].min(), datas.max(), color="#f9e79f", alpha=0.3, zorder=0)
    fig.tight_layout()
    caminho.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(caminho, dpi=150)
    plt.close(fig)


def rodar(inicio: date, fim: date) -> None:
    base = montar(inicio, fim)
    rotulo = f"{inicio:%Y%m%d}_{fim:%Y%m%d}"
    RESULTADOS.mkdir(parents=True, exist_ok=True)
    base.to_csv(RESULTADOS / f"episodio_{rotulo}.csv", index=False)
    grafico(base, FIGURAS / f"episodio_{rotulo}.png")
    cols = ["data", "ptax_venda", "var_ptax_pct"] + [
        c for c in base.columns if c.startswith(("agio_janela_", "agio_fech_", "horas_janela_"))
        and not c.endswith("_normal")] + [c for c in ("num_negocios", "pressao_compradora")
                                           if c in base]
    durante = base[base["no_episodio"]][cols]
    print(durante.to_string(index=False, float_format=lambda v: f"{v:.3f}"))
    print()
    print(resumo(base))
    print(f"\nTabela: {RESULTADOS / f'episodio_{rotulo}.csv'}")
    print(f"Gráfico: {FIGURAS / f'episodio_{rotulo}.png'}")
