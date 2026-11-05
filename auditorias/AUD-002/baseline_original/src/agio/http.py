"""Cliente HTTP simples com novas tentativas e pausa entre chamadas."""

from __future__ import annotations

import time

import requests

USER_AGENT = "agio-stablecoin/0.1 (pesquisa academica)"


def get_json(url: str, params: dict | None = None, tentativas: int = 4, pausa: float = 1.0):
    """GET que devolve JSON, com backoff exponencial em falhas temporárias."""
    ultimo_erro = None
    for i in range(tentativas):
        try:
            resp = requests.get(
                url, params=params, timeout=30, headers={"User-Agent": USER_AGENT}
            )
            if resp.status_code in (429, 500, 502, 503, 504):
                raise requests.HTTPError(f"HTTP {resp.status_code}", response=resp)
            resp.raise_for_status()
            time.sleep(pausa)  # educação com a API pública
            return resp.json()
        except (requests.RequestException, ValueError) as erro:
            ultimo_erro = erro
            time.sleep(pausa * 2**i)
    raise RuntimeError(f"Falha ao acessar {url}: {ultimo_erro}")
