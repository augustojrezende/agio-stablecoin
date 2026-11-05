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


JANELA_DIAS_HORARIO = 30  # 720 candles por consulta


def baixar(simbolo: str, inicio: date, fim: date, resolucao: str = "1d") -> list[dict]:
    """Candles entre inicio e fim. resolucao: "1d" (diário) ou "1h" (horário)."""
    janela = JANELA_DIAS if resolucao == "1d" else JANELA_DIAS_HORARIO
    lotes: list[dict] = []
    atual = inicio
    while atual <= fim:
        bloco_fim = min(fim, atual + timedelta(days=janela - 1))
        lote = get_json(
            CANDLES_URL,
            {"symbol": simbolo, "resolution": resolucao,
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


def tratar_horario(bruto: list[dict], fonte: str = "mercadobitcoin") -> pd.DataFrame:
    """Candles horários: inicio_utc, fonte, maxima, minima, fechamento, volume_base."""
    colunas = ["inicio_utc", "fonte", "maxima", "minima", "fechamento", "volume_base"]
    partes = [
        pd.DataFrame({"t": lote["t"], "maxima": lote["h"], "minima": lote["l"],
                      "fechamento": lote["c"], "volume_base": lote["v"]})
        for lote in bruto if lote.get("t")
    ]
    if not partes:
        return pd.DataFrame(columns=colunas)
    df = pd.concat(partes, ignore_index=True)
    df["inicio_utc"] = pd.to_datetime(pd.to_numeric(df["t"]), unit="s", utc=True)
    for c in ["maxima", "minima", "fechamento", "volume_base"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["fonte"] = fonte
    return (df.drop_duplicates("inicio_utc", keep="last")[colunas]
            .sort_values("inicio_utc").reset_index(drop=True))
