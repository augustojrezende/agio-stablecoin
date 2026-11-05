from pathlib import Path
import json,collections,subprocess,shutil,hashlib
import pandas as pd
S=json.loads(Path('/private/tmp/AUD-001-state.json').read_text());O=Path(S['out']);R=Path(S['repo']);T=Path(S['tmp'])
d=json.loads((O/'diagnosticos.json').read_text());c=json.loads((O/'complementos.json').read_text())
def md(df):
 def f(x):
  if isinstance(x,float):return f'{x:.8g}'
  return str(x).replace('|','/').replace('\n',' ')
 return '| '+' | '.join(df.columns)+' |\n|'+'---|'*len(df.columns)+'\n'+'\n'.join('| '+' | '.join(f(x) for x in row)+' |' for row in df.itertuples(index=False,name=None))
# One numbered verification is one item below, including approved and inconclusive checks.
F=[]
def add(title,cat,grav,status,loc,evidence,proc,impact,action,rec,risk):
 F.append(dict(id=f'AUD-001-{len(F)+1:02}',titulo=title,categoria=cat,gravidade=grav,situacao=status,arquivo_funcao=loc,evidencia=evidence,procedimento=proc,impacto=impact,acao=action,recomendacao=rec,risco=risk))
add('Integridade física da baseline','Verificação concluída sem problemas','informativa','aprovado','Repositório; hashes_antes.json / hashes_depois.json','154 arquivos protegidos, inclusive não rastreados; comparação final em integridade_final.json.','Inventário SHA-256 antes e depois; Git antes/depois.','Preserva história e separa novos artefatos.','MANTER','Manter o snapshot e os manifests desta execução.','Perda de rastreabilidade se descartados.')
add('Reconstrução dos tratados','Verificação concluída sem problemas','informativa','aprovado','fontes/*.py; janela.py; indicador.py; comportamento.py','14 tabelas tratadas reproduzidas exatamente no recorte até 30/10/2026; comparacoes.csv.','Replay dos brutos preservados, com deduplicação por coleta e corte temporal.','Não foi necessário substituir dados por consultas novas.','MANTER','Preservar os brutos e as regras da descoberta.','Reprodução futura depende da disponibilidade desses arquivos.')
add('Indicador, unidades e mediana causal no tempo','Verificação concluída sem problemas','informativa','aprovado','indicador.calcular_agio / consolidar; analise._anormal','Ágio = P/PTAX−1; agio_pct = 100×ágio; anormal em p.p.; mediana independente coincide, diferença máxima zero.','Conferência algébrica e mediana por laço dos 30–60 valores anteriores.','Sem vazamento do próprio dia na referência da regressão.','MANTER','Manter distinção proporção, percentual e ponto percentual.','Confusão de escala se documentação omitir unidades.')
add('Regressão principal e HAC','Verificação concluída sem problemas','informativa','aprovado','analise.regressao; regressao_agio_anormal.csv','n=1490; R²=0,0953508683; curtose Pearson=15,3378; MQO independente difere ≤2,23e−16 e covariância HAC ≤2,38e−14.','Reestimação e cálculo matricial independente de MQO e Bartlett HAC(5).','Coeficientes, erros-padrão e p-valores publicados reproduzem.','MANTER','Documentar inferência normal assintótica, intercepto e ausência de correção de pequena amostra.','Reprodução não resolve identificação causal.')
add('Regressões complementares, eventos e tabelas','Verificação concluída sem problemas','informativa','aprovado','cli.testar / buscas / oferta_usdt; relatorio.tabelas','30 CSVs de resultados reproduzidos diretamente; quadro, seis estudos e comparações coincidem; Markdown igual salvo data de geração.','Comparação de todas as células; dif de tabelas.','Valores de referência são computacionalmente sustentados.','MANTER','Conservar resultados originais como descoberta.','Nenhum erro numérico demonstrado nesses resultados.')
add('Falha do comando robustez com os lotes existentes','Erro comprovado','alta','confirmado','cli._horas_do_bruto:330; cli.robustez:390; janela.preco_janela_ptax:36','ValueError: cannot reindex on an axis with duplicate labels; pipeline.log:219–268. pd.concat conserva índices de cada lote.','Execução literal na cópia; recálculo separado das nove especificações, com reset_index apenas no objeto em memória da auditoria.','Impede reprodução integral pelo comando atual. Os números recalculados coincidem exatamente; não se demonstrou que estavam errados.','CORRIGIR','Em tarefa futura autorizada, normalizar índices na concatenação e testar múltiplos lotes reais.','Rotina de robustez para de funcionar após novas coletas.')
add('Base estatística oficial anterior à inclusão de Trends','Inconsistência documental','baixa','confirmado','dados/resultados/base_teste.csv; cli.testar','Reprodução acrescenta busca_usdt, busca_dólar e seus anormais; 17 colunas comuns idênticas, quatro novas.','Comparação estrutural e numérica com complementar.py.','Evidencia artefatos de rodadas distintas; não altera regressão principal.','DOCUMENTAR','Identificar qual execução produziu cada base/relatório.','Confusão entre rodadas ao reproduzir tudo de uma vez.')
add('Reconciliação de 158 para 154 eventos','Verificação concluída sem problemas','informativa','aprovado','analise._posicoes_eventos / _car; reconciliacao_eventos.csv','Copom 29/10/2020, Fed 06/11/2020 e relatório fiscal 21/11/2020 sem histórico/janela válida; Fed 29/10/2026 sem +3 completo.','CAR e elegibilidade de cada linha; comparação com resultados por evento.','Exclusões são explicadas, sem indício de seleção por sinal.','DOCUMENTAR','Publicar a tabela de fluxo de exclusões, datas cadastradas e efetivas.','Contagem 158/154 parece contraditória sem fluxo explícito.')
add('Definição de domésticos e externos','Verificação concluída sem problemas','informativa','aprovado','analise.DOMESTICOS / EXTERNOS; decisões e pré-registro V1','Domésticos=fiscal+político (50); externos=externo (53) na lista completa; isolados 32 e 15. Copom/regulação não entram no contraste.','Inspeção dos conjuntos e agrupamento da lista elegível.','Coerente com a regra documentada; não representa todo choque brasileiro.','MANTER','Explicitar o universo no texto e não acrescentar categorias retrospectivamente.','Generalização indevida para todo risco doméstico.')
add('Sobreposição calculada no calendário errado','Erro comprovado','alta','confirmado','scripts/montar_eventos.py:157; divergencias_sobreposicao.csv','Copom 28/10/2021 e Fed 04/11/2021 marcados nao; posições 262 e 266 na base (distância 4), janelas compartilham observação.','Recontagem por posições efetivas da base PTAX e tipos diferentes.','Lista sem sobrepostos contém dois eventos sobrepostos entre si. Sensibilidade isolada: diferença ajustada 0,8548, p=0,0306; não muda baseline.','CORRIGIR','Futuro ajuste da regra com calendário efetivo, acompanhado de registro e reapresentação lado a lado.','Amostras classificadas como isoladas não cumprem a regra.')
add('Dependência e comparabilidade nos testes de eventos','Risco metodológico','alta','potencial','analise.estudo_evento','Sorteio placebo com reposição; 654 datas na lista completa e 1006 na isolada; CARs vizinhos dependentes; 47 dos 53 externos são Fed agendado.','Inspeção e permutações por ano/deslocamentos circulares.','Rótulos não são atribuídos aleatoriamente; mudanças de regime e natureza dos eventos afetam permutabilidade.','TESTAR','Reportar sensibilidades temporais, agendados versus não agendados e intervalos compatíveis com dependência.','p-valores podem refletir composição temporal, não origem do choque.')
add('Universo placebo muda ao excluir sobrepostos','Risco metodológico','alta','potencial','analise.estudo_evento:141; analise.trajetoria_evento:284','Proibições usam somente eventos da lista passada. Isolados deixam eventos removidos nas datas placebo; gráficos excluem apenas o tipo do painel.','Leitura de chamadas e contagem de candidatos.','Comparação isolada muda simultaneamente eventos e referência nula; faixa gráfica não equivale ao teste formal.','TESTAR','Contrastar placebo excluindo toda a lista original, sem substituir os resultados publicados.','Atribuir sensibilidade apenas à exclusão de sobreposição.')
add('Precisão Monte Carlo e cálculo b/B','Risco metodológico','média','potencial','analise.estudo_evento:156,175','5000 sorteios, seed 42; p=b/5000, sem inclusão da observação; resolução 0,0002; EP MC aproximado 0,00253 para p=0,033.','Inspeção do algoritmo e cálculo binomial da precisão.','Há risco de p=0 e subestimação discreta; não demonstra inversão de conclusão publicada.','TESTAR','Avaliar (b+1)/(B+1), maior B e erro Monte Carlo em revisão autorizada.','Falsa precisão perto de limiares e problemas de multiplicidade.')
add('Datas e horários de eventos fiscais','Limitação conhecida e adequadamente documentada','alta','potencial','scripts/montar_eventos.montar; docs/decisoes.md: lista fechada','PLDO/PLOA e RARDP gerados por prazos com aviso conferir data efetiva; _ultimo_util_ate só trata fins de semana. CSV não contém hora precisa.','Confronto código, fontes textuais e 23 mapeamentos para outra data efetiva.','Janela pode não estar centrada no anúncio efetivo; já reconhecido pelo projeto.','TESTAR','Auditoria documental primária de publicação e horário dos eventos ainda não verificados.','Erro de mensuração temporal e classificação de surpresa.')
add('Janela PTAX é aproximação','Limitação conhecida e adequadamente documentada','média','confirmado','janela.preco_janela_ptax; docs/decisoes.md','Usa 10:00≤hora<13:00 (13,14,15 UTC); exclui a consulta após 13h; HLC3 ponderado não é VWAP de negócios. Há robustez 10–14.','Inspeção dos candles e método do BCB; reconstrução das duas janelas.','Melhora sincronização, mas não replica os quatro instantes de consulta.','DOCUMENTAR','Descrever limites exatos e HLC3; manter teste 10–14 como sensibilidade.','Alegação de alinhamento exato exagera qualidade da medida.')
add('Candles incompletos e cobertura de corretoras','Risco metodológico','média','potencial','janela.preco_janela_ptax; verificacoes_finais.json','13 linhas corretora-dia da amostra têm menos de três candles (2 Binance, 11 MB); sem janelas com volume total zero; horas_janela conta candles, não horas com negócios.','Contagem na interseção com as 1520 datas do indicador e validação OHLC.','Precisão da medida varia; alta concentração Binance já documentada.','TESTAR','Quantificar cobertura por fonte e sensibilidade a janelas completas, sem excluir silenciosamente.','Tratar preços com suporte distinto como equivalentes.')
add('Fusos, dias disponíveis e controles defasados','Verificação concluída sem problemas','informativa','aprovado','fontes.binance / mercadobitcoin; janela; analise.montar_base','Candles UTC convertidos via America/Sao_Paulo; dias PTAX determinam a base; 11 VIX carregados de data anterior, atraso máximo três dias.','Replay, interseção de datas e auditoria de merge_asof backward.','Não há backfill futuro nessas junções; diferenças são por dias da base, não sessões americanas consecutivas.','DOCUMENTAR','Explicitar calendário observado e tratamento de feriados estrangeiros.','Confundir variação de um intervalo irregular com retorno diário homogêneo.')
add('VIX contemporâneo e previsão em tempo real','Limitação conhecida e adequadamente documentada','alta','confirmado','analise.montar_base:74; docs/resultados.md §9','Fechamento contemporâneo do VIX ocorre depois da janela do ágio; d_vix_ant é defasado na base brasileira.','Inspeção de disponibilidade informacional, sem nova coleta.','Regressão contemporânea é associativa ex post; não é previsão disponível às 13h.','DOCUMENTAR','Restringir linguagem a associação e testar especificação estritamente disponível em t−1 se houver objetivo preditivo.','Vazamento informacional se resultados forem usados como previsão intradiária.')
add('Repasse: indicador não identifica vendas para realizar ganhos','Risco metodológico','alta','potencial','analise.regressao_repasse; docs/resultados.md §5.1; pré-registro V6','Identidade de retornos verificada ≤3,84e−14; regressão de retorno USDT dá 0,8562 versus −0,1290 sobre ágio anormal.','Decomposição algébrica e três regressões suplementares.','Ágio anormal é nível relativo à mediana, não retorno. Soma −0,0798 não identifica motivo de negociação nem resposta causal acumulada.','DOCUMENTAR','Separar identidade, associação e mecanismo; preservar V4a/V4b/V6 como hipóteses registradas.','V6 pode confirmar padrão de sinal sem confirmar realização de ganhos.')
add('Holm e hipótese conjunta V1 na descoberta','Verificação concluída sem problemas','informativa','aprovado','analise.holm / quadro_hipoteses; hipoteses.csv','Sete hipóteses; comparação com statsmodels multipletests idêntica. V1 usa máximo dos dois p-valores e exige ambos sinais.','Verificação independente da ordenação, monotonicidade, família e decisões.','Holm pode ser usado sob dependência se p-valores marginais forem válidos; não corrige seleção anterior de análises.','MANTER','Manter quadro bruto+Holm e origem exploratória explícita.','Confundir controle desta família com correção dos cerca de 40 testes exploratórios.')
add('Regra de menos de dez eventos omite V1','Erro comprovado','alta','confirmado','analise.quadro_hipoteses:365','n_eventos só tem V2 e V5. Exemplo sintético com dois eventos gera V1=nao, em vez de inconclusivo; hipoteses_teste_2_eventos.csv.','Chamada sintética separada, sem mexer em testes ou dados oficiais.','Descoberta tem eventos suficientes; problema afeta implementação do plano futuro de validação.','CORRIGIR','Definir com pesquisador contagem mínima por braço e aplicar guarda V1 em mudança futura datada.','Resultado negativo indevido com amostra insuficiente.')
add('Família de Holm encolhe se V5 não estiver disponível','Erro comprovado','média','confirmado','analise.quadro_hipoteses:351','Entrada grupos_ajustado_isolados=None produz seis linhas, embora adendo defina sete hipóteses.','Teste de fronteira com ausência de grupo; verificacoes_finais.json.','Não afeta quadro atual; muda proteção múltipla em validação com eventos ausentes.','CORRIGIR','Preservar família registrada, registrando não testável explicitamente, em implementação autorizada.','Decisões futuras variam com disponibilidade de uma hipótese.')
add('V4b e V6 e avaliações sequenciais','Risco metodológico','alta','potencial','docs/pre-registro.md; analise.quadro_hipoteses','V4b e V6 usam o mesmo p bilateral, com sinais opostos; Holm inclui ambos. Intermediária 1% permite antecipar confirmação e final usa 5%, sem gasto alfa.','Confronto do adendo com código e lógica de testes repetidos.','Duplicidade não invalida Holm, mas não são evidências independentes. 1%+5% não garante erro familiar global de 5% entre análises.','DOCUMENTAR','Adendo futuro datado: família, bilateralidade, hipótese não estimável e regra sequencial explícita antes de analisar validação.','Confirmação antecipada pode elevar erro além do declarado; reinterpretação retrospectiva.')
add('Origem e temporalidade do pré-registro','Verificação inconclusiva por falta de evidência','média','inconclusivo','docs/pre-registro.md; histórico Git; brutos com carimbo de coleta','Introdução 2409cfa em 01/11/2026 09:04 −03; adendo c176bfd às 17:13. Diário mostra descobertas e mudança de lista após resultados.','Histórico de arquivo e comparação com datas declaradas, sem inferir ordem não registrada.','Git local não prova registro independente imutável nem prioridade exata da hipótese original; dados são vintages coletados depois do corte.','DOCUMENTAR','Preservar histórico e obter registro público/datado; distinguir descoberta e validação.','Apresentar toda descoberta como confirmatória pré-registrada.')
add('Robustez de significância não é uniformidade','Risco metodológico','alta','potencial','dados/resultados/robustez.csv; sensibilidade_regressoes.csv','VIX anterior 7/9 reproduzido, mas retirar cinco maiores Cook leva p=0,09984; subamostras posteriores p=0,347 e 0,500. Dólar pós-04/05 p=0,111.','HAC 5/10/20, influência 1/5/15 e três períodos fixos.','Não sustenta afirmação categórica não depende de poucos dias; sinais/tamanhos variam. Não prova quebra estrutural.','TESTAR','Reportar sensibilidade completa e, futuramente, testes conjuntos de estabilidade/poder.','Escolher só especificações significativas e confundir falta de poder com prova de estabilidade.')
add('Mediana desenhada difere do normal da regressão','Erro comprovado','média','confirmado','relatorio.fig_serie:72 versus analise._anormal:32','Gráfico usa rolling sem shift; legenda chama de normal usado no ágio anormal. Diferença máxima 0,0800594 p.p.','Comparação das duas séries com 1520 dias.','Afeta legenda/figura, não coeficientes ou base de análise.','CORRIGIR','Em tarefa futura, alinhar a curva ou corrigir a legenda de modo explícito.','Leitor atribui ao gráfico referência diferente da estatística.')
add('Contagem nominal de eventos nas trajetórias','Erro comprovado','média','confirmado','analise.trajetoria_evento:280,297; relatorio.fig_trajetorias:182','Rótulos fiscal=47, externo=54, monetário=48; valores efetivos não nulos por dia: 46–47,53,47.','Matrizes de −5 a +10, contagem de NaN por posição.','Faixa usa n nominal enquanto nanmean ignora valores ausentes; precisão e contagem não coincidem.','CORRIGIR','Exibir n efetivo por dia ou definir amostra completa comum em revisão autorizada.','Faixas e legendas podem superestimar informação.')
add('Significado das faixas de 95%','Risco metodológico','média','potencial','analise.trajetoria_evento; figuras 06,07,09','Percentis ponto a ponto de médias placebo; não são IC da média observada nem banda simultânea de trajetória. Figura 08 usa 1,96×EP; Huber não tem HAC.','Inspeção da geração, escalas e legendas nas dez figuras.','Cruzar a faixa em um dia não equivale a rejeitar teste CAR nem teste simultâneo.','DOCUMENTAR','Explicitar referência, n, exclusões por tipo, ausência de simultaneidade e IC assintótico da robustez.','Interpretar inspeção visual como novo teste confirmatório.')
add('Google Trends e textos antigos','Inconsistência documental','baixa','confirmado','docs/resultados.md:189,197; relatorio.tabelas; dados/resultados/exploratorio_*','Trends importado e reproduzido; duas figuras presentes; narrativa ainda diz não importado e enumera oito figuras. Quadro textual cita V3–V5, omite V6.','Confronto artefatos, histórico e narrativa.','Dificulta saber o que já foi analisado.','DOCUMENTAR','Atualizar por documento novo/errata autorizado, mantendo diário histórico e origem exploratória.','Leitor recebe estado desatualizado da pesquisa.')
add('Afirmações causais e irrelevância fiscal','Inconsistência documental','alta','confirmado','docs/resultados.md resumo, §§5,5.1,6,8; docs/decisoes.md','Texto usa não funciona como termômetro, é movido e vendas para realização. Juro de fechamento é negativo e significativo (p≈0,001); não positivo em nenhuma das nove especificações originais.','Confronto de frases com resultados e desenho observacional.','Não significância não prova inexistência; sinal de juro não isola choque fiscal; modelo não identifica comportamento.','DOCUMENTAR','Usar não confirmada nesta amostra e associação; preservar hipótese original e resultados contrários.','Conclusão do TCC extrapola evidência observacional.')
add('Unidade do volume no episódio','Erro comprovado','média','confirmado','docs/resultados.md §3.1; episodio.resumo; janela.volume_janela','17,1457→26,0686 milhões são volume_base em USDT, descritos como R$ 17,1→26,1 mi. Proxy de valor HLC3×volume: R$87,23→134,36 mi.','Rastreio da coluna desde candles até tabela narrativa.','Não altera aumento de volume em unidades base, mas erra escala monetária.','CORRIGIR','Corrigir unidade em errata futura; não confundir proxy monetária com volume_brl exato.','Erro factual na descrição de liquidez.')
add('Episódio: janela e mecanismo','Risco metodológico','alta','potencial','episodio.montar; docs/resultados.md §3.1','Tabela refere-se a 01/06–14/08 (54 dias), não só 24/06–meados de julho. Recorte suplementar 24/06–17/07: ágio Binance 1,052%, MB 0,733%, correlação 0,76.','Reprodução da janela original e diagnóstico alternativo explicitamente identificado.','Ágio persistente nas duas fontes é observado; escassez de vendedores e atrito específico não são identificados por ticket/taker.','DOCUMENTAR','Separar período de diagnóstico, núcleo do episódio e interpretação exploratória.','Atribuição de comportamento e médias a um período diferente.')
add('Oferta global: não significância não descarta escassez','Inconsistência documental','alta','confirmado','docs/resultados.md:76,196; analise.regressao_oferta_usdt','Coeficiente +0,031, p≈0,051 reproduzido; variável é 100 log(S_t/S_t−5), deslocada um dia de calendário. Texto afirma escassez global descartada.','Replay DefiLlama e regressão exploratória, inspeção temporal.','Sinal não sustenta hipótese negativa específica, mas não prova ausência de escassez ou oferta local suficiente.','DOCUMENTAR','Trocar inferência conclusiva por hipótese não sustentada nesta especificação; manter causa não identificada.','Refutação causal indevida com proxy global e erro de medida.')
add('Procedência e disponibilidade histórica dos dados','Verificação inconclusiva por falta de evidência','alta','inconclusivo','dados/bruto; fontes.defillama / tesouro / google_trends','Arquivos preservados e valores reproduzíveis, mas não há recibos assinados/vintages históricos de publicação; datas não provam hora de disponibilização real da oferta ou taxa da manhã.','Inspeção de arquivos, metadados e consultas externas somente metodológicas/de procedência.','Não certifica autenticidade independente de cada observação, dado em tempo real nem todas as notícias de 2026.','TESTAR','Completar cadeia de custódia e fontes primárias; não substituir silenciosamente histórico.','Confundir consistência interna com validação externa integral.')
add('Testes, dependências e preservação computacional','Oportunidade de melhoria','baixa','confirmado','pyproject.toml; tests/*; git_antes.txt; versoes.json','41 testes passaram; um warning de precisão em caso sintético. Dependências têm limites mínimos sem lock; dados principais não rastreados apesar do diário mencionar CSV versionado.','pytest isolado, inventário de versões e Git.','Ambiente atual reproduz; clone do commit sozinho não contém toda baseline.','DOCUMENTAR','Arquivar bundle de dados, hashes, versões e comandos; testes de fronteira em tarefa futura.','Clone futuro não reproduz e mudanças de biblioteca afetam execução.')
add('Figuras e tabelas regeneradas','Verificação concluída sem problemas','informativa','aprovado','relatorio.gerar; cli.buscas; episodio.rodar','Dez figuras solicitadas idênticas byte a byte; episódio também idêntico em processo separado; tabelas idênticas exceto data.','Regeneração, SHA-256/pixels e inspeção visual do contato; episódio em processo separado elimina rcParams herdados.','Concordância com gerador e dados, ressalvados erros semânticos acima.','MANTER','Manter arquivos oficiais; anotar ordem/processo de geração e ressalvas de legenda.','Igualdade de pixels não valida interpretação científica.')
counts=collections.Counter(f['gravidade'] for f in F);cats=collections.Counter(f['categoria'] for f in F);nerr=cats['Erro comprovado']
(O/'achados.json').write_text(json.dumps(F,ensure_ascii=False,indent=2))
header='# AUD-001 — Matriz de achados\n\nExecução de 02/11/2026. Commit `'+S['commit']+'`. Cada item é uma verificação auditável; aprovados e inconclusivos também constam para evitar silêncio sobre limitações. Gravidade é impacto, não certeza. “Potencial” não significa erro demonstrado.\n\n'
header+=md(pd.DataFrame([{k:f[k] for k in ['id','titulo','categoria','gravidade','situacao','acao']} for f in F]))+'\n'
for f in F:
 header+=f"\n## {f['id']} — {f['titulo']}\n\n- Categoria: {f['categoria']}. Gravidade: **{f['gravidade']}**. Situação: **{f['situacao']}**.\n- Arquivo/função: `{f['arquivo_funcao']}`.\n- Evidência objetiva e resultado observado: {f['evidencia']}\n- Procedimento executado: {f['procedimento']}\n- Impacto científico: {f['impacto']}\n- Necessidade de ajuste: {f['acao']}; nenhuma mudança aplicada.\n- Recomendação: {f['recomendacao']}\n- Risco de não ajustar: {f['risco']}\n"
(O/'AUD-001_MATRIZ_ACHADOS.md').write_text(header)
# Sensitivity document
reg=pd.read_csv(O/'sensibilidade_regressoes.csv');events=pd.read_csv(O/'sensibilidade_eventos.csv');rep=pd.read_csv(O/'decomposicao_repasse.csv');hip=pd.read_csv(R/'dados/resultados/hipoteses.csv')
sens='''# AUD-001 — Sensibilidade estatística

Todos os testes aqui denominados suplementares pertencem à auditoria. Não substituem especificação, evento, hipótese ou resultado original. Não houve busca de uma especificação significativa. HAC 5/10/20, exclusão dos 1/5/15 maiores Cook e três períodos de calendário foram apresentados integralmente, inclusive resultados contrários. São diagnósticos condicionais aos dados observados; p-valores suplementares não receberam correção global de multiplicidade e não são confirmações novas.

## Regressões: original e HAC suplementar

HAC(5) é original. Todos têm n=1490 e os mesmos coeficientes; apenas a matriz de covariância muda. IC de 95% normal assintótico, Bartlett, sem correção de pequena amostra. Unidades: ágio anormal em p.p.; dólar em 100×retorno log; juro em bp; VIX em pontos; mercado em log do volume mediano anterior.

'''+md(reg[reg.teste.str.startswith('HAC')])+'''

O dólar continua negativo; VIX contemporâneo e anterior continuam positivos a 5%. Juro continua não significativo a 5%; com HAC20 também ultrapassa 10%. Isso não prova ausência de efeito fiscal. O controle log_mercado perde o limiar de 10% com 10/20 defasagens.

## Influência e estabilidade: somente suplementos

'''+md(reg[~reg.teste.str.startswith('HAC')])+'''

05/08/2024 tem Cook≈0,8155 (influencia.csv). Remover essa observação reduz o coeficiente VIX contemporâneo de 0,02123 para 0,01116; retirar cinco maiores Cook leva VIX anterior a 0,00639 (p=0,09984). Retirar quinze produz p=0,02213: a sensibilidade não é monotônica. Juro passa p=0,03987 ao retirar um caso e p=0,15414 ao retirar cinco: não selecionar uma dessas versões como evidência confirmatória. Exclusão por influência depende da resposta e altera o estimando; a covariância HAC também passa a operar sobre sequência com observações removidas. Preferir ler estes resultados como diagnóstico.

Os três períodos mostram dólar sempre negativo, com magnitude menor no fim; VIX anterior passa de 0,0251 para 0,00253. Diferença de significância entre períodos não é teste de diferença de coeficientes. Não declaramos quebra estrutural. As nove robustezes originais foram recalculadas integralmente em robustez_recalculada_auditoria.csv: diferença máxima zero. Huber não tem HAC. O juro do fechamento é negativo/significativo; o dólar pós-04/05/2026 tem p=0,111, portanto “forte em todas” não deve ser lido como “significativo em todas”.

## Eventos: desenho e resultados lado a lado

Original: 5000 sorteios, semente 42; CAR soma cinco níveis anormais (−1,+3); p bilateral. Datas placebo com reposição e exclusão de ±4 posições de eventos elegíveis da lista fornecida. Rótulos doméstico/externo embaralhados mantendo tamanhos dos grupos. A docstring ainda menciona ±10, mas constante e execução são ±4. CAR é área discreta do prêmio anormal, em p.p. somados ao longo de cinco dias, não retorno acumulado de um ativo.

Suplementos: 5000 sorteios, semente 20261102 (gerador sequencial no script), p=(1+b)/(5001). Não constituem randomização verdadeira dos choques:

1. **Rótulos dentro do ano:** preserva contagem doméstica/externa anual, centra CAR pela média dos eventos do ano e permuta dentro de ano. A estatística centrada difere da diferença bruta porque controla composição anual. Ainda não resolve dependência entre eventos nem heterogeneidade dentro de ano.
2. **Deslocamento circular anual dos CARs:** desloca conjuntamente a série de somas de cinco dias em cada ano por pelo menos 20 posições válidas, preservando boa parte da dependência e o calendário relativo dos eventos. Teste contra centro empírico da distribuição, que pode ser não zero. O corte circular cria emendas e supõe comparabilidade dentro de ano; não é teste exato.
3. **Placebos anuais para todos os eventos:** mantém número de eventos por ano e exclui a vizinhança de toda a lista original; amostragem com reposição. Não respeita toda dependência entre CARs. Não é o contraste domésticos–externos.

'''+md(events)+'''

Na lista completa, a ausência de evidência de diferença permanece. Na lista isolada ajustada, p original=0,033; rótulos anuais p=0,09418 e deslocamento circular p=0,13577. A evidência não se mantém a 5% nessas alternativas. Não significa que a diferença seja zero. No anormal isolado, p=0,0526 originalmente, versus 0,14957/0,18036 nos suplementos. IC dos contrastes não foi estimado: percentis da distribuição nula não foram rotulados como IC do efeito. EP Monte Carlo aproximado no original p=0,033 é 0,00253 (intervalo de precisão aproximado ±0,00495 a 95%).

Apenas recalcular os rótulos de sobreposição pelo calendário PTAX, em memória, deixa 60 eventos isolados (32 domésticos,14 externos e14 monetários): anormal diferença=0,83846/p=0,0434; ajustado=0,85480/p=0,0306. Esse diagnóstico revela a consequência do erro de calendário; não autoriza escolher o resultado mais significativo e não modifica eventos.csv.

## Repasse: identidade e estimandos diferentes

Se A=P/X−1, então log(P_t/P_{t−1})−log(X_t/X_{t−1})=log(1+A_t)−log(1+A_{t−1}). A identidade foi verificada com preço consolidado implícito P=X(1+A), erro máximo 3,84e−14 em 100×log. Esse preço agrega corretoras com pesos variáveis; não é necessariamente um preço transacionável único. Já ágio anormal=100A−mediana anterior de 100A. Portanto regressão em ágio anormal não equivale à regressão em retorno nem à variação diária do ágio.

'''+md(rep[rep.variavel=='d_dolar'])+'''

Com controles idênticos, coeficiente do retorno USDT é 0,85621 e da variação do ágio é −0,14431; o ágio anormal dá −0,12900. São associações, não elasticidades causais identificadas. Soma original dos lags 1–3=−0,07978, p=0,00025397; somar contemporâneo e lags não transforma a equação em resposta causal acumulada. V4b/V6 compartilham estatística, não identificam motivo de venda. Os valores-p originais são bilaterais mais verificação do sinal, não unilaterais.

## Hipóteses e multiplicidade

'''+md(hip)+'''

V1/V2 são originais do TCC conforme diário; V3/V4a/V5 derivam da descoberta; V4b foi formulada para validação e o adendo registra seu resultado contrário; V6 deriva desse resultado em 01/11/2026. V4b e V6 têm p e Holm idênticos, com sinais opostos: apenas uma pode confirmar pelo sinal. A dependência não invalida o algoritmo de Holm, mas o conjunto não oferece sete evidências independentes. V6 também tem confirma_holm=sim na descoberta, embora o resumo textual mencione só V3/V4a: nenhum desses “sim” é confirmação fora da amostra.

A escolha de eventos/modelos após observar a descoberta não é corrigida por Holm sobre apenas sete hipóteses. A inferência sequencial planejada também não foi calibrada: duas oportunidades de decisão com 1%/5% não garantem conjuntamente 5%; o limite de união é até 6%, não uma estimativa de erro efetivo. Recomendação é esclarecer via adendo futuro o orçamento de erro e a interpretação da intermediária. Nenhum pré-registro foi editado.
'''
(O/'AUD-001_SENSIBILIDADE.md').write_text(sens)
# Reproduction and traceability
cmp=pd.read_csv(O/'comparacoes.csv');ver=json.loads((O/'versoes.json').read_text())
trace=[
['BCB Olinda/SGS','dados/bruto/bcb_ptax, bcb_selic','fontes.bcb.tratar_ptax/tratar_sgs; atualizar_tratado','ptax.csv, selic.csv','indicador e d_dolar','ágio, regressões, figs 01–05','reproduzido; Selic não integra regressão principal'],
['Binance e Mercado Bitcoin','dados/bruto/{binance,mercadobitcoin} e *_1h','tratar/tratar_horario; janela.preco_janela_ptax','precos_usdt_brl; precos_janela_ptax','HLC3×volume, ágio; sinais_mercado','agio_*; painel; figs 01–07','reproduzido; índice duplicado bloqueia CLI robustez'],
['Tesouro Transparente','dados/bruto/tesouro_direto/*.csv','tesouro.tratar; juro_real_10a','juro_real_10a.csv','diferença×100 bp; MQO/HAC','regressao_*; fig08','reproduzido; vintage não comprova hora de publicação'],
['Cboe (fallback FRED)','dados/bruto/cboe_vix/*.csv','fred.tratar_cboe; merge_asof backward','vix.csv','d_vix e shift anterior','regressões, robustez','reproduzido; contemporâneo ex post'],
['Google Trends manual','dados/manual/google_trends/*.csv','ler_csv; encadear razão de médias de sobreposição','google_trends; painel','log1p, mediana anterior; buscas','exploratorio_atencao/eventos; 09_buscas_*','reproduzido; comprar dólar excluído por suporte insuficiente'],
['DefiLlama','dados/bruto/defillama_usdt/*.json','defillama.tratar; regressao_oferta_usdt','usdt_oferta.csv','log retorno 5 observações diárias, +1 dia calendário','exploratorio_oferta_usdt; episódio','reproduzido; latência histórica não provada'],
['Calendários/notícias/prazos','scripts/montar_eventos.py; manual/eventos.csv','montar; _posicoes_eventos; _car','158 cadastrados,154 elegíveis','−1,+3; placebos; rótulos; trajetórias','eventos_*.csv; figs 04,06,07,09','script igual célula a célula; calendário de sobreposição tem erro'],
['Tratados anteriores','14 CSVs tratados','analise.montar_base; _anormal; ajustar_pelo_dolar','base_teste; base_buscas','MQO, HAC, repasse, Holm','resultados/*.csv; resultados_tabelas.md','comuns exatos; quatro colunas Trends ausentes na base antiga']]
repro=f'''# AUD-001 — Reprodutibilidade e rastreabilidade

## Snapshot e ambiente

Branch `main`; commit `{S['commit']}`. Git não apresentava alterações em arquivos rastreados, mas havia numerosos arquivos não rastreados preexistentes (brutos, tratados, resultados e .DS_Store). Relação integral em git_antes.txt. Auditoria é somente diretório novo `auditorias/AUD-001/`; não houve commit, push, coleta remota, mudança em src/tests/dados/docs/scripts ou instalação de dependências.

Snapshot de **154 arquivos** fora de .git/.venv/caches/auditorias: hashes_antes.json e hashes_depois.json. Esses arquivos incluem código, documentação, figuras, manuais e todos os brutos/tratados/resultados encontrados. Integridade final: ver integridade_final.json. Hash prova preservação do conteúdo local, não autenticidade da fonte externa. Git, caches e ambiente virtual não são tratados como dados científicos protegidos.

Python `{ver['python']}`; `{ver['platform']}`.

{md(pd.DataFrame(ver['packages'].items(),columns=['pacote','versão']))}

O pyproject aceita Python≥3.10 e dependências sem limite superior. Não foi validada compatibilidade de todas as versões permitidas (por exemplo, uso de include_groups depende da versão pandas). O ambiente acima é a evidência efetiva, sem atualização de pacote.

## Isolamento e comandos

Cópia temporária em `{T}`. Módulos importados exclusivamente de `{T}/src`; Python do ambiente existente. Rede de requests bloqueada explicitamente no replay. Nenhum endpoint de dados foi consultado. Brutos foram ordenados por carimbo de coleta, último lote prevalece por chave; observações posteriores a 30/10/2026 foram removidas antes da construção final. Para Trends, janelas também foram cortadas antes de encadear. As coletas são vintages de 01/11/2026; isso não certifica informação disponível em tempo real no passado.

Comandos e chamadas efetivamente utilizados:

```text
git status --short --untracked-files=all
git branch --show-current
git rev-parse HEAD
git log --reverse --format=... -- docs/pre-registro.md
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=<temporário>/mpl <repo>/.venv/bin/python <temporário>/reproduzir.py
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=<temporário>/mpl PYTHONPATH=<temporário>/src <repo>/.venv/bin/python -m pytest -q -p no:cacheprovider
PYTHONDONTWRITEBYTECODE=1 <repo>/.venv/bin/python <temporário>/suplementar.py
PYTHONDONTWRITEBYTECODE=1 <repo>/.venv/bin/python <temporário>/complementar.py
PYTHONDONTWRITEBYTECODE=1 <repo>/.venv/bin/python <temporário>/verificacoes_finais.py
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=<temporário>/mpl PYTHONPATH=<temporário>/src <repo>/.venv/bin/python -m agio.cli episodio --inicio 2026-06-01 --fim 2026-08-15
```

Scripts exatos estão anexos nesta pasta. Eles usam o estado em `/private/tmp/AUD-001-state.json` (conteúdo em ambiente.json); para nova execução, criar **outra** pasta de auditoria e outra cópia temporária, atualizar esse estado e copiar os scripts para a nova cópia. Não executar sobre a baseline. `reproduzir.py` chama calcular, testar, robustez (captura falha), oferta_usdt(coletar=False), buscas, relatorio e episodio. `complementar.py` é necessário para distinguir a cópia antiga de robustez de recálculo efetivo e comparar colunas comuns da base. Scripts não são alterações da aplicação.

Antes do replay definitivo houve duas falhas no script auxiliar: um parêntese excedente e concatenação de lotes sem normalizar índices do objeto local. Foram corrigidas somente no auxiliar temporário. A mesma falha de índices foi então demonstrada no comando original robustez e preservada no log. Não confundir esses eventos com corrupção da baseline.

**Comandos que sobrescrevem:** coletar, coletar-horario, coletar-controles e oferta-usdt padrão também acessam rede; não foram usados. calcular/importar-trends escrevem tratados; testar/robustez/buscas/oferta-usdt --sem-coleta/episodio escrevem resultados; relatorio/grafico escrevem figuras/documentação; montar_eventos.py escreve lista. Todas as chamadas com escrita foram executadas somente na cópia. Script de eventos foi importado para comparação em memória.

## Mapa de rastreabilidade

{md(pd.DataFrame(trace,columns=['Fonte','Bruto/insumo','Transformação','Saída/variável','Análise/regra','Resultado/figura','Situação']))}

Inventário físico completo: inventario_arquivos.csv; cobertura, faltantes e duplicidades por tabela: inventario_dados.json; validação de candles: horarios.json. Os preços diários mantêm datas de abertura UTC e fecham aproximadamente às 21h de Brasília; negócios/ticket usam o dia completo, incluindo horas posteriores à janela PTAX. Não devem ser lidos como comportamento exclusivamente durante a janela.

## Comparação quantitativa

Tolerância declarada: `abs(a-b) ≤ 1e-10 + 1e-8×abs(b)`, NaN apenas igual a NaN; diferenças relativas usam denominador mínimo 1e−12 para evitar divisão por zero. São tolerâncias de arredondamento, não econômicas. As tabelas que coincidiram tiveram diferença observada zero, inclusive coeficientes, EP e p-valores. Comparação matricial independente admite arredondamento numérico (máximo 2,38e−14 para covariância).

{md(cmp[['arquivo','n_original','n_reproduzido','divergencias','max_abs','status']])}

Resumo: **14 tratados** exatos; **30 resultados CSV** reproduzidos diretamente; **uma base** com 17 colunas comuns exatas e quatro Trends novas; **uma robustez** cuja CLI falha, mas nove linhas recalculadas com funções coincidem exatamente. São 46 CSVs oficiais examinados. A linha inicial de comparação de robustez era uma cópia preservada: NÃO foi contada como replay da CLI. Evidência autônoma está em robustez_recalculada_auditoria.csv e complementos.json.

Comparacoes_colunas.csv contém nulos implícitos via comparação, mínimos/máximos/médias, diferenças absolutas e relativas por coluna. Não houve divergência de datas nos tratados recortados. PTAX tem 1527 dias desde 01/10/2020; sete dias anteriores ao início de negociação em 13/10 não entram no ágio. Ágio=1520 dias, regressão=1490 após mínimo de 30 dias. Para MB isolado, anormal é reconstruído na própria série e há 884 observações, não uma amostra emparelhada à Binance.

## Exclusões de eventos

{md(pd.DataFrame(d['excluidos']))}

No evento fiscal cadastrado 21/11/2020 (sábado), a data efetiva é 23/11; a janela ainda inclui dia sem anormal. As quatro exclusões valem para os resultados principais auditados. Cadastro não tem duplicata exata data/tipo/descrição; eventos distintos na mesma data são mantidos. 23 datas cadastradas são mapeadas ao próximo dia disponível, registrado em reconciliacao_eventos.csv. Lista completa elegível: fiscal46, político4, externo53, monetário47, regulatório4. Sem sobrepostos cadastrados:62. Todos os 158 eventos do script coincidem com o CSV, sem alteração manual detectável.

## Figuras, testes e limites

Dez figuras solicitadas reproduzidas com SHA idêntico e inspecionadas visualmente em contato_figuras.png. Figura adicional do episódio também idêntica quando gerada em processo separado: a primeira execução no mesmo processo herdou rcParams de relatorio, alterando aparência, não dados (episodio_render.json). Figura 05 mostra reta simples sem controles, corretamente distinta do coeficiente multivariado. Figura 08 usa os EPs oficiais, conferidos pelo recálculo. Figuras 06/07/09 usam −5,+10 e faixa placebo, não a mesma amostra/estatística do CAR −1,+3. Defeitos de legenda, n e medianas estão classificados na matriz.

**41 testes existentes passaram**, um warning de perda de precisão em dados sintéticos quase constantes. Nenhum teste da baseline foi alterado. Não foram executados testes de rede, novas coletas, validação fora da amostra ou afirmação de completude de todas as fontes primárias. Suplementos estão em scripts próprios, não em tests/.

Não declaramos reprodução integral automatizada do pipeline: a CLI robustez falha. Tampouco certificamos publicação histórica de cada dado, horários efetivos de todo anúncio fiscal, autenticidade externa de toda observação ou validação empírica 2027/2028. A reprodução local dos números é ampla e delimitada, não um certificado de validade causal.

## Fontes externas consultadas somente como documentação/metadados

Consulta em 02/11/2026; nenhum valor externo foi incorporado à amostra. BCB descreve quatro consultas com a última após 13h; isso sustenta a ressalva de janela aproximada: [BCB, metodologia PTAX](https://www.bcb.gov.br/detalhenoticia/12847/nota) e [REB 2018, seção PTAX](https://www.bcb.gov.br/content/publicacoes/relatorioeconomiabancaria/reb_2018.pdf). O calendário institucional confirma reunião FOMC em 27–28/10/2026, compatível com evento em 29/10: [Federal Reserve Bank of Chicago](https://www.chicagofed.org/utilities/about-us/federal-reserve-calendars). A norma oficial prevê informações para operações a partir de 03/11/2026; sua vigência é publicação: [Resolução BCB 574](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?numero=574&tipo=Resolu%C3%A7%C3%A3o+BCB). Não se certificou o horário da notícia de 18/06.

Para inferência, [documentação de HAC](https://www.statsmodels.org/dev/generated/statsmodels.stats.sandwich_covariance.cov_hac.html) foi usada como referência de método; defaults efetivos vieram do modelo instalado, não do default dessa função isolada. A ressalva do p Monte Carlo se apoia no artigo original [Phipson e Smyth](https://arxiv.org/abs/1603.05766). Consultas atuais são metadados de verificação e não reconstrução de dados posteriores ao corte.
'''
(O/'AUD-001_REPRODUTIBILIDADE.md').write_text(repro)
# Prioritized action plan with explicit research approval; no ask or changes.
plan='''# AUD-001 — Plano de ajustes para decisão do pesquisador

Nenhuma correção implementada. Este plano separa erro demonstrado de escolhas metodológicas defensáveis. Todos os itens que alterem baseline, pré-registro, classificação ou texto original dependem de autorização expressa do pesquisador em tarefa futura. Adendos devem ser datados, com versão original preservada; nenhuma hipótese deve ser reformulada retrospectivamente para coincidir com resultados.

Prioridade P1: antes de apresentação como resultado final ou inferência confirmatória; P2: melhorar auditabilidade e robustez; P3: manutenção. CORRIGIR aplica-se apenas a falhas demonstradas. DOCUMENTAR não deve apagar o histórico do diário.

'''
for f in sorted(F,key=lambda f:({'alta':0,'média':1,'baixa':2,'informativa':3}[f['gravidade']],f['id'])):
 pri='P1' if f['gravidade']=='alta' else 'P2' if f['gravidade']=='média' else 'P3'
 plan+=f"## {f['id']} — {f['acao']} — {pri}\n\n- Item: {f['titulo']}.\n- Justificativa: {f['evidencia']}\n- Arquivos potencialmente envolvidos: `{f['arquivo_funcao']}`.\n- Ação proposta: {f['recomendacao']}\n- Efeito esperado: {f['impacto']}\n- Risco científico se mantido sem tratamento: {f['risco']}\n- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.\n- Aprovação do pesquisador: {'não há mudança proposta; necessária somente se ampliar escopo' if f['acao']=='MANTER' else 'sim, antes de qualquer alteração ou adoção de nova especificação; não solicitada nesta auditoria'}.\n"
plan+='''
## ADIAR — P2 — Identificação do mecanismo e confirmação fora da amostra

- Justificativa: agregados de negócios/taker/ticket e oferta global não identificam decisões individuais, escassez de vendedores ou arbitragem local.
- Arquivos potenciais: documentos novos do projeto e protocolo futuro; preservar V4a/V4b/V6 e descoberta.
- Efeito esperado: separar confirmação de padrão estatístico da identificação causal do mecanismo.
- Risco científico: antecipar explicações como fatos ou chamar repetição de sinais de prova de motivação.
- Dependências: dados microestruturais e estratégia de identificação; amostra futura; financiamento/acesso, se pertinente.
- Aprovação do pesquisador: sim, para novo desenho. Nenhuma coleta proposta foi iniciada.

Alternativas defensáveis incluem pré-especificar um único teste final, orçamento alfa entre avaliações ou método sequencial calibrado. Não foi escolhida unilateralmente uma nova baseline. Para eventos, permutação por ano melhora comparabilidade temporal, mas pode perder poder e não elimina dependência; deslocamentos conjuntos preservam mais dependência, mas supõem estabilidade dentro de período. Decisão deve levar em conta pergunta científica, não o menor p.
'''
(O/'AUD-001_PLANO_AJUSTES.md').write_text(plan)
# Executive report and explicit acceptance matrix
ex=f'''# AUD-001 — Relatório executivo

**Parecer: os números centrais da descoberta são reproduzíveis, mas o TCC requer ajustes antes de ser apresentado como metodologicamente pronto.** A ausência de confirmação fiscal deve ser preservada como resultado válido; não autoriza concluir irrelevância fiscal. Os dados não identificam realização de ganhos, falta de vendedores ou causa local específica do episódio de 2026.

Auditoria de 02/11/2026, branch main, commit `{S['commit']}`. Objetivo: verificar integridade, reconstrução, inferência e coerência, preservando integralmente o histórico de descoberta de 13/10/2020 a 30/10/2026. Escopo: todos os módulos de coleta/transformação/análise/relatório, 46 CSVs oficiais, 158 eventos, dez figuras solicitadas e uma adicional, pré-registro/diário/narrativa e 41 testes existentes. Dados brutos foram reutilizados; não houve novas consultas de séries históricas.

## Contagens e síntese

**{len(F)} verificações registradas na matriz**, além dos 41 testes automatizados existentes (todos aprovados). As contagens abaixo incluem verificações aprovadas e inconclusivas; não são {len(F)} erros.

{md(pd.DataFrame([{'gravidade':g,'quantidade':counts[g]} for g in ['crítica','alta','média','baixa','informativa']]))}

{md(pd.DataFrame(cats.items(),columns=['classificação','quantidade']))}

Não foi demonstrado achado crítico que invalide toda a amostra. Há **{nerr} erros comprovados** de implementação/apresentação, com alcance delimitado abaixo. Riscos potenciais não foram promovidos a erros confirmados.

## Principais achados

1. CLI robustez falha com os lotes atuais por índices pandas duplicados. Nove especificações recalculadas em memória coincidem com as oficiais: falha de execução não é evidência de coeficientes incorretos.
2. Copom 28/10/2021 e Fed 04/11/2021 estão incorretamente marcados como não sobrepostos no calendário efetivo.
3. Mediana da Figura 01 inclui o próprio dia, apesar de ser descrita como normal usado no anormal; a análise estatística exclui corretamente esse dia.
4. Rótulos de n nas trajetórias contam eventos cujos valores são NaN; n efetivo é menor e por vezes varia ao longo da curva.
5. Volume do episódio está descrito em reais, mas representa USDT.
6. V1 não aplica a regra registrada de insuficiência de eventos; exemplo com dois eventos retorna nao em vez de inconclusivo. Afeta validação futura, não a contagem atual.
7. Família de Holm cai de sete para seis hipóteses quando V5 não é estimável; o quadro atual com sete está correto.

## Resultados que podem ser mantidos

Amostra: 1520 dias, 1490 na regressão principal. Dólar −0,128997 (p≈8,93e−22); juro +0,001927 (p=0,08756); VIX +0,021235 (p=0,04682); VIX anterior +0,015634 (p=0,007836). R²=0,09535 e curtose residual=15,3378. HAC independente e mediana independente confirmaram cálculos. Holm das sete hipóteses atuais é correto.

As quatro exclusões estão reconciliadas: Copom 29/10/2020, Fed 06/11/2020 e fiscal 21/11/2020 por falta de histórico/janela; Fed 29/10/2026 por janela posterior incompleta. Domésticos são apenas fiscal/político, conforme desenho. Os 154 eventos não indicam perda silenciosa inexplicada.

Os 14 tratados, 30 resultados diretamente regenerados e nove especificações recalculadas coincidem no recorte; a base_teste reproduz todas as colunas antigas e acrescenta quatro colunas Trends. Dez figuras solicitadas e a figura do episódio foram reproduzidas byte a byte (episódio em processo separado). Isso confirma rastreabilidade dos gráficos, não sua validade interpretativa.

## Sensibilidades e riscos científicos

- Comparação isolada ajustada: diferença +0,7974, p original=0,033. Permutação dentro de ano: estatística centrada +0,5854, p=0,09418; deslocamento circular anual: diferença bruta +0,7974, p=0,13577. Evidência é sensível à referência temporal, sem prova de efeito nulo.
- HAC10/20 preserva sinais principais, mas retirada dos cinco casos de maior Cook leva VIX anterior a p=0,09984. Não selecionar esse suplemento nem a versão original por significância; reportar a sensibilidade.
- VIX contemporâneo é informação posterior à janela PTAX. A limitação já era reconhecida. Resultados são associações ex post, sem identificação causal.
- A família Holm atual está correta, mas não desfaz exploração anterior nem resolve decisões intermediária/final com 1%/5%. V4b/V6 são sentidos opostos da mesma estatística.
- Ágio anormal é nível relativo à mediana; repasse exige separar identidade matemática de retorno, associação observada e mecanismo. Não inferir vendas para realização de ganhos.
- Junho/julho apresenta prêmio persistente em ambas as fontes; o teste de oferta global não autoriza descartar escassez. Médias publicadas abrangem junho–meados de agosto, não apenas o núcleo de alta.

## Recomendações prioritárias

**P1:** resolver futuramente falha de robustez e calendário de sobreposições; corrigir regras de elegibilidade/família para validação; publicar errata metodológica para causalidade, mecanismo, não significância e regra sequencial; verificar fontes/horários fiscais pendentes. Qualquer mudança depende do pesquisador e deve preservar o original.

**P2:** alinhar legenda/mediana, n efetivo, unidades do episódio e conceitos de faixas; apresentar sensibilidades e métricas de cobertura; identificar vintages e proveniência. **P3:** registrar bundle de dados/versões e atualizar estado documental do Trends. Nenhuma correção foi aplicada.

## Limitações e situação dos critérios de aceite

{md(pd.DataFrame([
[1,'Baseline preservada','Atendido; SHA-256 antes/depois'],[2,'Commit identificado','Atendido'],[3,'Hashes comparados','Atendido; integridade_final.json'],[4,'Pipeline reproduzido ou limites documentados','Atendido com ressalva: CLI robustez falha; números recalculados'],[5,'Quatro exclusões explicadas','Atendido'],[6,'Permutações examinadas','Atendido; suplementos e limites registrados'],[7,'Domésticos versus externos auditado','Atendido'],[8,'Repasse avaliado','Atendido; mecanismo não identificado'],[9,'Hipóteses/Holm verificados','Atendido; falhas de fronteira e regra sequencial registradas'],[10,'Figuras/tabelas confrontadas','Atendido; dez figuras + episódio'],[11,'Achados classificados','Atendido'],[12,'Ajustes separados da baseline','Atendido'],[13,'Implementação não modificada','Atendido'],[14,'Sem commits/pushes','Atendido']],columns=['critério','requisito','situação']))}

A entrega da auditoria cobre os critérios, mas **não constitui aprovação metodológica integral nem reprodução integral sem ressalvas do comando de pipeline**. Permanecem inconclusivas a autenticidade externa de cada dado/horário, todas as datas fiscais efetivas e a prioridade histórica independente das hipóteses. Não se produziu validação fora da amostra. A lista completa de limitações está na matriz/reprodutibilidade.

## Parecer final

**Pronto para discutir resultados de descoberta com ressalvas explícitas; ainda não pronto para conclusão causal ou confirmação definitiva das hipóteses.** Após resolver erros demonstrados e ambiguidades de protocolo/documentação, reavaliar prontidão sem exigir significância fiscal ou global. Os resultados não significativos podem e devem permanecer. Causa do episódio e motivação comportamental devem permanecer questões abertas.

## Entregáveis

- AUD-001_RELATORIO_EXECUTIVO.md
- AUD-001_MATRIZ_ACHADOS.md
- AUD-001_REPRODUTIBILIDADE.md
- AUD-001_SENSIBILIDADE.md
- AUD-001_PLANO_AJUSTES.md

Anexos CSV/JSON/logs/scripts preservam evidência e parâmetros. Hashes finais confirmam preservação dos 154 arquivos protegidos; somente esta pasta de auditoria foi criada, sem commits/pushes.
'''
(O/'AUD-001_RELATORIO_EXECUTIVO.md').write_text(ex)
print('verificações',len(F),'gravidades',dict(counts),'categorias',dict(cats))
