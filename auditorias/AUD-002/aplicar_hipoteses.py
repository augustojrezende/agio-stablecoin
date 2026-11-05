from pathlib import Path
import shutil,subprocess,os,datetime
r=Path('/Users/augustojrezende/Projetos/agio-stablecoin_v2');a=r/'auditorias/AUD-002';os.chdir(r)
e=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(r/'src'),MPLCONFIGDIR=str(a/'cache/mpl'),XDG_CACHE_HOME=str(a/'cache'),GIT_OPTIONAL_LOCKS='0')
shutil.copy2('/private/tmp/test_aud002_hipoteses.py',r/'tests/test_aud002_hipoteses.py')
with (a/'hipoteses_antes.log').open('w') as f:
 ret=subprocess.run([str(r/'.venv/bin/python'),'-m','pytest','-q','-p','no:cacheprovider','tests/test_aud002_hipoteses.py'],env=e,stdout=f,stderr=subprocess.STDOUT)
assert ret.returncode!=0
p=r/'src/agio/analise.py';s=p.read_text()
old='comparacao = {"car_domesticos": dom.mean(), "car_externos": ext.mean(),'
assert old in s;s=s.replace(old,'comparacao = {"car_domesticos": dom.mean(), "car_externos": ext.mean(),\n                      "n_domesticos": len(dom), "n_externos": len(ext),')
s=s.replace('                   np.nanmax([p, p_dif]), b > 0 and dif > 0))','                   max(p, p_dif) if np.isfinite(p) and np.isfinite(p_dif) else np.nan,\n                   b > 0 and dif > 0))')
old='    q = pd.DataFrame(linhas, columns=["hipotese", "descricao", "estimativa", "p_valor", "sinal_previsto"])'
new='''    else:
        linhas.append(("V5", "Choques externos isolados reduzem o ágio",
                       "não estimável: sem grupo externo isolado", np.nan, False))
    q = pd.DataFrame(linhas, columns=["hipotese", "descricao", "estimativa", "p_valor", "sinal_previsto"])
    # AUD-002: família fixa. O 1 é apenas reserva conservadora no cálculo,
    # não é p observado. Ausência permanece explícita nas colunas públicas.
    q["estimavel"] = np.isfinite(q["p_valor"])
    q.loc[~q["estimavel"], "p_valor"] = np.nan'''
assert s.count(old)==1;s=s.replace(old,new)
old='    n_eventos = {"V2": g.loc["todos", "n"] if "todos" in g.index else 0}'
new='''    # Decisão do pesquisador, AUD-002: mínimo de dez em CADA braço de V1.
    n_dom = comp_agio.get("n_domesticos", 0) if comp_agio else 0
    n_ext = comp_agio.get("n_externos", 0) if comp_agio else 0
    n_eventos = {"V1": min(n_dom, n_ext),
                "V2": g.loc["todos", "n"] if "todos" in g.index else 0}'''
assert old in s;s=s.replace(old,new)
old='    return q\n'
new='''    q.loc[~q["estimavel"], ["confirma", "confirma_holm"]] = "inconclusivo"
    q.loc[~q["estimavel"], "p_holm"] = np.nan
    return q
'''
assert s.count(old)==1;s=s.replace(old,new);p.write_text(s)
# Route generated analyses into clearly versioned locations within V2. Input/reference outputs remain intact.
for path,old,new in [
 ('src/agio/cli.py','PASTA_RESULTADOS = arm.RAIZ / "resultados"','PASTA_RESULTADOS = arm.RAIZ / "resultados_v2"'),
 ('src/agio/relatorio.py','DOCS = arm.RAIZ.parent / "docs"','DOCS = arm.RAIZ.parent / "docs" / "v2"'),
 ('src/agio/relatorio.py','RESULTADOS = arm.RAIZ / "resultados"','RESULTADOS = arm.RAIZ / "resultados_v2"'),
 ('src/agio/episodio.py','RESULTADOS = arm.RAIZ / "resultados"','RESULTADOS = arm.RAIZ / "resultados_v2"'),
 ('src/agio/episodio.py','FIGURAS = arm.RAIZ.parent / "docs" / "figuras"','FIGURAS = arm.RAIZ.parent / "docs" / "v2" / "figuras"')]:
 p=r/path;s=p.read_text();assert s.count(old)==1,(path,old);p.write_text(s.replace(old,new))
(r/'docs/AUD-002_DECISOES_V2.md').write_text('''# Decisões autorizadas para a V2 — 02/11/2026

Este registro novo documenta decisões explícitas do pesquisador na conversa AUD-002. Não reescreve docs/pre-registro.md, não modifica V1–V6 nem toma decisões sobre avaliação sequencial.

## AUD-001-21: elegibilidade V1

Autorização: “Exigir pelo menos 10 domésticos e 10 externos”. Contar eventos com CAR válido da lista completa: domésticos=fiscal+político, externos=externo. Zero/grupo ausente, contagem indisponível ou qualquer grupo abaixo de dez gera inconclusivo nas duas decisões; não negativo. Com ambos ≥10, mantém-se o teste conjunto de sinais e máximo dos p-valores. Quando um componente do teste conjunto não é estimável, o p conjunto é ausente, não apenas o p do componente restante. A insuficiência amostral não elimina uma hipótese da família.

## AUD-001-22: hipótese não estimável e Holm

Autorização: manter V5 não estimável, p bruto ausente e valor interno 1 somente como reserva conservadora de sua posição na família de sete. São sempre V1,V2,V3,V4a,V4b,V5,V6. A coluna estimavel identifica disponibilidade do p; p_valor e p_holm de hipótese não estimável ficam ausentes; confirma e confirma_holm ficam inconclusivo. Para as hipóteses estimáveis, o cálculo de Holm usa sete posições, sem excluir a vaga indisponível. O 1 interno não é estatística, estimativa ou evidência observada e não é publicado como p bruto.

Justificativa: manter o tamanho da família registrada evita reduzir silenciosamente os multiplicadores de Holm. Reservar posição no extremo superior não introduz evidência de rejeição; a hipótese não estimável não é rejeitada. A família com sete p-valores observados mantém resultados idênticos à implementação anterior. Essa política não corrige seleção exploratória, dependência temporal ou a regra sequencial, fora do escopo autorizado.

## Versionamento de saídas

Resultados originais: dados/resultados e docs/figuras, preservados; cópia histórica completa em auditorias/AUD-002/baseline_original. Lista original: dados/manual/eventos.csv. Lista V2: dados/manual/eventos_v2.csv. Resultados corrigidos: dados/resultados_v2. Figuras/tabelas corrigidas: docs/v2. Proveniência e comparação por artefato: auditorias/AUD-002. Parâmetros estatísticos e dados históricos são preservados.
''')
with (a/'hipoteses_depois.log').open('w') as f:
 ret=subprocess.run([str(r/'.venv/bin/python'),'-m','pytest','-q','-p','no:cacheprovider','tests/test_aud002_hipoteses.py'],env=e,stdout=f,stderr=subprocess.STDOUT)
print('Testes de hipóteses após correção:',ret.returncode);assert ret.returncode==0
shutil.copy2('/private/tmp/aud002_hipoteses.py',a/'aplicar_hipoteses.py')
