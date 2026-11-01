"""Oferta global de USDT (DefiLlama, API pública e gratuita, sem chave).

Uso EXPLORATÓRIO: esta variável não está no pré-registro. Surgiu ao
investigar o episódio de ágio alto de jun-jul/2026 (ver docs/decisoes.md),
quando a oferta de stablecoins teve a maior contração mensal desde 2022.

Endpoint: https://stablecoins.llama.fi/stablecoincharts/all?stablecoin=1
(stablecoin=1 é o USDT). Resposta: lista de
{"date": "<unix>", "totalCirculating": {"peggedUSD": ...}, ...}.
"""

from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd

from agio.http import get_json

URL = "https://stablecoins.llama.fi/stablecoincharts/all"
ID_USDT = 1


def baixar(stablecoin: int = ID_USDT) -> list[dict]:
    return get_json(URL, params={"stablecoin": stablecoin})


def tratar(bruto: list[dict], nome: str = "usdt_oferta_bi") -> pd.DataFrame:
    """Uma linha por dia: oferta em circulação, em bilhões de dólares."""
    linhas = []
    for item in bruto:
        total = item.get("totalCirculating") or item.get("totalCirculatingUSD") or {}
        valor = total.get("peggedUSD")
        if valor is None:
            continue
        dia = datetime.fromtimestamp(int(item["date"]), tz=timezone.utc).date()
        linhas.append({"data": dia, nome: float(valor) / 1e9})
    df = pd.DataFrame(linhas, columns=["data", nome])
    return df.drop_duplicates("data", keep="last").sort_values("data").reset_index(drop=True)
