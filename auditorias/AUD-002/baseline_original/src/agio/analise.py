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

    buscas = [c for c in painel.columns if c.startswith("busca_")]
    comp = painel[["data", "num_negocios", "ticket_medio_brl"] + buscas].assign(
        data=lambda d: pd.to_datetime(d["data"]))
    base = base.merge(comp, on="data", how="left")
    base["negocios_anormal"] = _anormal(np.log(base["num_negocios"]))
    base["ticket_anormal"] = _anormal(np.log(base["ticket_medio_brl"]))
    for c in buscas:  # atenção do público (Google Trends), em log
        nome = "busca_" + c[len("busca_"):].replace("ó", "o") + "_anormal"
        base[nome] = _anormal(np.log1p(base[c]))

    if juro is not None and not juro.empty:
        j = juro.assign(data=lambda d: pd.to_datetime(d["data"]).astype("datetime64[ns]"))
        base = pd.merge_asof(base.assign(data=base["data"].astype("datetime64[ns]")),
                             j.sort_values("data"), on="data")
        base["d_juro_bp"] = 100 * base["juro_real_10a"].diff()
    if vix is not None and not vix.empty:
        v = vix.assign(data=lambda d: pd.to_datetime(d["data"]).astype("datetime64[ns]"))
        base = pd.merge_asof(base.assign(data=base["data"].astype("datetime64[ns]")),
                             v.sort_values("data"), on="data")
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
    grupos.attrs["placebo_media"] = float(car_placebo.mean())

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
            linha[f"{v}_ep"] = t.loc[v, "erro_padrao"]
    return linha


def periodo(base: pd.DataFrame, inicio=None, fim=None) -> pd.DataFrame:
    """Recorte de datas feito depois de calcular o anormal, que usa o histórico."""
    dados = base
    if inicio is not None:
        dados = dados[dados["data"] >= pd.Timestamp(inicio)]
    if fim is not None:
        dados = dados[dados["data"] < pd.Timestamp(fim)]
    return dados


# --- Repasse do câmbio e trajetória em torno dos eventos -------------------

def regressao_repasse(base: pd.DataFrame, y: str = "agio_anormal", defasagens: int = 3,
                      lags_hac: int = 5):
    """Ágio anormal sobre a variação do dólar no dia e nos dias anteriores.

    Pergunta (pré-registrada para a amostra de validação; ver
    docs/pre-registro.md): o ágio cai quando o dólar oficial sobe (repasse
    incompleto ao USDT) e volta nos dias seguintes (o repasse se completa
    com atraso)? Devolve (modelo, tabela, teste da soma das defasagens).
    """
    dados = base.copy()
    nomes = []
    for k in range(1, defasagens + 1):
        dados[f"d_dolar_l{k}"] = dados["d_dolar"].shift(k)
        nomes.append(f"d_dolar_l{k}")
    controles = [c for c in ["d_juro_bp", "d_vix", "d_vix_ant", "log_mercado"]
                 if c in dados and dados[c].notna().any()]
    x = ["d_dolar"] + nomes + controles
    dados = dados[[y] + x].replace([np.inf, -np.inf], np.nan).dropna()
    modelo = smf.ols(f"{y} ~ " + " + ".join(x), data=dados).fit(
        cov_type="HAC", cov_kwds={"maxlags": lags_hac})
    tabela = pd.DataFrame({"coeficiente": modelo.params, "erro_padrao": modelo.bse,
                           "t": modelo.tvalues, "p_valor": modelo.pvalues})
    tabela.index.name = "variavel"
    teste = modelo.t_test(" + ".join(nomes) + " = 0")
    soma = {"soma_defasagens": float(np.squeeze(teste.effect)),
            "erro_padrao": float(np.squeeze(teste.sd)),
            "p_valor": float(np.squeeze(teste.pvalue))}
    return modelo, tabela.reset_index(), soma


def trajetoria_evento(base: pd.DataFrame, eventos: pd.DataFrame, coluna: str,
                      antes: int = 5, depois: int = 10, n_sorteios: int = 2000,
                      semente: int = 42) -> pd.DataFrame:
    """Média da variável em cada dia relativo ao evento, com faixa placebo.

    A faixa placebo (percentis 2,5 e 97,5) vem de médias de datas sorteadas
    fora dos eventos, com o mesmo número de datas do grupo. Serve aos
    gráficos; o teste formal continua sendo estudo_evento.
    """
    valores = base[coluna].to_numpy(dtype=float)
    ev = _posicoes_eventos(base, eventos)
    rel = np.arange(-antes, depois + 1)
    validas = [p for p in ev["pos"] if p - antes >= 0 and p + depois < len(valores)]
    matriz = np.array([valores[p + rel] for p in validas])
    proibidas = set()
    for p in ev["pos"]:
        proibidas.update(range(p - antes - EXCLUSAO_PLACEBO, p + depois + EXCLUSAO_PLACEBO + 1))
    candidatas = np.array([p for p in range(antes, len(valores) - depois) if p not in proibidas])
    rng = np.random.default_rng(semente)
    n = max(len(validas), 1)
    medias = np.array([np.nanmean(valores[rng.choice(candidatas, n)[:, None] + rel], axis=0)
                       for _ in range(n_sorteios)])
    return pd.DataFrame({
        "dia": rel, "media": np.nanmean(matriz, axis=0) if len(validas) else np.nan,
        "placebo_media": medias.mean(axis=0),
        "placebo_p025": np.percentile(medias, 2.5, axis=0),
        "placebo_p975": np.percentile(medias, 97.5, axis=0),
        "n_eventos": len(validas),
    })


# --- Quadro das hipóteses pré-registradas (docs/pre-registro.md) -----------

def holm(p_valores: list[float]) -> list[float]:
    """P-valores ajustados pelo método de Holm (controle do erro familiar)."""
    p = np.asarray(p_valores, dtype=float)
    ordem = np.argsort(p)
    m = len(p)
    ajustado = np.empty(m)
    acumulado = 0.0
    for posicao, i in enumerate(ordem):
        acumulado = max(acumulado, min(1.0, (m - posicao) * p[i]))
        ajustado[i] = acumulado
    return list(ajustado)


def quadro_hipoteses(reg_agio: pd.DataFrame, soma_repasse: dict,
                     grupos_negocios: pd.DataFrame, comp_agio: dict | None,
                     grupos_ajustado_isolados: pd.DataFrame | None,
                     alfa: float = 0.05) -> pd.DataFrame:
    """V1 a V6 do pré-registro: estimativa, p-valor, Holm e decisão.

    `confirma` usa o p-valor de cada hipótese; `confirma_holm`, o p-valor
    ajustado pelo método de Holm. O pré-registro manda reportar os dois.
    """
    t = reg_agio.set_index("variavel")
    g = grupos_negocios.set_index("tipo")

    def coef(v):
        return (t.loc[v, "coeficiente"], t.loc[v, "p_valor"]) if v in t.index else (np.nan, np.nan)

    linhas = []
    b, p = coef("d_juro_bp")
    dif = comp_agio["diferenca"] if comp_agio else np.nan
    p_dif = comp_agio["p_valor_permutacao"] if comp_agio else np.nan
    linhas.append(("V1", "Estresse fiscal eleva o ágio", f"juro {b:.4f}; dom−ext {dif:.3f}",
                   np.nanmax([p, p_dif]), b > 0 and dif > 0))
    car = g.loc["todos", "car_medio"] if "todos" in g.index else np.nan
    linhas.append(("V2", "Crises elevam a participação", f"CAR negócios {car:.3f}",
                   g.loc["todos", "p_valor_permutacao"] if "todos" in g.index else np.nan,
                   car > g.attrs.get("placebo_media", 0)))
    b, p = coef("d_vix_ant")
    linhas.append(("V3", "Medo global eleva o ágio", f"VIX anterior {b:.4f}", p, b > 0))
    b, p = coef("d_dolar")
    linhas.append(("V4a", "Repasse incompleto no dia", f"dólar {b:.4f}", p, b < 0))
    linhas.append(("V4b", "Repasse se completa depois",
                   f"soma defasagens {soma_repasse['soma_defasagens']:.4f}",
                   soma_repasse["p_valor"], soma_repasse["soma_defasagens"] > 0))
    # V6: adendo de 01/11/2026 ao pré-registro (derivada da descoberta): o ágio
    # continua caindo nos dias seguintes à alta do dólar (realização de ganhos).
    linhas.append(("V6", "Realização de ganhos: ágio segue caindo depois",
                   f"soma defasagens {soma_repasse['soma_defasagens']:.4f}",
                   soma_repasse["p_valor"], soma_repasse["soma_defasagens"] < 0))
    if grupos_ajustado_isolados is not None and "externo" in set(grupos_ajustado_isolados["tipo"]):
        ge = grupos_ajustado_isolados.set_index("tipo")
        car = ge.loc["externo", "car_medio"]
        linhas.append(("V5", "Choques externos isolados reduzem o ágio",
                       f"CAR externos {car:.3f} (n={int(ge.loc['externo', 'n'])})",
                       ge.loc["externo", "p_valor_permutacao"],
                       car < ge.attrs.get("placebo_media", 0)))
    q = pd.DataFrame(linhas, columns=["hipotese", "descricao", "estimativa", "p_valor", "sinal_previsto"])
    q["p_holm"] = holm(q["p_valor"].fillna(1.0).tolist())
    q["confirma"] = np.where(q["sinal_previsto"] & (q["p_valor"] < alfa), "sim", "nao")
    q["confirma_holm"] = np.where(q["sinal_previsto"] & (q["p_holm"] < alfa), "sim", "nao")
    # Pré-registro: menos de 10 eventos = sem poder, resultado inconclusivo.
    n_eventos = {"V2": g.loc["todos", "n"] if "todos" in g.index else 0}
    if grupos_ajustado_isolados is not None and "externo" in set(grupos_ajustado_isolados["tipo"]):
        n_eventos["V5"] = grupos_ajustado_isolados.set_index("tipo").loc["externo", "n"]
    for h, n in n_eventos.items():
        if n < 10:
            q.loc[q["hipotese"] == h, ["confirma", "confirma_holm"]] = "inconclusivo"
    return q


# --- Exploratório: oferta global de USDT (fora do pré-registro) ------------

def regressao_oferta_usdt(base: pd.DataFrame, oferta: pd.DataFrame, dias: int = 5,
                          y: str = "agio_anormal", lags_hac: int = 5):
    """Ágio anormal ~ controles + variação da oferta global de USDT.

    EXPLORATÓRIO. Hipótese surgida no episódio de jun-jul/2026: quando a
    oferta global de USDT encolhe, o USDT fica escasso onde a arbitragem é
    lenta e o ágio sobe (coeficiente negativo esperado). A oferta entra com
    um dia de defasagem (dado diário em UTC, conhecido antes da janela da
    PTAX). Devolve (modelo, tabela, base usada).
    """
    # Mesma unidade de data dos dois lados: versões novas do pandas recusam
    # juntar datas em segundos com datas em microssegundos.
    o = oferta.assign(data=lambda d: pd.to_datetime(d["data"]).astype("datetime64[ns]"))
    o = o.sort_values("data")
    o["var_oferta_usdt"] = 100 * np.log(o["usdt_oferta_bi"] / o["usdt_oferta_bi"].shift(dias))
    o["data"] = o["data"] + pd.Timedelta(days=1)
    esquerda = base.assign(data=pd.to_datetime(base["data"]).astype("datetime64[ns]"))
    dados = pd.merge_asof(esquerda.sort_values("data"), o[["data", "var_oferta_usdt"]], on="data")
    x = [c for c in ["d_dolar", "d_juro_bp", "d_vix", "d_vix_ant", "log_mercado",
                     "var_oferta_usdt"] if c in dados and dados[c].notna().any()]
    usada = dados[[y] + x].replace([np.inf, -np.inf], np.nan).dropna()
    modelo = smf.ols(f"{y} ~ " + " + ".join(x), data=usada).fit(
        cov_type="HAC", cov_kwds={"maxlags": lags_hac})
    tabela = pd.DataFrame({"coeficiente": modelo.params, "erro_padrao": modelo.bse,
                           "t": modelo.tvalues, "p_valor": modelo.pvalues})
    tabela.index.name = "variavel"
    return modelo, tabela.reset_index(), dados


# --- Exploratório: atenção do público (Google Trends) -----------------------

def regressao_atencao(base: pd.DataFrame, y: str = "agio_anormal", lags_hac: int = 5):
    """Ágio anormal ~ controles + buscas anormais do dia anterior.

    EXPLORATÓRIO (fora do pré-registro). Pergunta: a atenção do público ao
    dólar e ao USDT antecipa o ágio? As buscas entram com um dia de atraso
    para não confundir causa e efeito no mesmo dia.
    """
    dados = base.copy()
    novas = []
    for c in [c for c in dados.columns if c.startswith("busca_") and c.endswith("_anormal")]:
        dados[c + "_ant"] = dados[c].shift(1)
        novas.append(c + "_ant")
    x = [c for c in ["d_dolar", "d_juro_bp", "d_vix", "d_vix_ant", "log_mercado"] + novas
         if c in dados and dados[c].notna().any()]
    usada = dados[[y] + x].replace([np.inf, -np.inf], np.nan).dropna()
    modelo = smf.ols(f"{y} ~ " + " + ".join(x), data=usada).fit(
        cov_type="HAC", cov_kwds={"maxlags": lags_hac})
    tabela = pd.DataFrame({"coeficiente": modelo.params, "erro_padrao": modelo.bse,
                           "t": modelo.tvalues, "p_valor": modelo.pvalues})
    tabela.index.name = "variavel"
    return modelo, tabela.reset_index()
