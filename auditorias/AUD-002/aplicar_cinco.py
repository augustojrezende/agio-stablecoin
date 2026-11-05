from pathlib import Path
import shutil,subprocess,os,json
r=Path('/Users/augustojrezende/Projetos/agio-stablecoin_v2');a=r/'auditorias/AUD-002';os.chdir(r)
e=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(r/'src'),MPLCONFIGDIR=str(a/'cache/mpl'),XDG_CACHE_HOME=str(a/'cache'),GIT_OPTIONAL_LOCKS='0')
shutil.copy2('/private/tmp/test_aud002.py',r/'tests/test_aud002.py')
with (a/'regressoes_antes.log').open('w') as f:
 ret=subprocess.run([str(r/'.venv/bin/python'),'-m','pytest','-q','-p','no:cacheprovider','tests/test_aud002.py'],env=e,stdout=f,stderr=subprocess.STDOUT)
assert ret.returncode!=0

def replace(path,old,new):
 p=r/path;s=p.read_text();assert s.count(old)==1,(path,old);p.write_text(s.replace(old,new))
replace('src/agio/cli.py','return pd.concat(lotes).drop_duplicates(["inicio_utc", "fonte"], keep="last")','return (pd.concat(lotes, ignore_index=True)\n            .drop_duplicates(["inicio_utc", "fonte"], keep="last")\n            .sort_values(["inicio_utc", "fonte"]).reset_index(drop=True))')
# Preserve original events.csv and direct V2 analyses to the separately named corrected list.
for path in ['src/agio/cli.py','src/agio/relatorio.py']:
 replace(path,'/ "manual" / "eventos.csv"','/ "manual" / "eventos_v2.csv"')
p=r/'scripts/montar_eventos.py';s=p.read_text();s=s.replace('dados/manual/eventos.csv','dados/manual/eventos_v2.csv').replace('/ "manual" / "eventos.csv"','/ "manual" / "eventos_v2.csv"')
s=s.replace('def montar() -> pd.DataFrame:', '''def marcar_sobreposicoes(eventos: pd.DataFrame, calendario) -> pd.DataFrame:
    """V2: interseção de janelas −1,+3 nas datas efetivamente observadas.

    Preserva a regra de comparar apenas tipos diferentes. Eventos após o
    fim da base não possuem janela observada; nenhuma data é inventada.
    """
    from agio.analise import JANELA_EVENTO

    datas = pd.DatetimeIndex(pd.to_datetime(calendario))
    if datas.empty or datas.hasnans or datas.has_duplicates or not datas.is_monotonic_increasing:
        raise ValueError("O calendário efetivo deve ser ordenado, único, não vazio e sem NaT")
    posicoes = datas.searchsorted(pd.to_datetime(eventos["data"]))
    janelas = [set(range(max(0, p + JANELA_EVENTO[0]),
                         min(len(datas), p + JANELA_EVENTO[1] + 1)))
               if p < len(datas) else set() for p in posicoes]
    tipos = eventos["tipo"].to_numpy()
    saida = eventos.copy()
    saida["sobreposto"] = [
        "sim" if any(tipos[i] != tipos[j] and bool(janela & outra)
                     for j, outra in enumerate(janelas)) else "nao"
        for i, janela in enumerate(janelas)
    ]
    return saida


def montar(calendario=None) -> pd.DataFrame:''')
start=s.index('    # Sobreposição: outro evento de tipo diferente');end=s.index('    return ev[[',start)
s=s[:start]+'''    if calendario is None:
        caminho = SAIDA.parents[1] / "resultados" / "base_teste.csv"
        calendario = pd.read_csv(caminho, usecols=["data"])["data"]
    ev = marcar_sobreposicoes(ev, calendario)
'''+s[end:];p.write_text(s)
replace('src/agio/relatorio.py','    med = alinhado.set_index("data")["agio_pct"].rolling(60, min_periods=30).median()', '    from agio.analise import JANELA_NORMAL, MINIMO_NORMAL\n    med = (alinhado.set_index("data")["agio_pct"].shift(1)\n           .rolling(JANELA_NORMAL, min_periods=MINIMO_NORMAL).median())')
replace('src/agio/analise.py','        "n_eventos": len(validas),','        "n_eventos": np.sum(~np.isnan(matriz), axis=0) if len(validas) else np.zeros(len(rel), dtype=int),\n        "n_eventos_nominal": len(validas),\n        "n_placebo_sorteado": n,')
replace('src/agio/relatorio.py', '        ax.set_title(f"{NOMES_TIPO[tipo]} (n = {int(tr[\'n_eventos\'].iloc[0])})")', '''        n_min, n_max = int(tr["n_eventos"].min()), int(tr["n_eventos"].max())
        rotulo_n = str(n_min) if n_min == n_max else f"{n_min}–{n_max}"
        ax.set_title(f"{NOMES_TIPO[tipo]} (n válido = {rotulo_n})", pad=35)
        contagens = ax.secondary_xaxis("top")
        contagens.set_xticks(tr["dia"], [str(int(n)) for n in tr["n_eventos"]])
        contagens.tick_params(labelsize=6, length=2, pad=1)
        contagens.set_xlabel("n válido por dia", fontsize=6, labelpad=2)
        FIGURAS.mkdir(parents=True, exist_ok=True)
        tr.to_csv(FIGURAS / f"{Path(nome).stem}_{tipo}.csv", index=False)''')
# Only trajectory legend, not inference or random generator.
replace('src/agio/relatorio.py','    _salvar(fig, nome, legenda, figs)','    _salvar(fig, nome, legenda + " n válido por dia indicado acima de cada ponto; "\n            "pode variar por dados ausentes. Contagens, médias e faixas nos CSVs por tipo. "\n            "O número nominal de datas do sorteio placebo foi preservado.", figs)')
replace('src/agio/episodio.py','        linhas.append(f"  {c:32s} {antes[c].mean():>12.3f} {durante[c].mean():>12.3f}")', '''        rotulo = f"{c} (USDT)" if c.startswith("volume_janela") else c
        anterior, atual = antes[c].mean(), durante[c].mean()
        variacao = (f"; variação {100 * (atual / anterior - 1):+.2f}%"
                    if c.startswith("volume_janela") and anterior > 0 else "")
        linhas.append(f"  {rotulo:40s} {anterior:>12.3f} {atual:>12.3f}{variacao}")''')
replace('docs/resultados.md','R$ 17,1 mi → R$ 26,1 mi','17,1 mi → 26,1 mi de USDT')
p=r/'docs/resultados.md';s=p.read_text();s=s.replace('\n\n','\n\n*V2 — AUD-002: neste documento, somente a unidade do volume na seção 3.1 foi corrigida. A narrativa histórica restante foi preservada; os resultados V2 e suas diferenças estão em auditorias/AUD-002/.*\n\n',1);p.write_text(s)
# Generate the corrected list without touching historical original.
with (a/'eventos_v2.log').open('w') as f:
 ret=subprocess.run([str(r/'.venv/bin/python'),'scripts/montar_eventos.py'],env=e,stdout=f,stderr=subprocess.STDOUT)
assert ret.returncode==0
with (a/'regressoes_cinco_depois.log').open('w') as f:
 ret=subprocess.run([str(r/'.venv/bin/python'),'-m','pytest','-q','-p','no:cacheprovider','tests/test_aud002.py'],env=e,stdout=f,stderr=subprocess.STDOUT)
print('Testes após cinco correções:',ret.returncode)
assert ret.returncode==0
shutil.copy2('/private/tmp/aud002_cinco.py',a/'aplicar_cinco.py')
