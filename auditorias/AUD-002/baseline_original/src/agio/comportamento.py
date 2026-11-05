"""Sinais de comportamento coletivo (análise 3 do TCC).

Os dados são agregados: medem comportamento coletivo, não a motivação de
cada investidor (ver docs/decisoes.md, falácia ecológica).
"""

from __future__ import annotations

import pandas as pd


def sinais_mercado(precos: pd.DataFrame) -> pd.DataFrame:
    """Urgência, participação e perfil das compras, por dia e corretora.

    - pressao_compradora: parcela do volume comprada por quem aceitou o preço
      pedido (0,5 = equilíbrio; acima disso, pressa em comprar)
    - num_negocios: número de negócios no dia (participação)
    - ticket_medio_brl: valor médio de cada negócio em reais (perfil;
      quanto menor, maior o peso do varejo)
    """
    df = precos.copy()
    for c in ["volume_brl", "num_negocios", "volume_compra_taker"]:
        if c not in df:
            df[c] = float("nan")
    vol = df["volume_base"].where(df["volume_base"] > 0)
    neg = df["num_negocios"].where(df["num_negocios"] > 0)
    df["pressao_compradora"] = df["volume_compra_taker"] / vol
    df["ticket_medio_brl"] = df["volume_brl"] / neg
    colunas = ["data", "fonte", "num_negocios", "pressao_compradora", "ticket_medio_brl"]
    return df[colunas].sort_values(["data", "fonte"]).reset_index(drop=True)


def painel_diario(agio_diario: pd.DataFrame, sinais: pd.DataFrame,
                  buscas: pd.DataFrame | None = None) -> pd.DataFrame:
    """Uma linha por dia útil: ágio consolidado, sinais de mercado e buscas.

    Os sinais de mercado vêm da corretora que os informa (hoje, a Binance).
    As buscas entram em colunas `busca_<termo>`.
    """
    mercado = (sinais.dropna(subset=["num_negocios"])
               .groupby("data")[["num_negocios", "pressao_compradora", "ticket_medio_brl"]]
               .first())
    painel = agio_diario.set_index("data").join(mercado, how="left")
    if buscas is not None and not buscas.empty:
        largas = buscas.pivot_table(index="data", columns="termo", values="interesse")
        largas.columns = [f"busca_{t.lower().replace(' ', '_')}" for t in largas.columns]
        painel = painel.join(largas, how="left")
    return painel.reset_index()
