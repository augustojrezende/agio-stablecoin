"""Testes sem rede: controles (Tesouro e FRED) e análise formal."""

from datetime import date

import numpy as np
import pandas as pd
import pytest

from agio.analise import estudo_evento, montar_base, regressao
from agio.fontes import fred, tesouro

CSV_TESOURO = """Tipo Titulo;Data Vencimento;Data Base;Taxa Compra Manha;Taxa Venda Manha;PU Compra Manha;PU Venda Manha;PU Base Manha
Tesouro IPCA+;15/05/2031;02/01/2026;7,00;7,12;1000,00;990,00;990,00
Tesouro IPCA+;15/05/2041;02/01/2026;8,00;8,12;500,00;490,00;490,00
Tesouro Selic;01/03/2029;02/01/2026;0,10;0,12;15000,00;14990,00;14990,00
Tesouro IPCA+ com Juros Semestrais;15/05/2035;02/01/2026;7,50;7,62;4000,00;3990,00;3990,00
"""


def test_tesouro_interpola_10_anos():
    titulos = tesouro.tratar(CSV_TESOURO)
    assert len(titulos) == 4
    juro = tesouro.juro_real_10a(titulos)
    assert len(juro) == 1
    # prazos de ~5,4 e ~15,4 anos; 10 anos fica perto do meio
    assert 7.3 < juro.loc[0, "juro_real_10a"] < 7.7


def test_fred_aceita_ponto_como_vazio():
    texto = "observation_date,VIXCLS\n2026-10-23,18.5\n2026-10-26,.\n2026-10-27,22.1\n"
    vix = fred.tratar(texto)
    assert list(vix["vix"]) == [18.5, 22.1]


def _base_sintetica(n=300, semente=1):
    rng = np.random.default_rng(semente)
    datas = pd.bdate_range("2024-01-01", periods=n)
    juro_bp = rng.normal(0, 5, n)
    agio = 0.5 + 0.05 * juro_bp + rng.normal(0, 0.2, n)  # efeito verdadeiro: 0,05
    ptax = 5 * np.exp(np.cumsum(rng.normal(0, 0.005, n)))
    agio_diario = pd.DataFrame({"data": datas.date, "agio_pct": agio})
    painel = pd.DataFrame({"data": datas.date, "num_negocios": rng.integers(40_000, 60_000, n),
                           "ticket_medio_brl": rng.uniform(5_000, 9_000, n)})
    ptax_df = pd.DataFrame({"data": datas.date, "ptax_venda": ptax})
    precos = pd.DataFrame({"data": datas.date, "fonte": "binance",
                           "volume_base": rng.uniform(1e7, 2e7, n)})
    juro = pd.DataFrame({"data": datas.date, "juro_real_10a": 7 + np.cumsum(juro_bp) / 100})
    vix = pd.DataFrame({"data": datas.date, "vix": 20 + rng.normal(0, 1, n)})
    return montar_base(agio_diario, painel, ptax_df, precos, juro, vix)


def test_montar_base_tem_variaveis_do_teste():
    base = _base_sintetica()
    for c in ["agio_anormal", "d_dolar", "d_juro_bp", "d_vix", "log_mercado",
              "negocios_anormal", "ticket_anormal"]:
        assert c in base
    assert base["agio_anormal"].iloc[:30].isna().all()  # precisa de histórico


def test_regressao_recupera_efeito_do_juro():
    base = _base_sintetica()
    base["agio_anormal"] = base["agio_pct"] - 0.5  # remove o normal para o teste
    _, tabela = regressao(base)
    linha = tabela.set_index("variavel").loc["d_juro_bp"]
    assert linha["coeficiente"] == pytest.approx(0.05, abs=0.01)
    assert linha["p_valor"] < 0.01


def test_estudo_evento_detecta_choque():
    base = _base_sintetica(semente=2)
    base["agio_anormal"] = 0.0
    datas = base["data"]
    eventos = pd.DataFrame({
        "data": [datas.iloc[100], datas.iloc[150], datas.iloc[200], datas.iloc[250]],
        "tipo": ["fiscal", "fiscal", "externo", "externo"],
        "descricao": ["a", "b", "c", "d"],
    })
    for i in [100, 150]:
        base.loc[i, "agio_anormal"] = 2.0  # choque fiscal no dia do evento
    por_evento, grupos, comp = estudo_evento(base, eventos, n_perm=500)
    g = grupos.set_index("tipo")
    assert g.loc["fiscal", "car_medio"] == pytest.approx(2.0)
    assert g.loc["fiscal", "p_valor_permutacao"] < 0.05
    assert g.loc["externo", "car_medio"] == pytest.approx(0.0)
    assert comp["diferenca"] == pytest.approx(2.0)


def test_evento_em_fim_de_semana_vai_para_o_dia_util_seguinte():
    base = _base_sintetica()
    sabado = date(2024, 6, 1)
    ev = pd.DataFrame({"data": [sabado], "tipo": ["politico"], "descricao": ["x"]})
    por_evento, _, _ = estudo_evento(base, ev, n_perm=10)
    assert por_evento.loc[0, "data"] == pd.Timestamp(sabado)


def test_cboe_vix():
    texto = "DATE,OPEN,HIGH,LOW,CLOSE\n10/23/2026,18.0,19.0,17.5,18.5\n10/26/2026,20.0,24.0,19.8,22.1\n"
    vix = fred.tratar_cboe(texto)
    assert vix.loc[1, "data"] == date(2026, 10, 26)
    assert vix.loc[1, "vix"] == 22.1


def test_winsorizar_corta_extremos():
    from agio.analise import winsorizar
    base = pd.DataFrame({"agio_anormal": list(range(99)) + [1000.0]})
    w = winsorizar(base, ["agio_anormal", "nao_existe"])
    assert w["agio_anormal"].max() < 200
    assert base["agio_anormal"].max() == 1000.0  # original intacto


def test_huber_resiste_a_dia_extremo():
    from agio.analise import resumo_especificacao
    base = _base_sintetica()
    base["agio_anormal"] = base["agio_pct"] - 0.5
    base.loc[200, "agio_anormal"] = 50.0  # um dia absurdo
    linha = resumo_especificacao("huber", base, metodo="huber")
    assert linha["d_juro_bp_coef"] == pytest.approx(0.05, abs=0.01)
    assert linha["n"] > 250


def test_periodo_recorta_depois_do_anormal():
    from agio.analise import periodo
    base = _base_sintetica()
    corte = base["data"].iloc[150]
    antes, depois = periodo(base, fim=corte), periodo(base, inicio=corte)
    assert len(antes) + len(depois) == len(base)
    assert depois["agio_anormal"].notna().all()  # o histórico de antes foi usado


def test_comando_robustez_ponta_a_ponta(tmp_path, monkeypatch):
    from agio import armazenamento as arm
    from agio import cli

    rng = np.random.default_rng(3)
    datas = pd.bdate_range("2025-01-01", "2026-10-30")
    n = len(datas)
    dias = datas.date
    ptax = pd.DataFrame({"data": dias, "ptax_venda": 5 + rng.normal(0, 0.01, n).cumsum()})
    agio = pd.DataFrame({"data": dias, "agio_pct": rng.normal(0.3, 0.2, n)})
    por_fonte = pd.concat([agio.assign(fonte="binance"), agio.assign(fonte="mercadobitcoin")])
    tabelas = {
        "ptax": ptax,
        "painel_diario": pd.DataFrame({"data": dias, "num_negocios": rng.integers(4e4, 6e4, n),
                                       "ticket_medio_brl": rng.uniform(5e3, 9e3, n)}),
        "precos_usdt_brl": pd.DataFrame({"data": dias, "fonte": "binance",
                                         "volume_base": rng.uniform(1e7, 2e7, n)}),
        "juro_real_10a": pd.DataFrame({"data": dias, "juro_real_10a": 7 + rng.normal(0, .05, n).cumsum()}),
        "vix": pd.DataFrame({"data": dias, "vix": 20 + rng.normal(0, 1, n)}),
        "agio_diario": agio, "agio_fechamento_diario": agio, "agio_por_fonte": por_fonte,
    }
    monkeypatch.setattr(arm, "ler_tratado", lambda nome: tabelas[nome].copy())
    monkeypatch.setattr(arm, "BRUTO", tmp_path / "bruto")
    monkeypatch.setattr(cli, "PASTA_RESULTADOS", tmp_path / "resultados")
    cli.robustez()
    saida = pd.read_csv(tmp_path / "resultados" / "robustez.csv")
    assert len(saida) == 8  # 1-4, duas corretoras, antes e depois (sem bruto horário)
    assert {"d_juro_bp_coef", "d_vix_p"} <= set(saida.columns)


def test_estudo_evento_agrupa_por_agendado():
    base = _base_sintetica(semente=4)
    datas = base["data"]
    eventos = pd.DataFrame({
        "data": [datas.iloc[i] for i in (60, 100, 140, 180, 220)],
        "tipo": ["fiscal", "externo", "fiscal", "externo", "monetario"],
        "descricao": list("abcde"),
        "agendado": ["sim", "nao", "nao", "sim", "sim"],
    })
    _, grupos, _ = estudo_evento(base, eventos, n_perm=100)
    g = grupos.set_index("tipo")
    assert g.loc["agendado=sim", "n"] == 3 and g.loc["agendado=nao", "n"] == 2
    assert grupos.attrs["n_placebo"] > 100


def test_lista_de_eventos_segue_a_regra():
    import importlib.util
    from pathlib import Path
    caminho = Path(__file__).resolve().parents[1] / "scripts" / "montar_eventos.py"
    spec = importlib.util.spec_from_file_location("montar_eventos", caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    ev = mod.montar()
    gravado = pd.read_csv(caminho.parents[1] / "dados" / "manual" / "eventos.csv")
    assert len(ev) == len(gravado)  # o CSV foi gerado pelo script, não editado à mão
    assert (ev["fonte"].str.len() > 0).all()
    assert not ev["fonte"].str.contains("A CONFIRMAR").any()
    copom = ev[ev["descricao"] == "Decisão do Copom"]
    assert (pd.to_datetime(copom["data"]) > pd.to_datetime(copom["data_anuncio"])).all()


def _tabelas_sinteticas(n_dias_inicio="2024-01-01", fim="2026-10-30", semente=5):
    rng = np.random.default_rng(semente)
    datas = pd.bdate_range(n_dias_inicio, fim)
    n = len(datas)
    dias = datas.date
    ptax = 5 * np.exp(np.cumsum(rng.normal(0, 0.006, n)))
    d_dolar = np.r_[0, 100 * np.diff(np.log(ptax))]
    agio = 0.3 - 0.13 * d_dolar + rng.normal(0, 0.2, n)
    agio_df = pd.DataFrame({"data": dias, "agio_pct": agio})
    return {
        "ptax": pd.DataFrame({"data": dias, "ptax_venda": ptax}),
        "painel_diario": pd.DataFrame({"data": dias, "agio_pct": agio,
                                       "agio_fechamento_pct": agio + rng.normal(0, .2, n),
                                       "num_negocios": rng.integers(4e4, 6e4, n),
                                       "ticket_medio_brl": rng.uniform(5e3, 9e3, n)}),
        "precos_usdt_brl": pd.DataFrame({"data": dias, "fonte": "binance",
                                         "volume_base": rng.uniform(1e7, 2e7, n)}),
        "juro_real_10a": pd.DataFrame({"data": dias, "juro_real_10a": 7 + rng.normal(0, .05, n).cumsum()}),
        "vix": pd.DataFrame({"data": dias, "vix": 20 + rng.normal(0, 1, n)}),
        "agio_diario": agio_df, "agio_fechamento_diario": agio_df,
        "agio_por_fonte": pd.concat([agio_df.assign(fonte="binance"),
                                     agio_df.assign(fonte="mercadobitcoin")]),
    }


def test_regressao_repasse_mede_volta_do_agio():
    from agio.analise import regressao_repasse
    rng = np.random.default_rng(7)
    n = 800
    datas = pd.bdate_range("2023-01-02", periods=n)
    d = rng.normal(0, 1, n)
    y = -0.13 * d + 0.05 * np.r_[0, d[:-1]] + 0.04 * np.r_[0, 0, d[:-2]] + rng.normal(0, .1, n)
    base = pd.DataFrame({"data": datas, "d_dolar": d, "agio_anormal": y})
    _, tabela, soma = regressao_repasse(base)
    t = tabela.set_index("variavel")
    assert t.loc["d_dolar", "coeficiente"] == pytest.approx(-0.13, abs=0.02)
    assert soma["soma_defasagens"] == pytest.approx(0.09, abs=0.03)
    assert soma["p_valor"] < 0.01


def test_testar_por_periodo_e_relatorio(tmp_path, monkeypatch):
    from agio import armazenamento as arm
    from agio import cli, relatorio

    tabelas = _tabelas_sinteticas()
    tratado = tmp_path / "tratado"
    tratado.mkdir()
    for nome, df in tabelas.items():
        df.to_csv(tratado / f"{nome}.csv", index=False)
    resultados = tmp_path / "resultados"
    monkeypatch.setattr(arm, "ler_tratado", lambda nome: tabelas[nome].copy())
    monkeypatch.setattr(arm, "TRATADO", tratado)
    monkeypatch.setattr(arm, "BRUTO", tmp_path / "bruto")
    monkeypatch.setattr(cli, "PASTA_RESULTADOS", resultados)
    monkeypatch.setattr(relatorio, "RESULTADOS", resultados)
    monkeypatch.setattr(relatorio, "DOCS", tmp_path / "docs")
    monkeypatch.setattr(relatorio, "FIGURAS", tmp_path / "docs" / "figuras")
    (tmp_path / "docs").mkdir()

    cli.testar(inicio=date(2026, 1, 1))
    validacao = resultados / "periodo_2026-01-01_fim"
    base = pd.read_csv(validacao / "base_teste.csv", parse_dates=["data"])
    assert base["data"].min() >= pd.Timestamp("2026-01-01")
    assert (validacao / "regressao_repasse_soma.csv").exists()
    hip = pd.read_csv(validacao / "hipoteses.csv")
    assert {"V1", "V3", "V4a", "V4b"} <= set(hip["hipotese"])

    cli.testar()
    cli.robustez()
    relatorio.gerar()
    figuras = sorted(p.name for p in (tmp_path / "docs" / "figuras").glob("*.png"))
    assert len(figuras) == 8
    texto = (tmp_path / "docs" / "resultados_tabelas.md").read_text(encoding="utf-8")
    assert "Repasse do câmbio" in texto and "figuras/08_robustez.png" in texto


def test_holm():
    from agio.analise import holm
    assert holm([0.01, 0.04, 0.03]) == pytest.approx([0.03, 0.06, 0.06])


def test_episodio_compara_corretoras_e_horarios(tmp_path, monkeypatch):
    from agio import armazenamento as arm
    from agio import episodio

    rng = np.random.default_rng(9)
    datas = pd.bdate_range("2026-01-02", "2026-08-31").date
    n = len(datas)
    ptax = pd.DataFrame({"data": datas, "ptax_venda": 5 + rng.normal(0, .01, n).cumsum()})
    agio = rng.normal(0.3, 0.1, n)
    agio[(pd.to_datetime(datas) >= "2026-06-24") & (pd.to_datetime(datas) < "2026-07-20")] += 1.0
    por_fonte = pd.concat([
        pd.DataFrame({"data": datas, "fonte": f, "agio_pct": agio, "preco_janela": 5.0})
        for f in ("binance", "mercadobitcoin")])
    tabelas = {"ptax": ptax, "agio_por_fonte": por_fonte, "agio_fechamento_por_fonte": por_fonte,
               "agio_diario": pd.DataFrame({"data": datas, "agio_pct": agio}),
               "precos_janela_ptax": por_fonte.assign(horas_janela=3, volume_janela=1e6),
               "sinais_comportamento": pd.DataFrame({
                   "data": datas, "fonte": "binance", "num_negocios": 50_000,
                   "pressao_compradora": 0.5, "ticket_medio_brl": 6_000.0})}
    monkeypatch.setattr(arm, "ler_tratado", lambda nome: tabelas[nome].copy())
    monkeypatch.setattr(episodio, "RESULTADOS", tmp_path / "res")
    monkeypatch.setattr(episodio, "FIGURAS", tmp_path / "fig")
    base = episodio.montar(date(2026, 6, 24), date(2026, 7, 20))
    durante = base[base["no_episodio"]]
    assert durante["agio_janela_binance"].mean() > 1.0
    assert (~base["no_episodio"]).sum() > 50  # 90 dias de contexto
    assert "Correlação entre corretoras" in episodio.resumo(base)
    episodio.rodar(date(2026, 6, 24), date(2026, 7, 20))
    assert (tmp_path / "fig" / "episodio_20260624_20260720.png").exists()
