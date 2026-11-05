import sys,json
from pathlib import Path
import pandas as pd,numpy as np
S=json.loads(Path('/private/tmp/AUD-001-state.json').read_text());sys.path.insert(0,S['tmp']+'/src');O=Path(S['out']);r=Path(S['repo'])
from agio import analise as a
reg=pd.read_csv(r/'dados/resultados/regressao_agio_anormal.csv');soma=pd.read_csv(r/'dados/resultados/regressao_repasse_soma.csv').iloc[0].to_dict();g=pd.read_csv(r/'dados/resultados/eventos_grupos_negocios_anormal.csv');gi=pd.read_csv(r/'dados/resultados/eventos_grupos_agio_ajustado_dolar_sem_sobrepostos.csv');b=pd.read_csv(r/'dados/resultados/base_teste.csv',parse_dates=['data'])
e=pd.DataFrame({'data':b.data.iloc[[100,200]].to_numpy(),'tipo':['fiscal','externo'],'descricao':['sintético doméstico','sintético externo']});_,_,comp=a.estudo_evento(b,e,n_perm=100)
q=a.quadro_hipoteses(reg,soma,g,comp,gi);q.to_csv(O/'hipoteses_teste_2_eventos.csv',index=False)
q2=a.quadro_hipoteses(reg,soma,g,comp,None)
d={'V1_com_2_eventos':q[q.hipotese=='V1'].to_dict('records'),'familia_sem_V5':q2.hipotese.tolist()}
w=pd.read_csv(r/'dados/tratado/precos_janela_ptax.csv');w=w[w.data.isin(b.data.dt.strftime('%Y-%m-%d'))];d['janelas_incompletas_na_amostra']=w[w.horas_janela<3].to_dict('records')
# Figure table difference: normalize generation date only, preserve every other difference.
import re,difflib
x=(r/'docs/resultados_tabelas.md').read_text();y=(Path(S['tmp'])/'docs/resultados_tabelas.md').read_text();x=re.sub(r'gerado','gerado',x);x=re.sub(r'em \d\d/\d\d/\d{4}', 'em DATA',x);y=re.sub(r'em \d\d/\d\d/\d{4}','em DATA',y)
(O/'diferenca_tabelas.diff').write_text(''.join(difflib.unified_diff(x.splitlines(True),y.splitlines(True),fromfile='original',tofile='reproduzido')));d['tabelas_iguais_exceto_data']=x==y
# Complete inventory, sizes and functions.
rows=[]
for p in sorted(r.rglob('*')):
 if p.is_file() and not any(x in p.relative_to(r).parts for x in ['.git','.venv','.pytest_cache','__pycache__','auditorias']):rows.append({'arquivo':str(p.relative_to(r)),'bytes':p.stat().st_size})
pd.DataFrame(rows).to_csv(O/'inventario_arquivos.csv',index=False)
(O/'verificacoes_finais.json').write_text(json.dumps(d,indent=2,default=str));print(json.dumps(d,indent=2,default=str))
