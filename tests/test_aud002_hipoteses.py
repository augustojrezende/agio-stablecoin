"""Políticas aprovadas pelo pesquisador em 02/11/2026, sem alterar pré-registro."""
from pathlib import Path
import importlib.util
import numpy as np
import pandas as pd
import pytest
from statsmodels.stats.multitest import multipletests
from agio import analise as a

ROOT=Path(__file__).resolve().parents[1]


def entradas(n_dom=10,n_ext=10,v5=True):
    reg=pd.DataFrame({'variavel':['d_juro_bp','d_vix_ant','d_dolar'],
                      'coeficiente':[.01,.02,-.1], 'p_valor':[.001,.02,.003]})
    soma={'soma_defasagens':-.1,'p_valor':.004}
    negocios=pd.DataFrame({'tipo':['todos'],'n':[30],'car_medio':[.5],'p_valor_permutacao':[.03]})
    comp={'diferenca':.2,'p_valor_permutacao':.001,'n_domesticos':n_dom,'n_externos':n_ext}
    isolados=pd.DataFrame({'tipo':['externo'],'n':[15],'car_medio':[-.3],'p_valor_permutacao':[.01]}) if v5 else None
    return reg,soma,negocios,comp,isolados


@pytest.mark.parametrize('n_dom,n_ext,elegivel',[(0,0,False),(2,2,False),(9,9,False),(10,10,True),(11,11,True),(9,20,False),(20,9,False),(0,20,False),(20,0,False)])
def test_aud21_minimo_dez_por_grupo(n_dom,n_ext,elegivel):
    q=a.quadro_hipoteses(*entradas(n_dom,n_ext)).set_index('hipotese')
    esperado='sim' if elegivel else 'inconclusivo'
    assert q.loc['V1','confirma']==esperado
    assert q.loc['V1','confirma_holm']==esperado


def test_aud21_grupo_ausente_nao_usa_so_juro():
    args=list(entradas());args[3]=None
    row=a.quadro_hipoteses(*args).set_index('hipotese').loc['V1']
    assert row.confirma=='inconclusivo'
    assert row.confirma_holm=='inconclusivo'
    assert pd.isna(row.p_valor)


def test_aud21_contagens_vem_dos_eventos_elegiveis():
    b=pd.DataFrame({'data':pd.bdate_range('2020-01-01',periods=180),'agio_anormal':np.sin(np.arange(180))})
    ev=pd.DataFrame({'data':b.data.iloc[[20,45,70,90,110,179]].to_numpy(),
                     'tipo':['fiscal','politico','externo','monetario','regulatorio','externo'],'descricao':list('abcdef')})
    _,_,comp=a.estudo_evento(b,ev,n_perm=20)
    assert comp['n_domesticos']==2 and comp['n_externos']==1


@pytest.mark.parametrize('ausencia',['none','sem_externo','p_nan'])
def test_aud22_familia_fixa_v5_indisponivel_sem_p_ficticio(ausencia):
    args=list(entradas())
    if ausencia=='none':args[4]=None
    elif ausencia=='sem_externo':args[4]=args[4].assign(tipo='fiscal')
    else:args[4]=args[4].assign(p_valor_permutacao=np.nan)
    q=a.quadro_hipoteses(*args).set_index('hipotese')
    assert set(q.index)=={'V1','V2','V3','V4a','V4b','V5','V6'}
    assert pd.isna(q.loc['V5','p_valor']) and pd.isna(q.loc['V5','p_holm'])
    assert not q.loc['V5','estimavel']
    assert q.loc['V5','confirma']==q.loc['V5','confirma_holm']=='inconclusivo'
    expected=multipletests(q.p_valor.fillna(1.0).to_numpy(),method='holm')[1]
    ok=q.estimavel.to_numpy()
    np.testing.assert_allclose(q.p_holm.to_numpy()[ok],expected[ok])


def test_aud22_sete_estimaveis_preservam_resultado_baseline():
    spec=importlib.util.spec_from_file_location('a_old',ROOT/'auditorias/AUD-002/baseline_original/src/agio/analise.py')
    old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    args=entradas()
    before=old.quadro_hipoteses(*args)
    after=a.quadro_hipoteses(*args)
    # Adendo 2 (05/11/2026): só o rótulo da V6 mudou; números e decisões iguais.
    rotulo_v6=after.hipotese=='V6'
    assert after.loc[rotulo_v6,'descricao'].tolist()==['Ágio segue caindo após alta do dólar']
    pd.testing.assert_frame_equal(before.drop(columns='descricao'),after[before.columns].drop(columns='descricao'))
    assert (before.descricao[~rotulo_v6]==after.descricao[~rotulo_v6]).all()
