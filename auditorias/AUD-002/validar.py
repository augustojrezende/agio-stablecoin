from pathlib import Path
import os,sys,json,subprocess,hashlib,datetime,contextlib,functools,importlib.util,importlib.metadata,shutil
R=Path('/Users/augustojrezende/Projetos/agio-stablecoin_v2');A=R/'auditorias/AUD-002';B=A/'baseline_original';os.chdir(R)
os.environ.update(PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(R/'src'),MPLCONFIGDIR=str(A/'cache/mpl'),XDG_CACHE_HOME=str(A/'cache'),GIT_OPTIONAL_LOCKS='0')
sys.dont_write_bytecode=True;sys.path.insert(0,str(R/'src'))
import numpy as np,pandas as pd,requests
from datetime import date
from agio import cli,analise as an,armazenamento as arm,relatorio,episodio
from agio.fontes import bcb,binance,mercadobitcoin,tesouro,fred,defillama,google_trends
from agio.janela import preco_janela_ptax
assert arm.RAIZ==R/'dados' and Path(sys.prefix)==R/'.venv'
assert not any('/agio-stablecoin/' in str(p) for p in sys.path)
# Local console entry point for the independent environment (no network/install).
entry=R/'.venv/bin/agio';entry.write_text(f'#!{R}/.venv/bin/python\nfrom agio.cli import main\nif __name__ == "__main__":\n    main()\n');entry.chmod(0o755)
commands=[]
def run(cmd,log):
 commands.append(cmd)
 with (A/log).open('w') as f:
  p=subprocess.run(cmd,env=os.environ.copy(),stdout=f,stderr=subprocess.STDOUT)
 assert p.returncode==0,(cmd,log,p.returncode)
run([str(R/'.venv/bin/python'),'-m','pytest','-q','-p','no:cacheprovider'],'testes_finais.log')
run([str(entry),'robustez'],'robustez_v2_cli.log')
rob_cli=pd.read_csv(cli.PASTA_RESULTADOS/'robustez.csv');rob_old=pd.read_csv(B/'dados/resultados/robustez.csv')
assert len(rob_cli)==9
pd.testing.assert_frame_equal(rob_cli,rob_old,check_exact=False,atol=1e-10,rtol=1e-8)
shutil.copy2(cli.PASTA_RESULTADOS/'robustez.csv',A/'robustez_v2_cli.csv')
# Offline reconstruction into new V2 treated directory. Original input tables and snapshot remain intact.
def blocked(*args,**kwargs):raise RuntimeError('AUD-002: rede proibida')
requests.sessions.Session.request=blocked
cut=date(2026,10,30);treated=R/'dados/tratado_v2';treated.mkdir(exist_ok=True)
arm.TRATADO=treated;read_original=arm.ler_tratado;arm.ler_tratado=functools.partial(read_original,raiz=treated)
used=[]
def raw(folder):
 p=sorted((arm.BRUTO/folder).glob('*'),key=lambda p:p.name.split('coletado-')[-1]);used.extend(p);return p
def clip(d):return d[pd.to_datetime(d.data).dt.date<=cut].copy()
def save(name,d,keys):clip(d).drop_duplicates(keys,keep='last').sort_values(keys).reset_index(drop=True).to_csv(treated/f'{name}.csv',index=False)
for folder,name,fn in [('bcb_ptax','ptax',bcb.tratar_ptax),('bcb_selic','selic',lambda b:bcb.tratar_sgs(b,'selic_dia_pct'))]:
 save(name,pd.concat([fn(json.loads(p.read_text())) for p in raw(folder)]),['data'])
prices=[];windows=[]
for source,module in [('binance',binance),('mercadobitcoin',mercadobitcoin)]:
 prices += [module.tratar(json.loads(p.read_text()),source) for p in raw(source)]
 h=pd.concat([module.tratar_horario(json.loads(p.read_text()),source) for p in raw(source+'_1h')],ignore_index=True)
 h=h.drop_duplicates(['inicio_utc','fonte'],keep='last').sort_values(['inicio_utc','fonte']).reset_index(drop=True)
 h=h[h.inicio_utc.dt.tz_convert('America/Sao_Paulo').dt.date<=cut].reset_index(drop=True)
 windows.append(preco_janela_ptax(h))
save('precos_usdt_brl',pd.concat(prices),['data','fonte']);save('precos_janela_ptax',pd.concat(windows),['data','fonte'])
save('juro_real_10a',tesouro.juro_real_10a(clip(tesouro.tratar(raw('tesouro_direto')[-1].read_text()))),['data'])
save('vix',fred.tratar_cboe(raw('cboe_vix')[-1].read_text()),['data'])
save('usdt_oferta',defillama.tratar(json.loads(raw('defillama_usdt')[-1].read_text())),['data'])
manual=sorted((R/'dados/manual/google_trends').glob('*.csv'));used.extend(manual)
with (A/'pipeline_v2.log').open('w') as log,contextlib.redirect_stdout(log):
 save('google_trends',google_trends.encadear([clip(google_trends.ler_csv(p)) for p in manual]),['data','termo'])
 cli.calcular()
 # Safety gate: no further analysis if fundamental indicators/principal regression differ unexpectedly.
 baseline_ind=pd.read_csv(B/'dados/tratado/agio_diario.csv');novo_ind=pd.read_csv(treated/'agio_diario.csv')
 pd.testing.assert_frame_equal(baseline_ind,novo_ind,check_exact=False,atol=1e-10,rtol=1e-8)
 x=an.montar_base(*[arm.ler_tratado(k) for k in ['agio_diario','painel_diario','ptax','precos_usdt_brl','juro_real_10a','vix']])
 model,table=an.regressao(x);assert model.nobs==1490
 pd.testing.assert_frame_equal(table,pd.read_csv(B/'dados/resultados/regressao_agio_anormal.csv'),check_exact=False,atol=1e-10,rtol=1e-8)
 spec=importlib.util.spec_from_file_location('montar_v2',R/'scripts/montar_eventos.py');evmod=importlib.util.module_from_spec(spec);spec.loader.exec_module(evmod)
 regenerated=evmod.montar(calendario=x.data).astype(str)
 pd.testing.assert_frame_equal(regenerated,pd.read_csv(R/'dados/manual/eventos_v2.csv').astype(str))
 cli.testar();cli.robustez();cli.oferta_usdt(coletar=False);cli.buscas();cli.relatorio()
# Episode separate process: stable global rendering configuration, same preserved treated inputs.
run([str(entry),'episodio','--inicio','2026-06-01','--fim','2026-08-15'],'episodio_v2.log')
# Compare every official CSV, with exact row keys rather than truncated output.
comparisons=[];cellchanges=[]
for oldfolder,newfolder in [(B/'dados/tratado',treated),(B/'dados/resultados',cli.PASTA_RESULTADOS)]:
 for p in sorted(oldfolder.glob('*.csv')):
  q=newfolder/p.name;assert q.exists(),q
  before=pd.read_csv(p);after=pd.read_csv(q)
  if 'data' in before:before=clip(before)
  if 'data' in after:after=clip(after)
  keys=[k for k in ['data','fonte','termo','variavel','tipo','descricao','hipotese','especificacao'] if k in before and k in after]
  if keys:
   before=before.sort_values(keys).reset_index(drop=True);after=after.sort_values(keys).reset_index(drop=True)
  common=[col for col in before if col in after];nums=[col for col in common if pd.api.types.is_numeric_dtype(before[col]) and pd.api.types.is_numeric_dtype(after[col])]
  # Outer-key merge records individual deletions and numeric/text differences.
  before['__row__']=np.arange(len(before));after['__row__']=np.arange(len(after))
  join=keys or ['__row__'];merged=before.merge(after,on=join,how='outer',suffixes=('_v1','_v2'),indicator=True)
  changes=0;maxdiff=0.
  for _,row in merged.iterrows():
   key='; '.join(f'{k}={row[k]}' for k in join)
   if row['_merge']!='both':
    cellchanges.append({'arquivo':str(q.relative_to(R)),'chave':key,'coluna':'linha','v1':'presente' if row['_merge']=='left_only' else 'ausente','v2':'presente' if row['_merge']=='right_only' else 'ausente'});changes+=1;continue
   for col in common:
    if col in join:continue
    v1,v2=row[col+'_v1'],row[col+'_v2']
    if col in nums:
     equal=np.isclose(v1,v2,atol=1e-10,rtol=1e-8,equal_nan=True)
     if np.isfinite(v1) and np.isfinite(v2):maxdiff=max(maxdiff,float(abs(v1-v2)))
    else:equal=(pd.isna(v1) and pd.isna(v2)) or str(v1)==str(v2)
    if not equal:
     cellchanges.append({'arquivo':str(q.relative_to(R)),'chave':key,'coluna':col,'v1':v1,'v2':v2});changes+=1
  comparisons.append({'arquivo_v1':str(p.relative_to(B)),'arquivo_v2':str(q.relative_to(R)),'n_v1':len(before),'n_v2':len(after),'colunas_novas':','.join(sorted(set(after)-set(before))),'alteracoes':changes,'max_dif_absoluta_comuns':maxdiff})
pd.DataFrame(comparisons).to_csv(A/'comparativo_csv.csv',index=False);pd.DataFrame(cellchanges).to_csv(A/'diferencas_celulas.csv',index=False)
# Corrected event list: only the two proven flags may differ.
e1=pd.read_csv(B/'dados/manual/eventos.csv');e2=pd.read_csv(R/'dados/manual/eventos_v2.csv');assert len(e1)==len(e2)==158
pd.testing.assert_frame_equal(e1.drop(columns='sobreposto'),e2.drop(columns='sobreposto'))
ed=e1[['data','tipo','sobreposto']].rename(columns={'sobreposto':'sobreposto_v1'});ed['sobreposto_v2']=e2.sobreposto;ed=ed[ed.sobreposto_v1!=ed.sobreposto_v2];assert len(ed)==2;ed.to_csv(A/'diferencas_eventos.csv',index=False)
# All trajectory numerical means/bands remain exactly the original methodology; export coverage comparisons.
spec=importlib.util.spec_from_file_location('analise_antiga',B/'src/agio/analise.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
base=pd.read_csv(cli.PASTA_RESULTADOS/'base_teste.csv',parse_dates=['data']);cover=[]
for col,stem in [('agio_ajustado_dolar','06_trajetoria_agio'),('negocios_anormal','07_trajetoria_negocios'),('busca_dolar_anormal','09_buscas_dolar'),('busca_usdt_anormal','09_buscas_usdt')]:
 for tipo in ['fiscal','externo','monetario']:
  ev=e1[e1.tipo==tipo];tr_old=old.trajetoria_evento(base,ev,col);tr_new=an.trajetoria_evento(base,ev,col)
  for colnum in ['media','placebo_media','placebo_p025','placebo_p975']:np.testing.assert_array_equal(tr_old[colnum],tr_new[colnum])
  cover.append({'figura':stem,'tipo':tipo,'n_v1':int(tr_old.n_eventos.iloc[0]),'n_v2_min':int(tr_new.n_eventos.min()),'n_v2_max':int(tr_new.n_eventos.max()),'medias_faixas_identicas':True})
pd.DataFrame(cover).to_csv(A/'comparativo_trajetorias.csv',index=False)
figs=[]
for p in sorted((B/'docs/figuras').glob('*.png')):
 q=relatorio.FIGURAS/p.name;assert q.exists(),q
 figs.append({'figura':p.name,'sha_v1':hashlib.sha256(p.read_bytes()).hexdigest(),'sha_v2':hashlib.sha256(q.read_bytes()).hexdigest(),'igual':p.read_bytes()==q.read_bytes()})
pd.DataFrame(figs).to_csv(A/'comparativo_figuras.csv',index=False)
# Effective sample and episode unit verification.
ep=pd.read_csv(B/'dados/resultados/episodio_20260601_20260815.csv');v1=ep.loc[~ep.no_episodio,'volume_janela_binance'].mean();v2=ep.loc[ep.no_episodio,'volume_janela_binance'].mean()
summary={'n_indicador':len(x),'n_regressao':int(model.nobs),'robustez_especificacoes':len(rob_cli),'eventos_cadastrados':len(e2),'eventos_validos_v1':154,'eventos_validos_v2':len(pd.read_csv(cli.PASTA_RESULTADOS/'eventos_agio_anormal.csv')),'isolados_v1':62,'isolados_v2':len(pd.read_csv(cli.PASTA_RESULTADOS/'eventos_agio_anormal_sem_sobrepostos.csv')),'volume_usdt_antes':v1,'volume_usdt_durante':v2,'variacao_volume_pct':100*(v2/v1-1),'principal_preservada':True,'pipeline_sem_rede':True,'sys_prefix':sys.prefix,'packages':{n:importlib.metadata.version(n) for n in ['numpy','pandas','scipy','statsmodels','matplotlib','requests','pytest']}}
(A/'validacao_resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));(A/'comandos_validacao.json').write_text(json.dumps(commands,indent=2))
# Script durável: nenhuma dependência do arquivo temporário de preparação.
print(json.dumps(summary,ensure_ascii=False,indent=2));print(pd.DataFrame(comparisons)[lambda d:d.alteracoes>0].to_string(index=False))
