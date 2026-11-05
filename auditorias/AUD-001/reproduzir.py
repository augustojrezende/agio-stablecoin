import os,sys,json,platform,importlib.metadata,contextlib,subprocess
from pathlib import Path
import numpy as np,pandas as pd
from datetime import date
R=Path(__file__).parent; S=json.loads(Path('/private/tmp/AUD-001-state.json').read_text()); O=Path(S['out']); original=Path(S['repo'])
sys.path.insert(0,str(R/'src'))
from agio import cli,armazenamento as arm
from agio.fontes import bcb,binance,mercadobitcoin,tesouro,fred,defillama,google_trends
from agio.janela import preco_janela_ptax
assert arm.RAIZ==R/'dados'
# Network prohibited even if a future code path accidentally attempts it.
import requests,socket
def blocked(*a,**k): raise RuntimeError('AUD-001: rede bloqueada')
requests.sessions.Session.request=blocked
socket.create_connection=blocked
cut=date(2026,10,30)
def clip(d): return d[pd.to_datetime(d.data).dt.date<=cut].copy()
def raw(folder): return sorted((arm.BRUTO/folder).glob('*'),key=lambda p:p.name.split('coletado-')[-1])
def save(name,d,keys):
 d=clip(d).drop_duplicates(keys,keep='last').sort_values(keys).reset_index(drop=True);d.to_csv(arm.TRATADO/f'{name}.csv',index=False)
for folder,name,fun in [('bcb_ptax','ptax',bcb.tratar_ptax),('bcb_selic','selic',lambda b:bcb.tratar_sgs(b,'selic_dia_pct'))]:
 save(name,pd.concat([fun(json.loads(p.read_text())) for p in raw(folder)]),['data'])
prices=[]; windows=[]; hours_summary=[]
for name,mod in [('binance',binance),('mercadobitcoin',mercadobitcoin)]:
 prices += [mod.tratar(json.loads(p.read_text()),name) for p in raw(name)]
 h=pd.concat([mod.tratar_horario(json.loads(p.read_text()),name) for p in raw(name+'_1h')]); dup=int(h.duplicated(['inicio_utc','fonte']).sum());h=h.drop_duplicates(['inicio_utc','fonte'],keep='last')
 h=h[h.inicio_utc.dt.tz_convert('America/Sao_Paulo').dt.date<=cut]
 windows.append(preco_janela_ptax(h.reset_index(drop=True))); hours_summary.append({'fonte':name,'horas':len(h),'duplicatas_entre_lotes':dup,'volume_negativo':int((h.volume_base<0).sum()),'ohlc_invalido':int(((h.maxima<h.minima)|(h.fechamento>h.maxima)|(h.fechamento<h.minima)).sum())})
save('precos_usdt_brl',pd.concat(prices),['data','fonte']);save('precos_janela_ptax',pd.concat(windows),['data','fonte'])
save('juro_real_10a',tesouro.juro_real_10a(clip(tesouro.tratar(raw('tesouro_direto')[-1].read_text()))),['data'])
save('vix',fred.tratar_cboe(raw('cboe_vix')[-1].read_text()),['data'])
save('usdt_oferta',defillama.tratar(json.loads(raw('defillama_usdt')[-1].read_text())),['data'])
save('google_trends',google_trends.encadear([clip(google_trends.ler_csv(p)) for p in sorted((arm.RAIZ/'manual/google_trends').glob('*.csv'))]),['data','termo'])
(O/'horarios.json').write_text(json.dumps(hours_summary,indent=2))
with (O/'pipeline.log').open('w') as f,contextlib.redirect_stdout(f):
 cli.calcular();cli.testar()
 try:cli.robustez()
 except Exception:
  import traceback
  traceback.print_exc(file=f)
 cli.oferta_usdt(coletar=False);cli.buscas();cli.relatorio()
 from agio.episodio import rodar
 rodar(date(2026,6,1),date(2026,8,15))
# Compare all CSV data, cutting dates only (later raw observations are never inputs).
comparisons=[]; details=[]; inventory=[]
for folder in ['tratado','resultados']:
 for p in sorted((original/'dados'/folder).glob('*.csv')):
  a=pd.read_csv(p);q=R/'dados'/folder/p.name
  if not q.exists():continue
  b=pd.read_csv(q)
  if 'data' in a:a=clip(a)
  if 'data' in b:b=clip(b)
  keys=[c for c in ['data','fonte','termo','variavel','tipo','descricao','hipotese','especificacao'] if c in a and c in b]
  if keys:a=a.sort_values(keys).reset_index(drop=True);b=b.sort_values(keys).reset_index(drop=True)
  row={'arquivo':str(p.relative_to(original)),'n_original':len(a),'n_reproduzido':len(b),'colunas_iguais':list(a)==list(b),'max_abs':0.,'max_rel':0.,'divergencias':0,'texto_igual':True}
  if a.shape==b.shape and list(a)==list(b):
   for c in a:
    if pd.api.types.is_numeric_dtype(a[c]) and pd.api.types.is_numeric_dtype(b[c]):
     av=a[c].to_numpy(float);bv=b[c].to_numpy(float);delta=np.abs(av-bv); valid=np.isfinite(delta)
     ma=float(delta[valid].max()) if valid.any() else 0;mr=float((delta[valid]/np.maximum(np.abs(av[valid]),1e-12)).max()) if valid.any() else 0
     n=int((~np.isclose(av,bv,atol=1e-10,rtol=1e-8,equal_nan=True)).sum());row['max_abs']=max(row['max_abs'],ma);row['max_rel']=max(row['max_rel'],mr);row['divergencias']+=n
     details.append({'arquivo':row['arquivo'],'coluna':c,'max_abs':ma,'max_rel':mr,'divergencias':n,'min_original':a[c].min(),'max_original':a[c].max(),'media_original':a[c].mean(),'min_reproduzido':b[c].min(),'max_reproduzido':b[c].max(),'media_reproduzido':b[c].mean()})
    else: row['texto_igual'] &= a[c].fillna('').astype(str).equals(b[c].fillna('').astype(str))
  else:row['divergencias']=-1
  comparisons.append(row)
  if 'data' in a: inventory.append({'arquivo':row['arquivo'],'n':len(a),'inicio':a.data.min(),'fim':a.data.max(),'duplicatas_chave':int(a.duplicated(keys).sum()) if keys else None,'ausentes':a.isna().sum().to_dict()})
pd.DataFrame(comparisons).to_csv(O/'comparacoes.csv',index=False);pd.DataFrame(details).to_csv(O/'comparacoes_colunas.csv',index=False)
(O/'inventario_dados.json').write_text(json.dumps(inventory,indent=2,default=str))
(O/'versoes.json').write_text(json.dumps({'python':sys.version,'platform':platform.platform(),'packages':{n:importlib.metadata.version(n) for n in ['numpy','pandas','scipy','statsmodels','matplotlib','requests','pytest']}},indent=2))
print(pd.DataFrame(comparisons).to_string(index=False))
