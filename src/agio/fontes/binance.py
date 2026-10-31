"""Binance: candles diários do par USDT/BRL pela API pública de mercado.

Além do preço, cada candle traz dados de comportamento usados na análise 3:
número de negócios e volume comprado por quem aceitou o preço pedido
("taker"), um indicador de urgência ou pressão compradora.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

import pandas as pd

from agio.http import get_json

# Espelho público da Binance só para dados de mercado; não exige chave.
KLINES_URL = "https://data-api.binance.vision/api/v3/klines"
LIMITE = 1000

# Posições no array de cada candle, segundo a documentação da Binance.
COLUNAS_KLINE = [
    "abertura_ms", "abertura", "maxima", "minima", "fechamento", "volume_base",
    "fechamento_ms", "volume_brl", "num_negocios", "volume_compra_taker",
    "volume_compra_taker_brl", "ignorar",
]
COLUNAS_SAIDA = [
    "data", "fonte", "abertura", "maxima", "minima", "fechamento", "volume_base",
    "volume_brl", "num_negocios", "volume_compra_taker",
]


def _ms(d: date) -> int:
    return int(datetime(d.year, d.month, d.day, tzinfo=timezone.utc).timestamp() * 1000)


def baixar(simbolo: str, inicio: date, fim: date) -> list[list]:
    """Candles diários (UTC) entre inicio e fim, paginando de 1000 em 1000."""
    linhas: list[list] = []
    cursor = _ms(inicio)
    fim_ms = _ms(fim + timedelta(days=1)) - 1
    while cursor <= fim_ms:
        lote = get_json(
            KLINES_URL,
            {"symbol": simbolo, "interval": "1d", "startTime": cursor,
             "endTime": fim_ms, "limit": LIMITE},
        )
        if not lote:
            break
        linhas.extend(lote)
        cursor = lote[-1][0] + 86_400_000
        if len(lote) < LIMITE:
            break
    return linhas


def tratar(bruto: list[list], fonte: str = "binance") -> pd.DataFrame:
    """Formato padrão de preços, com as colunas de comportamento."""
    if not bruto:
        return pd.DataFrame(columns=COLUNAS_SAIDA)
    df = pd.DataFrame([linha[: len(COLUNAS_KLINE)] for linha in bruto],
                      columns=COLUNAS_KLINE[: len(bruto[0])])
    df["data"] = pd.to_datetime(df["abertura_ms"], unit="ms", utc=True).dt.date
    for c in COLUNAS_SAIDA[2:]:
        df[c] = pd.to_numeric(df[c], errors="coerce") if c in df else float("nan")
    df["fonte"] = fonte
    return df[COLUNAS_SAIDA]
