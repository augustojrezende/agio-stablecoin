"""Cálculo do ágio diário da stablecoin em reais sobre o dólar oficial.

    agio = preço de fechamento do USDT em BRL / PTAX de venda - 1

Decisões metodológicas (registre mudanças em docs/decisoes.md):

1. Referência oficial: PTAX de venda de fechamento do Banco Central.
2. Só dias úteis com PTAX entram no indicador. Fins de semana e feriados
   ficam no arquivo de preços, mas não têm ágio calculado.
3. Descasamento de horário: a PTAX fecha por volta das 13h (Brasília); o
   candle diário das corretoras fecha às 21h (meia-noite UTC). O ágio diário
   carrega, portanto, a variação do câmbio da tarde. Para o estudo de evento,
   isso é ruído, não viés; numa versão futura, use candles horários.
"""

from __future__ import annotations

import pandas as pd


def calcular_agio(precos: pd.DataFrame, ptax: pd.DataFrame) -> pd.DataFrame:
    """Uma linha por (data, fonte), com o ágio em proporção e em %."""
    base = precos.merge(ptax[["data", "ptax_venda"]], on="data", how="inner")
    base = base[base["fechamento"].notna() & (base["ptax_venda"] > 0)].copy()
    base["agio"] = base["fechamento"] / base["ptax_venda"] - 1
    base["agio_pct"] = base["agio"] * 100
    colunas = ["data", "fonte", "fechamento", "ptax_venda", "agio", "agio_pct", "volume_base"]
    return base[colunas].sort_values(["data", "fonte"]).reset_index(drop=True)


def consolidar(agio: pd.DataFrame) -> pd.DataFrame:
    """Ágio do dia ponderado pelo volume das corretoras (média simples se faltar volume)."""
    def _dia(g: pd.DataFrame) -> pd.Series:
        peso = g["volume_base"].fillna(0)
        valor = (g["agio"] * peso).sum() / peso.sum() if peso.sum() > 0 else g["agio"].mean()
        return pd.Series({"agio": valor, "agio_pct": valor * 100, "n_fontes": len(g)})

    return agio.groupby("data").apply(_dia, include_groups=False).reset_index()
