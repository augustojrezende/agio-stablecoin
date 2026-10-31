"""Mercado Bitcoin: candles diários do par USDT-BRL pela API pública v4.

O endpoint de candles devolve colunas paralelas: {"t": [...], "o": [...],
"h": [...], "l": [...], "c": [...], "v": [...]}. Confira a documentação
oficial se a corretora mudar o formato.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

import pandas as pd

from agio.http import get_json

CANDLES_URL = "https://api.mercadobitcoin.net/api/v4/candles"
JANELA_DIAS = 300  # consultas em blocos para não estourar limites da API


def _s(d: date) -> int:
    return int(datetime(d.year, d.month, d.day, tzinfo=timezone.utc).timestamp())


def baixar(simbolo: str, inicio: date, fim: date) -> list[dict]:
    lotes: list[dict] = []
    atual = inicio
    while atual <= fim:
        bloco_fim = min(fim, atual + timedelta(days=JANELA_DIAS - 1))
        lote = get_json(
            CANDLES_URL,
            {"symbol": simbolo, "resolution": "1d",
             "from": _s(atual), "to": _s(bloco_fim + timedelta(days=1)) - 1},
        )
        if lote:
            lotes.append(lote)
        atual = bloco_fim + timedelta(days=1)
    return lotes


def tratar(bruto: list[dict], fonte: str = "mercadobitcoin") -> pd.DataFrame:
    colunas = ["data", "fonte", "abertura", "maxima", "minima", "fechamento", "volume_base"]
    partes = []
    for lote in bruto:
        if not lote.get("t"):
            continue
        partes.append(pd.DataFrame({
            "t": lote["t"], "abertura": lote["o"], "maxima": lote["h"],
            "minima": lote["l"], "fechamento": lote["c"], "volume_base": lote["v"],
        }))
    if not partes:
        return pd.DataFrame(columns=colunas)
    df = pd.concat(partes, ignore_index=True)
    df["data"] = pd.to_datetime(pd.to_numeric(df["t"]), unit="s", utc=True).dt.date
    for c in ["abertura", "maxima", "minima", "fechamento", "volume_base"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["fonte"] = fonte
    return df.drop_duplicates("data", keep="last")[colunas].sort_values("data").reset_index(drop=True)
