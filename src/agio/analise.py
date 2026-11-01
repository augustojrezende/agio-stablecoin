"""Teste formal do TCC: regressão com todos os dias e estudo de evento.

Regra de decisão (definida antes de rodar; ver docs/decisoes.md):

- Hipótese original confirmada: coeficiente do juro real positivo e
  significativo a 5%, e choques domésticos com ágio anormal maior que os
  externos.
- Hipótese comportamental confirmada: participação (número de negócios)
  significativamente maior nas crises.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

JANELA_NORMAL = 60          # dias úteis usados para definir o "normal"
MINIMO_NORMAL = 30
JANELA_EVENTO = (-1, 3)     # do dia anterior até 3 dias úteis depois
# Datas placebo não podem ter a janela (-1 a +3) cruzando a janela de um evento:
# ficam de fora as posições a até 4 dias úteis de qualquer evento. (Era 10 com
# 15 eventos; com a lista fechada, ~150 eventos, 10 esgotaria o sorteio.)
EXCLUSAO_PLACEBO = 4
DOMESTICOS = {"fiscal", "politico"}
EXTERNOS = {"externo"}


def _anormal(serie: pd.Series) -> pd.Series:
    """Valor do dia menos a mediana dos 60 dias úteis anteriores."""
    normal = serie.shift(1).rolling(JANELA_NORMAL, min_periods=MINIMO_NORMAL).median()
    return serie - normal


def montar_base(agio_diario: pd.DataFrame, painel: pd.DataFrame, ptax: pd.DataFrame,
                precos: pd.DataFrame, juro: pd.DataFrame | None = None,
                vix: pd.DataFrame | None = None) -> pd.DataFrame:
    """Uma linha por dia útil com todas as variáveis do teste."""
    base = agio_diario[["data", "agio_pct"]].copy()
    base["data"] = pd.to_datetime(base["data"])
    base = base.sort_values("data").reset_index(drop=True)
    base["agio_anormal"] = _anormal(base["agio_pct"])

    px = ptax[["data", "ptax_venda"]].assign(data=lambda d: pd.to_datetime(d["data"]))
    base = base.merge(px, on="data", how="left")
    base["d_dolar"] = 100 * np.log(base["ptax_venda"] / base["ptax_venda"].shift(1))

    vol = (precos.assign(data=lambda d: pd.to_datetime(d["data"]))
           .groupby("data")["volume_base"].sum().rename("volume").reset_index())
    base = base.merge(vol, on="data", how="left")
    base["log_mercado"] = np.log(base["volume"].shift(1).rolling(JANELA_NORMAL,
                                 min_periods=MINIMO_NORMAL).median())

    comp = painel[["data", "num_negocios", "ticket_medio_brl"]].assign(
        data=lambda d: pd.to_datetime(d["data"]))
    base = base.merge(comp, on="data", how="left")
    base["negocios_anormal"] = _anormal(np.log(base["num_negocios"]))
    base["ticket_anormal"] = _anormal(np.log(base["ticket_medio_brl"]))

    if juro is not None and not juro.empty:
        j = juro.assign(data=lambda d: pd.to_datetime(d["data"])).sort_values("data")
        base = pd.merge_asof(base, j, on="data")
        base["d_juro_bp"] = 100 * base["juro_real_10a"].diff()
    if vix is not None and not vix.empty:
        v = vix.assign(data=lambda d: pd.to_datetime(d["data"])).sort_values("data")
        base = pd.merge_asof(base, v, on="data")
        base["d_vix"] = base["vix"].diff()
        base["d_vix_ant"] = base["d_vix"].shift(1)
    return base


def regressao(base: pd.DataFrame, y: str = "agio_anormal", lags_hac: int = 5):
    """OLS com erros padrão de Newey-West. Usa os controles disponíveis."""
    candidatos = ["d_dolar", "d_juro_bp", "d_vix", "d_vix_ant", "log_mercado"]
    x = [c for c in candidatos if c in base and base[c].notna().any()]
    dados = base[[y] + x].replace([np.inf, -np.inf], np.nan).dropna()
    formula = f"{y} ~ " + " + ".join(x)
    modelo = smf.ols(formula, data=dados).fit(cov_type="HAC", cov_kwds={"maxlags": lags_hac})
    tabela = pd.DataFrame({
        "coeficiente": modelo.params, "erro_padrao": modelo.bse,
        "t": modelo.tvalues, "p_valor": modelo.pvalues,
    })
    tabela.index.name = "variavel"
    return modelo, tabela.reset_index()


def ajustar_pelo_dolar(base: pd.DataFrame, y: str = "agio_anormal") -> pd.Series:
    """Parte de y que a variação do dólar oficial no dia não explica.

    Os dados mostram que, quando o dólar oficial dispara, o ágio cai quase
    mecanicamente. O estudo de evento usa este resíduo para não confundir
    esse efeito com a reação ao medo fiscal.
    """
    dados = base[[y, "d_dolar"]].replace([np.inf, -np.inf], np.nan).dropna()
    modelo = smf.ols(f"{y} ~ d_dolar", data=dados).fit()
    ajustado = pd.Series(np.nan, index=base.index)
    ajustado.loc[dados.index] = modelo.resid
    return ajustado


def _posicoes_eventos(base: pd.DataFrame, eventos: pd.DataFrame) -> pd.DataFrame:
    """Leva cada evento ao primeiro dia útil da base na data ou depois dela."""
    datas = base["data"].to_numpy()
    ev = eventos.copy()
    ev["data"] = pd.to_datetime(ev["data"])
    ev["pos"] = np.searchsorted(datas, ev["data"].to_numpy())
    return ev[ev["pos"] < len(base)].reset_index(drop=True)


def _car(valores: np.ndarray, pos: int) -> float:
    ini, fim = pos + JANELA_EVENTO[0], pos + JANELA_EVENTO[1]
    if ini < 0 or fim >= len(valores):
        return np.nan
    janela = valores[ini:fim + 1]
    return np.nan if np.isnan(janela).any() else float(janela.sum())


def estudo_evento(base: pd.DataFrame, eventos: pd.DataFrame, coluna: str = "agio_anormal",
                  n_perm: int = 5000, semente: int = 42):
    """CAR por evento, estatística por grupo e teste de permutação.

    Permutação: sorteia datas fora de ±10 dias úteis de qualquer evento e
    compara a média dos CAR sorteados com a média observada do grupo.
    """
    valores = base[coluna].to_numpy(dtype=float)
    ev = _posicoes_eventos(base, eventos)
    ev["car"] = [_car(valores, p) for p in ev["pos"]]
    ev = ev.dropna(subset=["car"])

    proibidas = set()
    for p in ev["pos"]:
        proibidas.update(range(p - EXCLUSAO_PLACEBO, p + EXCLUSAO_PLACEBO + 1))
    candidatas = np.array([p for p in range(len(valores))
                           if p not in proibidas and not np.isnan(_car(valores, p))])
    car_placebo = np.array([_car(valores, p) for p in candidatas])
    rng = np.random.default_rng(semente)

    linhas = []
    grupos_teste = [(tipo, g) for tipo, g in ev.groupby("tipo")] + [("todos", ev)]
    if "agendado" in ev:
        grupos_teste += [(f"agendado={v}", g) for v, g in ev.groupby("agendado")]
    for tipo, g in grupos_teste:
        n, media = len(g), g["car"].mean()
        t, p_t = (stats.ttest_1samp(g["car"], 0.0) if n > 1 else (np.nan, np.nan))
        sorteios = rng.choice(car_placebo, size=(n_perm, n), replace=True).mean(axis=1)
        p_perm = float((np.abs(sorteios - car_placebo.mean())
                        >= abs(media - car_placebo.mean())).mean())
        linhas.append({"tipo": tipo, "n": n, "car_medio": media, "t": t,
                       "p_valor_t": p_t, "p_valor_permutacao": p_perm})
    grupos = pd.DataFrame(linhas)
    grupos.attrs["n_placebo"] = len(car_placebo)

    dom = ev[ev["tipo"].isin(DOMESTICOS)]["car"].to_numpy()
    ext = ev[ev["tipo"].isin(EXTERNOS)]["car"].to_numpy()
    comparacao = None
    if len(dom) and len(ext):
        dif = dom.mean() - ext.mean()
        juntos = np.concatenate([dom, ext])
        difs = []
        for _ in range(n_perm):
            rng.shuffle(juntos)
            difs.append(juntos[:len(dom)].mean() - juntos[len(dom):].mean())
        comparacao = {"car_domesticos": dom.mean(), "car_externos": ext.mean(),
                      "diferenca": dif,
                      "p_valor_permutacao": float((np.abs(difs) >= abs(dif)).mean())}
    return ev[["data", "tipo", "descricao", "car"]], grupos, comparacao


# --- Testes de robustez ----------------------------------------------------

CONTROLES = ["d_dolar", "d_juro_bp", "d_vix", "d_vix_ant", "log_mercado"]
VARIAVEIS_CHAVE = ["d_juro_bp", "d_vix", "d_vix_ant", "d_dolar"]


def winsorizar(base: pd.DataFrame, colunas: list[str], limite: float = 0.01) -> pd.DataFrame:
    """Corta cada coluna nos percentis 1% e 99%: os dias extremos ficam, mas pesam menos."""
    saida = base.copy()
    for c in colunas:
        if c in saida:
            baixo, alto = saida[c].quantile([limite, 1 - limite])
            saida[c] = saida[c].clip(baixo, alto)
    return saida


def regressao_huber(base: pd.DataFrame, y: str = "agio_anormal"):
    """Regressão robusta (Huber): reduz automaticamente o peso dos dias atípicos.

    Não tem correção de Newey-West; serve para checar se o sinal e o tamanho
    dos coeficientes dependem de poucos dias extremos.
    """
    import statsmodels.api as sm

    x = [c for c in CONTROLES if c in base and base[c].notna().any()]
    dados = base[[y] + x].replace([np.inf, -np.inf], np.nan).dropna()
    modelo = smf.rlm(f"{y} ~ " + " + ".join(x), data=dados,
                     M=sm.robust.norms.HuberT()).fit()
    tabela = pd.DataFrame({"coeficiente": modelo.params, "erro_padrao": modelo.bse,
                           "t": modelo.tvalues, "p_valor": modelo.pvalues})
    tabela.index.name = "variavel"
    return modelo, tabela.reset_index()


def resumo_especificacao(nome: str, base: pd.DataFrame, metodo: str = "ols",
                         y: str = "agio_anormal") -> dict:
    """Uma linha com n e coeficiente/p-valor das variáveis-chave."""
    if metodo == "huber":
        modelo, tabela = regressao_huber(base, y)
    else:
        modelo, tabela = regressao(base, y)
    linha = {"especificacao": nome, "n": int(modelo.nobs)}
    t = tabela.set_index("variavel")
    for v in VARIAVEIS_CHAVE:
        if v in t.index:
            linha[f"{v}_coef"] = t.loc[v, "coeficiente"]
            linha[f"{v}_p"] = t.loc[v, "p_valor"]
    return linha


def periodo(base: pd.DataFrame, inicio=None, fim=None) -> pd.DataFrame:
    """Recorte de datas feito depois de calcular o anormal, que usa o histórico."""
    dados = base
    if inicio is not None:
        dados = dados[dados["data"] >= pd.Timestamp(inicio)]
    if fim is not None:
        dados = dados[dados["data"] < pd.Timestamp(fim)]
    return dados
