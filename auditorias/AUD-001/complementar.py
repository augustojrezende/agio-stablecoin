import sys,json,hashlib,shutil
from pathlib import Path
import numpy as np,pandas as pd
from PIL import Image,ImageDraw
S=json.loads(Path('/private/tmp/AUD-001-state.json').read_text());R=Path(S['tmp']);O=Path(S['out']);repo=Path(S['repo']);sys.path.insert(0,str(R/'src'))
from agio import analise as a,armazenamento as arm,cli
from agio.janela import preco_janela_ptax
from agio.indicador import calcular_agio,consolidar
T={p.stem:arm.ler_tratado(p.stem) for p in arm.TRATADO.glob('*.csv')}
def base(df):return a.montar_base(df,T['painel_diario'],T['ptax'],T['precos_usdt_brl'],T['juro_real_10a'],T['vix'])
b=base(T['agio_diario']);rows=[a.resumo_especificacao('1. Principal (janela 10h-13h, MQO + Newey-West)',b),a.resumo_especificacao('2. Winsorizado 1%/99%',a.winsorizar(b,['agio_anormal']+a.CONTROLES)),a.resumo_especificacao('3. Regressão robusta (Huber)',b,metodo='huber'),a.resumo_especificacao('4. Ágio de fechamento (21h)',base(T['agio_fechamento_diario']))]
for f in sorted(T['agio_por_fonte'].fonte.unique()):rows.append(a.resumo_especificacao('5. Só '+f,base(T['agio_por_fonte'].query('fonte==@f')[['data','agio_pct']])))
rows.extend([a.resumo_especificacao('6a. Antes de 04/05/2026',a.periodo(b,fim='2026-05-04')),a.resumo_especificacao('6b. A partir de 04/05/2026',a.periodo(b,inicio='2026-05-04'))])
# AUDIT ONLY: remove non-unique pandas row labels in memory, leave baseline implementation untouched.
w=[]
for f in cli.CORRETORAS:
 h=cli._horas_do_bruto(f).reset_index(drop=True);h=h[h.inicio_utc.dt.tz_convert('America/Sao_Paulo').dt.strftime('%Y-%m-%d')<='2026-10-30'].reset_index(drop=True);w.append(preco_janela_ptax(h,hora_fim=14))
rows.append(a.resumo_especificacao('7. Janela 10h-14h (inclui a consulta das 13h)',base(consolidar(calcular_agio(pd.concat(w),T['ptax'],coluna_preco='preco_janela',coluna_volume='volume_janela')))))
rob=pd.DataFrame(rows);rob.to_csv(O/'robustez_recalculada_auditoria.csv',index=False);old=pd.read_csv(repo/'dados/resultados/robustez.csv');num=old.select_dtypes('number').columns
s={'robustez_maxdiff':float(np.max(np.abs(old[num].values-rob[num].values))),'robustez_cli':'falha; números recalculados por funções, reset_index apenas em memória de auditoria'}
# Full original base vs reconstructed common columns.
u=pd.read_csv(repo/'dados/resultados/base_teste.csv');v=pd.read_csv(R/'dados/resultados/base_teste.csv');num=u.select_dtypes('number').columns
s['base_colunas_novas']=sorted(set(v)-set(u));s['base_comum_maxdiff']=float(np.nanmax(abs(u[num].values-v[num].values)))
c=pd.read_csv(O/'comparacoes.csv');c['status']='reproduzido';c.loc[c.arquivo.str.endswith('/robustez.csv'),'status']='CLI falhou; comparação inicial era cópia; ver robustez_recalculada_auditoria.csv';c.loc[c.arquivo.str.endswith('/base_teste.csv'),'status']='colunas comuns exatas; 4 colunas Trends novas';c.to_csv(O/'comparacoes.csv',index=False)
# Pixel checks for all 10 figures and extra episode. No edits to any baseline image.
fr=[];thumbs=[]
for p in sorted((repo/'docs/figuras').glob('*.png')):
 q=R/'docs/figuras'/p.name;im=Image.open(p).convert('RGB');im2=Image.open(q).convert('RGB');equal=im.size==im2.size and np.array_equal(np.asarray(im),np.asarray(im2));fr.append({'figura':p.name,'dimensao':str(im.size),'pixels_iguais':equal,'sha_igual':hashlib.sha256(p.read_bytes()).digest()==hashlib.sha256(q.read_bytes()).digest()})
 im.thumbnail((600,380));tile=Image.new('RGB',(620,410),'white');tile.paste(im,((620-im.width)//2,24));ImageDraw.Draw(tile).text((8,4),p.name,fill='black');thumbs.append(tile)
canvas=Image.new('RGB',(1240,410*((len(thumbs)+1)//2)),'white')
for i,t in enumerate(thumbs):canvas.paste(t,((i%2)*620,(i//2)*410))
canvas.save(O/'contato_figuras.png');pd.DataFrame(fr).to_csv(O/'comparacao_figuras.csv',index=False)
# trajectories effective n differs pointwise; contaminants by other event types.
ev=pd.read_csv(repo/'dados/manual/eventos.csv',parse_dates=['data']);br=pd.read_csv(repo/'dados/resultados/base_teste.csv',parse_dates=['data']);trrows=[]
for typ in ['fiscal','externo','monetario']:
 es=ev[ev.tipo==typ];pos=a._posicoes_eventos(br,es).pos.to_numpy();pos=pos[(pos>=5)&(pos+10<len(br))];valid=np.array([br.agio_anormal.iloc[p-5:p+11].notna().to_numpy() for p in pos]);trrows.append({'tipo':typ,'n_rotulo':len(pos),'n_min_por_dia':int(valid.sum(axis=0).min()),'n_max_por_dia':int(valid.sum(axis=0).max())})
pd.DataFrame(trrows).to_csv(O/'figuras_n_efetivo.csv',index=False)
# real overlaps diagnostic only, no changing list.
e=pd.read_csv(O/'reconciliacao_eventos.csv',parse_dates=['data']);ef=a._posicoes_eventos(br,ev);mask=np.array([not any((abs(ef.pos-p)<=4)&(ef.tipo!=t)) for p,t in zip(ef.pos,ef.tipo)])
for col in ['agio_anormal','agio_ajustado_dolar']:
 _,_,comp=a.estudo_evento(br,ef[mask],col);s['calendario_real_'+col]=comp
# Episode true subwindow vs broad published interval.
from agio.episodio import montar,resumo
from datetime import date
(O/'episodio_janela_estreita.txt').write_text(resumo(montar(date(2026,6,24),date(2026,7,20))))
# unit volume-base vs BRL approximation from HLC typical price.
ep=pd.read_csv(repo/'dados/resultados/episodio_20260601_20260815.csv');s['volume_brl_estimado_antes']=float((ep.loc[~ep.no_episodio,'volume_janela_binance']*ep.loc[~ep.no_episodio,'preco_janela_binance']).mean());s['volume_brl_estimado_durante']=float((ep.loc[ep.no_episodio,'volume_janela_binance']*ep.loc[ep.no_episodio,'preco_janela_binance']).mean())
(O/'complementos.json').write_text(json.dumps(s,indent=2,default=str));print(json.dumps(s,indent=2,default=str));print(pd.DataFrame(fr).to_string(index=False))
