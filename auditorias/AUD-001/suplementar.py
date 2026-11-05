import sys,json,importlib.util
from pathlib import Path
import numpy as np,pandas as pd
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests
S=json.loads(Path('/private/tmp/AUD-001-state.json').read_text());R=Path(S['tmp']);O=Path(S['out']);repo=Path(S['repo']);sys.path.insert(0,str(R/'src'))
from agio import analise as a
b=pd.read_csv(repo/'dados/resultados/base_teste.csv',parse_dates=['data']);ev=pd.read_csv(repo/'dados/manual/eventos.csv',parse_dates=['data','data_anuncio'])
summary={}; rows=[]
for lag in [5,10,20]:
 m,t=a.regressao(b,lags_hac=lag)
 for v in m.params.index:rows.append(dict(teste=f'HAC {lag}',variavel=v,n=m.nobs,coef=m.params[v],ep=m.bse[v],p=m.pvalues[v],ic_inf=m.conf_int().loc[v,0],ic_sup=m.conf_int().loc[v,1]))
summary['n']=m.nobs;summary['kurtosis']=stats.kurtosis(m.resid,fisher=False);summary['r2']=m.rsquared
# Independent OLS and Bartlett HAC (default statsmodels fit HAC no small sample correction).
X=m.model.exog;y=m.model.endog;beta=np.linalg.lstsq(X,y,rcond=None)[0];u=y-X@beta;xu=X*u[:,None];meat=xu.T@xu
for l in range(1,6):
 z=xu[l:].T@xu[:-l];meat+=(1-l/6)*(z+z.T)
inv=np.linalg.inv(X.T@X);cov=inv@meat@inv
m5,_=a.regressao(b);summary['ols_maxdiff']=float(np.max(np.abs(beta-m5.params)));summary['hac_maxdiff']=float(np.max(np.abs(cov-m5.cov_params())));summary['cov_kwds']=str(m5.cov_kwds)
normal=np.array([np.median(b.agio_pct.iloc[max(0,i-60):i]) if i>=30 else np.nan for i in range(len(b))]);summary['median_maxdiff']=float(np.nanmax(np.abs(b.agio_anormal-(b.agio_pct-normal))))
summary['fig_median_maxdiff']=float(np.nanmax(abs(b.agio_pct.rolling(60,min_periods=30).median()-pd.Series(normal))))
# Leave top Cook's distances out, fixed preselected diagnostic counts; not alternative baseline.
plain=sm.OLS(y,X).fit();cooks=plain.get_influence().cooks_distance[0];indices=np.asarray(m.model.data.row_labels)
pd.DataFrame({'data':b.loc[indices,'data'].to_numpy(),'cook':cooks,'resid':u}).sort_values('cook',ascending=False).head(20).to_csv(O/'influencia.csv',index=False)
for k in [1,5,15]:
 sub=b.drop(index=indices[np.argsort(cooks)[-k:]])
 mm,_=a.regressao(sub)
 for v in ['d_dolar','d_juro_bp','d_vix','d_vix_ant']:rows.append(dict(teste=f'Sem {k} maiores Cook',variavel=v,n=mm.nobs,coef=mm.params[v],ep=mm.bse[v],p=mm.pvalues[v],ic_inf=mm.conf_int().loc[v,0],ic_sup=mm.conf_int().loc[v,1]))
for lo,hi in [('2020-01-01','2023-01-01'),('2023-01-01','2025-01-01'),('2025-01-01','2026-10-31')]:
 mm,_=a.regressao(b[b.data.between(lo,hi,inclusive='left')])
 for v in ['d_dolar','d_juro_bp','d_vix','d_vix_ant']:rows.append(dict(teste=f'{lo} a {hi} exclusivo',variavel=v,n=mm.nobs,coef=mm.params[v],ep=mm.bse[v],p=mm.pvalues[v],ic_inf=mm.conf_int().loc[v,0],ic_sup=mm.conf_int().loc[v,1]))
pd.DataFrame(rows).to_csv(O/'sensibilidade_regressoes.csv',index=False)
# Events: reconcile effective dates and reason, overlaps measured on actual observed calendar.
e=a._posicoes_eventos(b,ev);e['data_efetiva']=[b.data.iloc[p] for p in e.pos];e['car']=[a._car(b.agio_anormal.to_numpy(),p) for p in e.pos]
e['motivo']= ['janela final incompleta' if p+3>=len(b) else 'histórico mínimo de 30 dias / janela contém NaN' if np.isnan(c) else 'incluído' for p,c in zip(e.pos,e.car)]
e.to_csv(O/'reconciliacao_eventos.csv',index=False)
e['sobreposto_calendario_real']=['sim' if any((abs(e.pos-p)<=4)&(e.tipo!=t)) else 'nao' for p,t in zip(e.pos,e.tipo)]
e[e.sobreposto!=e.sobreposto_calendario_real].to_csv(O/'divergencias_sobreposicao.csv',index=False)
summary['excluidos']=e[e.car.isna()][['data','tipo','descricao','motivo']].to_dict('records');summary['sobreposicoes_divergentes']=int((e.sobreposto!=e.sobreposto_calendario_real).sum());summary['eventos_duplicados']=int(ev.duplicated(['data','tipo','descricao']).sum());summary['datas_divergentes_efetivas']=int((e.data!=e.data_efetiva).sum())
summary['composicao']=e[e.car.notna()].groupby(['tipo','agendado']).size().to_dict().__str__()
# Event sensitivity, all supplement seeds 20261102, 5000 draws, add-one p.
rng=np.random.default_rng(20261102);N=5000;erows=[]
for suff,es in [('completa',ev),('sem_sobrepostos',ev[ev.sobreposto=='nao'])]:
 for col in ['agio_anormal','agio_ajustado_dolar']:
  evr,groups,comp=a.estudo_evento(b,es,col)
  q=a._posicoes_eventos(b,es);vals=b[col].to_numpy(float);q['car']=[a._car(vals,p) for p in q.pos];q=q.dropna(subset=['car']);q['ano']=q.data.dt.year
  d=q[q.tipo.isin(a.DOMESTICOS|a.EXTERNOS)].reset_index(drop=True);isdom=d.tipo.isin(a.DOMESTICOS).to_numpy();obs=d.car[isdom].mean()-d.car[~isdom].mean()
  strata=[g.index.to_numpy() for _,g in d.groupby('ano')];car=d.car.to_numpy();adjusted=car-d.groupby('ano').car.transform('mean').to_numpy();obsadj=adjusted[isdom].mean()-adjusted[~isdom].mean();sims=[]
  for _ in range(N):
   lab=isdom.copy()
   for idx in strata:lab[idx]=rng.permutation(lab[idx])
   sims.append(adjusted[lab].mean()-adjusted[~lab].mean())
  p=(1+np.sum(np.abs(sims)>=abs(obsadj)))/(N+1)
  erows.append(dict(lista=suff,variavel=col,teste='Original rótulos irrestritos',n_dom=int(isdom.sum()),n_ext=int((~isdom).sum()),estatistica=obs,p=comp['p_valor_permutacao'],referencia_nula=0))
  erows.append(dict(lista=suff,variavel=col,teste='Rótulos dentro de ano; CAR centrado por ano',n_dom=int(isdom.sum()),n_ext=int((~isdom).sum()),estatistica=obsadj,p=p,referencia_nula=0))
  # Circular annual shifts of complete 5-day CAR series: preserves much serial dependence and overlaps, breaks calendar alignment.
  cars=np.array([a._car(vals,i) for i in range(len(vals))]);years=b.data.dt.year.to_numpy();annual=[np.flatnonzero((years==yr)&np.isfinite(cars)) for yr in np.unique(years)];pos=d.pos.to_numpy();sim=[]
  for _ in range(N):
   shifted=cars.copy()
   for idx in annual:
    if len(idx)>40:shifted[idx]=np.roll(cars[idx],rng.integers(20,len(idx)-19))
   z=shifted[pos];sim.append(z[isdom].mean()-z[~isdom].mean())
  mu=float(np.mean(sim));p=(1+np.sum(np.abs(np.array(sim)-mu)>=abs(obs-mu)))/(N+1)
  erows.append(dict(lista=suff,variavel=col,teste='Deslocamento circular anual CAR, mínimo 20 posições',n_dom=int(isdom.sum()),n_ext=int((~isdom).sum()),estatistica=obs,p=p,referencia_nula=mu))
  # Annual matched placebo for all events, exclusion all registered valid events, not just selected subset.
  full=a._posicoes_eventos(b,ev);full=full[[np.isfinite(a._car(vals,p)) for p in full.pos]];bad=set()
  for posi in full.pos:bad.update(range(posi-4,posi+5))
  candidates=np.array([i for i in range(len(vals)) if i not in bad and np.isfinite(cars[i])]);draw=np.zeros(N);valid=True
  for yr,g in q.groupby('ano'):
   options=candidates[years[candidates]==yr]
   if not len(options):valid=False;break
   draw+=cars[rng.choice(options,size=(N,len(g)),replace=True)].sum(axis=1)/len(q)
  if valid:
   mu=float(draw.mean());ob=q.car.mean();pp=(1+np.sum(abs(draw-mu)>=abs(ob-mu)))/(N+1)
   erows.append(dict(lista=suff,variavel=col,teste='Placebos todos eventos estratificados por ano',n_dom=np.nan,n_ext=np.nan,estatistica=ob,p=pp,referencia_nula=mu))
  summary[f'placebos_{suff}_{col}']=groups.attrs
pd.DataFrame(erows).to_csv(O/'sensibilidade_eventos.csv',index=False)
# Exact mathematical return identity of aggregate USDT implied by price-weighted premium.
P=b.ptax_venda*(1+b.agio_pct/100);rp=100*np.log(P/P.shift());rx=100*np.log(b.ptax_venda/b.ptax_venda.shift());gap=100*np.log((1+b.agio_pct/100)/(1+b.agio_pct.shift()/100))
summary['identidade_retornos_maxdiff']=float(np.nanmax(abs(rp-rx-gap)))
z=b.copy();z['ret_usdt']=rp;z['delta_agio']=b.agio_pct.diff()
rr=[]
for ycol in ['ret_usdt','delta_agio','agio_anormal']:
 mm,tt=a.regressao(z,y=ycol);tt['dependente']=ycol;rr.append(tt)
pd.concat(rr).to_csv(O/'decomposicao_repasse.csv',index=False)
h=pd.read_csv(repo/'dados/resultados/hipoteses.csv');summary['holm_maxdiff']=float(np.max(abs(multipletests(h.p_valor,method='holm')[1]-h.p_holm)))
# Missing covariates and effective VIX vintage after alignment, price-window quality.
v=pd.read_csv(repo/'dados/tratado/vix.csv',parse_dates=['data']).rename(columns={'data':'data_vix'})
left=b[['data']].astype({'data':'datetime64[ns]'});v['data_vix']=v.data_vix.astype('datetime64[ns]');aligned=pd.merge_asof(left,v,left_on='data',right_on='data_vix');aligned['dias_atraso']=(aligned.data-aligned.data_vix).dt.days
aligned[aligned.dias_atraso>0].to_csv(O/'vix_datas_carregadas.csv',index=False);summary['vix_carregado']=int((aligned.dias_atraso>0).sum());summary['vix_max_atraso']=int(aligned.dias_atraso.max())
w=pd.read_csv(repo/'dados/tratado/precos_janela_ptax.csv',parse_dates=['data']);w=w[w.data<=pd.Timestamp('2026-10-30')];summary['horas_janela']=w.groupby('fonte').horas_janela.value_counts().to_dict().__str__();summary['janelas_volume_zero']=w[w.volume_janela<=0].groupby('fonte').size().to_dict()
summary['datas_ptax_sem_agio']=sorted(set(pd.read_csv(repo/'dados/tratado/ptax.csv').data)-set(b.data.dt.strftime('%Y-%m-%d')))
# Frozen event script compared on ALL cells, not just count.
spec=importlib.util.spec_from_file_location('events',R/'scripts/montar_eventos.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);gen=mod.montar().astype(str);official=pd.read_csv(repo/'dados/manual/eventos.csv').astype(str);summary['eventos_script_igual']=gen.equals(official)
(O/'diagnosticos.json').write_text(json.dumps(summary,indent=2,default=str));print(json.dumps(summary,indent=2,default=str));print(pd.DataFrame(erows).to_string(index=False))
