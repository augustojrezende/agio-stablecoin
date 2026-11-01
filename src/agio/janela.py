"""Preço do USDT na mesma janela de horário da PTAX.

A PTAX de fechamento é a média de quatro consultas feitas pelo Banco Central
entre 10h e 13h (horário de Brasília). O candle diário das corretoras fecha às
21h, e em dias de crise o câmbio pode mudar muito entre um horário e outro.
Para comparar preços do mesmo momento, o ágio alinhado usa o preço médio do
USDT ponderado pelo volume entre 10h e 13h de Brasília.

O Brasil não tem horário de verão desde 2019, então a janela é sempre
13h a 16h UTC.
"""

from __future__ import annotations

import pandas as pd

FUSO_BRASILIA = "America/Sao_Paulo"
HORA_INICIO, HORA_FIM = 10, 13  # janela da PTAX, horário de Brasília


def preco_janela_ptax(horarios: pd.DataFrame, hora_fim: int = HORA_FIM) -> pd.DataFrame:
    """Um preço por dia e corretora: média ponderada por volume na janela da PTAX.

    Usa o preço típico de cada hora, (máxima + mínima + fechamento) / 3. Se o
    volume da janela for zero, usa a média simples dos fechamentos.

    hora_fim: primeira hora fora da janela. O padrão (13) cobre 10h a 12h59;
    o teste de robustez usa 14 para incluir a consulta das 13h.
    """
    colunas = ["data", "fonte", "preco_janela", "volume_janela", "horas_janela"]
    if horarios.empty:
        return pd.DataFrame(columns=colunas)
    df = horarios.copy()
    local = df["inicio_utc"].dt.tz_convert(FUSO_BRASILIA)
    df = df[(local.dt.hour >= HORA_INICIO) & (local.dt.hour < hora_fim)].copy()
    df["data"] = local.loc[df.index].dt.date
    df["tipico"] = (df["maxima"] + df["minima"] + df["fechamento"]) / 3

    def _dia(g: pd.DataFrame) -> pd.Series:
        vol = g["volume_base"].fillna(0)
        preco = (g["tipico"] * vol).sum() / vol.sum() if vol.sum() > 0 else g["fechamento"].mean()
        return pd.Series({"preco_janela": preco, "volume_janela": vol.sum(),
                          "horas_janela": len(g)})

    saida = df.groupby(["data", "fonte"]).apply(_dia, include_groups=False).reset_index()
    return saida[colunas].sort_values(["data", "fonte"]).reset_index(drop=True)
