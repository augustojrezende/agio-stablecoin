# AUD-001 — Matriz de achados

Execução de 02/11/2026. Commit `543fdea26bc734fbea6d0fa712e5213c0d75d06a`. Cada item é uma verificação auditável; aprovados e inconclusivos também constam para evitar silêncio sobre limitações. Gravidade é impacto, não certeza. “Potencial” não significa erro demonstrado.

| id | titulo | categoria | gravidade | situacao | acao |
|---|---|---|---|---|---|
| AUD-001-01 | Integridade física da baseline | Verificação concluída sem problemas | informativa | aprovado | MANTER |
| AUD-001-02 | Reconstrução dos tratados | Verificação concluída sem problemas | informativa | aprovado | MANTER |
| AUD-001-03 | Indicador, unidades e mediana causal no tempo | Verificação concluída sem problemas | informativa | aprovado | MANTER |
| AUD-001-04 | Regressão principal e HAC | Verificação concluída sem problemas | informativa | aprovado | MANTER |
| AUD-001-05 | Regressões complementares, eventos e tabelas | Verificação concluída sem problemas | informativa | aprovado | MANTER |
| AUD-001-06 | Falha do comando robustez com os lotes existentes | Erro comprovado | alta | confirmado | CORRIGIR |
| AUD-001-07 | Base estatística oficial anterior à inclusão de Trends | Inconsistência documental | baixa | confirmado | DOCUMENTAR |
| AUD-001-08 | Reconciliação de 158 para 154 eventos | Verificação concluída sem problemas | informativa | aprovado | DOCUMENTAR |
| AUD-001-09 | Definição de domésticos e externos | Verificação concluída sem problemas | informativa | aprovado | MANTER |
| AUD-001-10 | Sobreposição calculada no calendário errado | Erro comprovado | alta | confirmado | CORRIGIR |
| AUD-001-11 | Dependência e comparabilidade nos testes de eventos | Risco metodológico | alta | potencial | TESTAR |
| AUD-001-12 | Universo placebo muda ao excluir sobrepostos | Risco metodológico | alta | potencial | TESTAR |
| AUD-001-13 | Precisão Monte Carlo e cálculo b/B | Risco metodológico | média | potencial | TESTAR |
| AUD-001-14 | Datas e horários de eventos fiscais | Limitação conhecida e adequadamente documentada | alta | potencial | TESTAR |
| AUD-001-15 | Janela PTAX é aproximação | Limitação conhecida e adequadamente documentada | média | confirmado | DOCUMENTAR |
| AUD-001-16 | Candles incompletos e cobertura de corretoras | Risco metodológico | média | potencial | TESTAR |
| AUD-001-17 | Fusos, dias disponíveis e controles defasados | Verificação concluída sem problemas | informativa | aprovado | DOCUMENTAR |
| AUD-001-18 | VIX contemporâneo e previsão em tempo real | Limitação conhecida e adequadamente documentada | alta | confirmado | DOCUMENTAR |
| AUD-001-19 | Repasse: indicador não identifica vendas para realizar ganhos | Risco metodológico | alta | potencial | DOCUMENTAR |
| AUD-001-20 | Holm e hipótese conjunta V1 na descoberta | Verificação concluída sem problemas | informativa | aprovado | MANTER |
| AUD-001-21 | Regra de menos de dez eventos omite V1 | Erro comprovado | alta | confirmado | CORRIGIR |
| AUD-001-22 | Família de Holm encolhe se V5 não estiver disponível | Erro comprovado | média | confirmado | CORRIGIR |
| AUD-001-23 | V4b e V6 e avaliações sequenciais | Risco metodológico | alta | potencial | DOCUMENTAR |
| AUD-001-24 | Origem e temporalidade do pré-registro | Verificação inconclusiva por falta de evidência | média | inconclusivo | DOCUMENTAR |
| AUD-001-25 | Robustez de significância não é uniformidade | Risco metodológico | alta | potencial | TESTAR |
| AUD-001-26 | Mediana desenhada difere do normal da regressão | Erro comprovado | média | confirmado | CORRIGIR |
| AUD-001-27 | Contagem nominal de eventos nas trajetórias | Erro comprovado | média | confirmado | CORRIGIR |
| AUD-001-28 | Significado das faixas de 95% | Risco metodológico | média | potencial | DOCUMENTAR |
| AUD-001-29 | Google Trends e textos antigos | Inconsistência documental | baixa | confirmado | DOCUMENTAR |
| AUD-001-30 | Afirmações causais e irrelevância fiscal | Inconsistência documental | alta | confirmado | DOCUMENTAR |
| AUD-001-31 | Unidade do volume no episódio | Erro comprovado | média | confirmado | CORRIGIR |
| AUD-001-32 | Episódio: janela e mecanismo | Risco metodológico | alta | potencial | DOCUMENTAR |
| AUD-001-33 | Oferta global: não significância não descarta escassez | Inconsistência documental | alta | confirmado | DOCUMENTAR |
| AUD-001-34 | Procedência e disponibilidade histórica dos dados | Verificação inconclusiva por falta de evidência | alta | inconclusivo | TESTAR |
| AUD-001-35 | Testes, dependências e preservação computacional | Oportunidade de melhoria | baixa | confirmado | DOCUMENTAR |
| AUD-001-36 | Figuras e tabelas regeneradas | Verificação concluída sem problemas | informativa | aprovado | MANTER |

## AUD-001-01 — Integridade física da baseline

- Categoria: Verificação concluída sem problemas. Gravidade: **informativa**. Situação: **aprovado**.
- Arquivo/função: `Repositório; hashes_antes.json / hashes_depois.json`.
- Evidência objetiva e resultado observado: 154 arquivos protegidos, inclusive não rastreados; comparação final em integridade_final.json.
- Procedimento executado: Inventário SHA-256 antes e depois; Git antes/depois.
- Impacto científico: Preserva história e separa novos artefatos.
- Necessidade de ajuste: MANTER; nenhuma mudança aplicada.
- Recomendação: Manter o snapshot e os manifests desta execução.
- Risco de não ajustar: Perda de rastreabilidade se descartados.

## AUD-001-02 — Reconstrução dos tratados

- Categoria: Verificação concluída sem problemas. Gravidade: **informativa**. Situação: **aprovado**.
- Arquivo/função: `fontes/*.py; janela.py; indicador.py; comportamento.py`.
- Evidência objetiva e resultado observado: 14 tabelas tratadas reproduzidas exatamente no recorte até 30/10/2026; comparacoes.csv.
- Procedimento executado: Replay dos brutos preservados, com deduplicação por coleta e corte temporal.
- Impacto científico: Não foi necessário substituir dados por consultas novas.
- Necessidade de ajuste: MANTER; nenhuma mudança aplicada.
- Recomendação: Preservar os brutos e as regras da descoberta.
- Risco de não ajustar: Reprodução futura depende da disponibilidade desses arquivos.

## AUD-001-03 — Indicador, unidades e mediana causal no tempo

- Categoria: Verificação concluída sem problemas. Gravidade: **informativa**. Situação: **aprovado**.
- Arquivo/função: `indicador.calcular_agio / consolidar; analise._anormal`.
- Evidência objetiva e resultado observado: Ágio = P/PTAX−1; agio_pct = 100×ágio; anormal em p.p.; mediana independente coincide, diferença máxima zero.
- Procedimento executado: Conferência algébrica e mediana por laço dos 30–60 valores anteriores.
- Impacto científico: Sem vazamento do próprio dia na referência da regressão.
- Necessidade de ajuste: MANTER; nenhuma mudança aplicada.
- Recomendação: Manter distinção proporção, percentual e ponto percentual.
- Risco de não ajustar: Confusão de escala se documentação omitir unidades.

## AUD-001-04 — Regressão principal e HAC

- Categoria: Verificação concluída sem problemas. Gravidade: **informativa**. Situação: **aprovado**.
- Arquivo/função: `analise.regressao; regressao_agio_anormal.csv`.
- Evidência objetiva e resultado observado: n=1490; R²=0,0953508683; curtose Pearson=15,3378; MQO independente difere ≤2,23e−16 e covariância HAC ≤2,38e−14.
- Procedimento executado: Reestimação e cálculo matricial independente de MQO e Bartlett HAC(5).
- Impacto científico: Coeficientes, erros-padrão e p-valores publicados reproduzem.
- Necessidade de ajuste: MANTER; nenhuma mudança aplicada.
- Recomendação: Documentar inferência normal assintótica, intercepto e ausência de correção de pequena amostra.
- Risco de não ajustar: Reprodução não resolve identificação causal.

## AUD-001-05 — Regressões complementares, eventos e tabelas

- Categoria: Verificação concluída sem problemas. Gravidade: **informativa**. Situação: **aprovado**.
- Arquivo/função: `cli.testar / buscas / oferta_usdt; relatorio.tabelas`.
- Evidência objetiva e resultado observado: 30 CSVs de resultados reproduzidos diretamente; quadro, seis estudos e comparações coincidem; Markdown igual salvo data de geração.
- Procedimento executado: Comparação de todas as células; dif de tabelas.
- Impacto científico: Valores de referência são computacionalmente sustentados.
- Necessidade de ajuste: MANTER; nenhuma mudança aplicada.
- Recomendação: Conservar resultados originais como descoberta.
- Risco de não ajustar: Nenhum erro numérico demonstrado nesses resultados.

## AUD-001-06 — Falha do comando robustez com os lotes existentes

- Categoria: Erro comprovado. Gravidade: **alta**. Situação: **confirmado**.
- Arquivo/função: `cli._horas_do_bruto:330; cli.robustez:390; janela.preco_janela_ptax:36`.
- Evidência objetiva e resultado observado: ValueError: cannot reindex on an axis with duplicate labels; pipeline.log:219–268. pd.concat conserva índices de cada lote.
- Procedimento executado: Execução literal na cópia; recálculo separado das nove especificações, com reset_index apenas no objeto em memória da auditoria.
- Impacto científico: Impede reprodução integral pelo comando atual. Os números recalculados coincidem exatamente; não se demonstrou que estavam errados.
- Necessidade de ajuste: CORRIGIR; nenhuma mudança aplicada.
- Recomendação: Em tarefa futura autorizada, normalizar índices na concatenação e testar múltiplos lotes reais.
- Risco de não ajustar: Rotina de robustez para de funcionar após novas coletas.

## AUD-001-07 — Base estatística oficial anterior à inclusão de Trends

- Categoria: Inconsistência documental. Gravidade: **baixa**. Situação: **confirmado**.
- Arquivo/função: `dados/resultados/base_teste.csv; cli.testar`.
- Evidência objetiva e resultado observado: Reprodução acrescenta busca_usdt, busca_dólar e seus anormais; 17 colunas comuns idênticas, quatro novas.
- Procedimento executado: Comparação estrutural e numérica com complementar.py.
- Impacto científico: Evidencia artefatos de rodadas distintas; não altera regressão principal.
- Necessidade de ajuste: DOCUMENTAR; nenhuma mudança aplicada.
- Recomendação: Identificar qual execução produziu cada base/relatório.
- Risco de não ajustar: Confusão entre rodadas ao reproduzir tudo de uma vez.

## AUD-001-08 — Reconciliação de 158 para 154 eventos

- Categoria: Verificação concluída sem problemas. Gravidade: **informativa**. Situação: **aprovado**.
- Arquivo/função: `analise._posicoes_eventos / _car; reconciliacao_eventos.csv`.
- Evidência objetiva e resultado observado: Copom 29/10/2020, Fed 06/11/2020 e relatório fiscal 21/11/2020 sem histórico/janela válida; Fed 29/10/2026 sem +3 completo.
- Procedimento executado: CAR e elegibilidade de cada linha; comparação com resultados por evento.
- Impacto científico: Exclusões são explicadas, sem indício de seleção por sinal.
- Necessidade de ajuste: DOCUMENTAR; nenhuma mudança aplicada.
- Recomendação: Publicar a tabela de fluxo de exclusões, datas cadastradas e efetivas.
- Risco de não ajustar: Contagem 158/154 parece contraditória sem fluxo explícito.

## AUD-001-09 — Definição de domésticos e externos

- Categoria: Verificação concluída sem problemas. Gravidade: **informativa**. Situação: **aprovado**.
- Arquivo/função: `analise.DOMESTICOS / EXTERNOS; decisões e pré-registro V1`.
- Evidência objetiva e resultado observado: Domésticos=fiscal+político (50); externos=externo (53) na lista completa; isolados 32 e 15. Copom/regulação não entram no contraste.
- Procedimento executado: Inspeção dos conjuntos e agrupamento da lista elegível.
- Impacto científico: Coerente com a regra documentada; não representa todo choque brasileiro.
- Necessidade de ajuste: MANTER; nenhuma mudança aplicada.
- Recomendação: Explicitar o universo no texto e não acrescentar categorias retrospectivamente.
- Risco de não ajustar: Generalização indevida para todo risco doméstico.

## AUD-001-10 — Sobreposição calculada no calendário errado

- Categoria: Erro comprovado. Gravidade: **alta**. Situação: **confirmado**.
- Arquivo/função: `scripts/montar_eventos.py:157; divergencias_sobreposicao.csv`.
- Evidência objetiva e resultado observado: Copom 28/10/2021 e Fed 04/11/2021 marcados nao; posições 262 e 266 na base (distância 4), janelas compartilham observação.
- Procedimento executado: Recontagem por posições efetivas da base PTAX e tipos diferentes.
- Impacto científico: Lista sem sobrepostos contém dois eventos sobrepostos entre si. Sensibilidade isolada: diferença ajustada 0,8548, p=0,0306; não muda baseline.
- Necessidade de ajuste: CORRIGIR; nenhuma mudança aplicada.
- Recomendação: Futuro ajuste da regra com calendário efetivo, acompanhado de registro e reapresentação lado a lado.
- Risco de não ajustar: Amostras classificadas como isoladas não cumprem a regra.

## AUD-001-11 — Dependência e comparabilidade nos testes de eventos

- Categoria: Risco metodológico. Gravidade: **alta**. Situação: **potencial**.
- Arquivo/função: `analise.estudo_evento`.
- Evidência objetiva e resultado observado: Sorteio placebo com reposição; 654 datas na lista completa e 1006 na isolada; CARs vizinhos dependentes; 47 dos 53 externos são Fed agendado.
- Procedimento executado: Inspeção e permutações por ano/deslocamentos circulares.
- Impacto científico: Rótulos não são atribuídos aleatoriamente; mudanças de regime e natureza dos eventos afetam permutabilidade.
- Necessidade de ajuste: TESTAR; nenhuma mudança aplicada.
- Recomendação: Reportar sensibilidades temporais, agendados versus não agendados e intervalos compatíveis com dependência.
- Risco de não ajustar: p-valores podem refletir composição temporal, não origem do choque.

## AUD-001-12 — Universo placebo muda ao excluir sobrepostos

- Categoria: Risco metodológico. Gravidade: **alta**. Situação: **potencial**.
- Arquivo/função: `analise.estudo_evento:141; analise.trajetoria_evento:284`.
- Evidência objetiva e resultado observado: Proibições usam somente eventos da lista passada. Isolados deixam eventos removidos nas datas placebo; gráficos excluem apenas o tipo do painel.
- Procedimento executado: Leitura de chamadas e contagem de candidatos.
- Impacto científico: Comparação isolada muda simultaneamente eventos e referência nula; faixa gráfica não equivale ao teste formal.
- Necessidade de ajuste: TESTAR; nenhuma mudança aplicada.
- Recomendação: Contrastar placebo excluindo toda a lista original, sem substituir os resultados publicados.
- Risco de não ajustar: Atribuir sensibilidade apenas à exclusão de sobreposição.

## AUD-001-13 — Precisão Monte Carlo e cálculo b/B

- Categoria: Risco metodológico. Gravidade: **média**. Situação: **potencial**.
- Arquivo/função: `analise.estudo_evento:156,175`.
- Evidência objetiva e resultado observado: 5000 sorteios, seed 42; p=b/5000, sem inclusão da observação; resolução 0,0002; EP MC aproximado 0,00253 para p=0,033.
- Procedimento executado: Inspeção do algoritmo e cálculo binomial da precisão.
- Impacto científico: Há risco de p=0 e subestimação discreta; não demonstra inversão de conclusão publicada.
- Necessidade de ajuste: TESTAR; nenhuma mudança aplicada.
- Recomendação: Avaliar (b+1)/(B+1), maior B e erro Monte Carlo em revisão autorizada.
- Risco de não ajustar: Falsa precisão perto de limiares e problemas de multiplicidade.

## AUD-001-14 — Datas e horários de eventos fiscais

- Categoria: Limitação conhecida e adequadamente documentada. Gravidade: **alta**. Situação: **potencial**.
- Arquivo/função: `scripts/montar_eventos.montar; docs/decisoes.md: lista fechada`.
- Evidência objetiva e resultado observado: PLDO/PLOA e RARDP gerados por prazos com aviso conferir data efetiva; _ultimo_util_ate só trata fins de semana. CSV não contém hora precisa.
- Procedimento executado: Confronto código, fontes textuais e 23 mapeamentos para outra data efetiva.
- Impacto científico: Janela pode não estar centrada no anúncio efetivo; já reconhecido pelo projeto.
- Necessidade de ajuste: TESTAR; nenhuma mudança aplicada.
- Recomendação: Auditoria documental primária de publicação e horário dos eventos ainda não verificados.
- Risco de não ajustar: Erro de mensuração temporal e classificação de surpresa.

## AUD-001-15 — Janela PTAX é aproximação

- Categoria: Limitação conhecida e adequadamente documentada. Gravidade: **média**. Situação: **confirmado**.
- Arquivo/função: `janela.preco_janela_ptax; docs/decisoes.md`.
- Evidência objetiva e resultado observado: Usa 10:00≤hora<13:00 (13,14,15 UTC); exclui a consulta após 13h; HLC3 ponderado não é VWAP de negócios. Há robustez 10–14.
- Procedimento executado: Inspeção dos candles e método do BCB; reconstrução das duas janelas.
- Impacto científico: Melhora sincronização, mas não replica os quatro instantes de consulta.
- Necessidade de ajuste: DOCUMENTAR; nenhuma mudança aplicada.
- Recomendação: Descrever limites exatos e HLC3; manter teste 10–14 como sensibilidade.
- Risco de não ajustar: Alegação de alinhamento exato exagera qualidade da medida.

## AUD-001-16 — Candles incompletos e cobertura de corretoras

- Categoria: Risco metodológico. Gravidade: **média**. Situação: **potencial**.
- Arquivo/função: `janela.preco_janela_ptax; verificacoes_finais.json`.
- Evidência objetiva e resultado observado: 13 linhas corretora-dia da amostra têm menos de três candles (2 Binance, 11 MB); sem janelas com volume total zero; horas_janela conta candles, não horas com negócios.
- Procedimento executado: Contagem na interseção com as 1520 datas do indicador e validação OHLC.
- Impacto científico: Precisão da medida varia; alta concentração Binance já documentada.
- Necessidade de ajuste: TESTAR; nenhuma mudança aplicada.
- Recomendação: Quantificar cobertura por fonte e sensibilidade a janelas completas, sem excluir silenciosamente.
- Risco de não ajustar: Tratar preços com suporte distinto como equivalentes.

## AUD-001-17 — Fusos, dias disponíveis e controles defasados

- Categoria: Verificação concluída sem problemas. Gravidade: **informativa**. Situação: **aprovado**.
- Arquivo/função: `fontes.binance / mercadobitcoin; janela; analise.montar_base`.
- Evidência objetiva e resultado observado: Candles UTC convertidos via America/Sao_Paulo; dias PTAX determinam a base; 11 VIX carregados de data anterior, atraso máximo três dias.
- Procedimento executado: Replay, interseção de datas e auditoria de merge_asof backward.
- Impacto científico: Não há backfill futuro nessas junções; diferenças são por dias da base, não sessões americanas consecutivas.
- Necessidade de ajuste: DOCUMENTAR; nenhuma mudança aplicada.
- Recomendação: Explicitar calendário observado e tratamento de feriados estrangeiros.
- Risco de não ajustar: Confundir variação de um intervalo irregular com retorno diário homogêneo.

## AUD-001-18 — VIX contemporâneo e previsão em tempo real

- Categoria: Limitação conhecida e adequadamente documentada. Gravidade: **alta**. Situação: **confirmado**.
- Arquivo/função: `analise.montar_base:74; docs/resultados.md §9`.
- Evidência objetiva e resultado observado: Fechamento contemporâneo do VIX ocorre depois da janela do ágio; d_vix_ant é defasado na base brasileira.
- Procedimento executado: Inspeção de disponibilidade informacional, sem nova coleta.
- Impacto científico: Regressão contemporânea é associativa ex post; não é previsão disponível às 13h.
- Necessidade de ajuste: DOCUMENTAR; nenhuma mudança aplicada.
- Recomendação: Restringir linguagem a associação e testar especificação estritamente disponível em t−1 se houver objetivo preditivo.
- Risco de não ajustar: Vazamento informacional se resultados forem usados como previsão intradiária.

## AUD-001-19 — Repasse: indicador não identifica vendas para realizar ganhos

- Categoria: Risco metodológico. Gravidade: **alta**. Situação: **potencial**.
- Arquivo/função: `analise.regressao_repasse; docs/resultados.md §5.1; pré-registro V6`.
- Evidência objetiva e resultado observado: Identidade de retornos verificada ≤3,84e−14; regressão de retorno USDT dá 0,8562 versus −0,1290 sobre ágio anormal.
- Procedimento executado: Decomposição algébrica e três regressões suplementares.
- Impacto científico: Ágio anormal é nível relativo à mediana, não retorno. Soma −0,0798 não identifica motivo de negociação nem resposta causal acumulada.
- Necessidade de ajuste: DOCUMENTAR; nenhuma mudança aplicada.
- Recomendação: Separar identidade, associação e mecanismo; preservar V4a/V4b/V6 como hipóteses registradas.
- Risco de não ajustar: V6 pode confirmar padrão de sinal sem confirmar realização de ganhos.

## AUD-001-20 — Holm e hipótese conjunta V1 na descoberta

- Categoria: Verificação concluída sem problemas. Gravidade: **informativa**. Situação: **aprovado**.
- Arquivo/função: `analise.holm / quadro_hipoteses; hipoteses.csv`.
- Evidência objetiva e resultado observado: Sete hipóteses; comparação com statsmodels multipletests idêntica. V1 usa máximo dos dois p-valores e exige ambos sinais.
- Procedimento executado: Verificação independente da ordenação, monotonicidade, família e decisões.
- Impacto científico: Holm pode ser usado sob dependência se p-valores marginais forem válidos; não corrige seleção anterior de análises.
- Necessidade de ajuste: MANTER; nenhuma mudança aplicada.
- Recomendação: Manter quadro bruto+Holm e origem exploratória explícita.
- Risco de não ajustar: Confundir controle desta família com correção dos cerca de 40 testes exploratórios.

## AUD-001-21 — Regra de menos de dez eventos omite V1

- Categoria: Erro comprovado. Gravidade: **alta**. Situação: **confirmado**.
- Arquivo/função: `analise.quadro_hipoteses:365`.
- Evidência objetiva e resultado observado: n_eventos só tem V2 e V5. Exemplo sintético com dois eventos gera V1=nao, em vez de inconclusivo; hipoteses_teste_2_eventos.csv.
- Procedimento executado: Chamada sintética separada, sem mexer em testes ou dados oficiais.
- Impacto científico: Descoberta tem eventos suficientes; problema afeta implementação do plano futuro de validação.
- Necessidade de ajuste: CORRIGIR; nenhuma mudança aplicada.
- Recomendação: Definir com pesquisador contagem mínima por braço e aplicar guarda V1 em mudança futura datada.
- Risco de não ajustar: Resultado negativo indevido com amostra insuficiente.

## AUD-001-22 — Família de Holm encolhe se V5 não estiver disponível

- Categoria: Erro comprovado. Gravidade: **média**. Situação: **confirmado**.
- Arquivo/função: `analise.quadro_hipoteses:351`.
- Evidência objetiva e resultado observado: Entrada grupos_ajustado_isolados=None produz seis linhas, embora adendo defina sete hipóteses.
- Procedimento executado: Teste de fronteira com ausência de grupo; verificacoes_finais.json.
- Impacto científico: Não afeta quadro atual; muda proteção múltipla em validação com eventos ausentes.
- Necessidade de ajuste: CORRIGIR; nenhuma mudança aplicada.
- Recomendação: Preservar família registrada, registrando não testável explicitamente, em implementação autorizada.
- Risco de não ajustar: Decisões futuras variam com disponibilidade de uma hipótese.

## AUD-001-23 — V4b e V6 e avaliações sequenciais

- Categoria: Risco metodológico. Gravidade: **alta**. Situação: **potencial**.
- Arquivo/função: `docs/pre-registro.md; analise.quadro_hipoteses`.
- Evidência objetiva e resultado observado: V4b e V6 usam o mesmo p bilateral, com sinais opostos; Holm inclui ambos. Intermediária 1% permite antecipar confirmação e final usa 5%, sem gasto alfa.
- Procedimento executado: Confronto do adendo com código e lógica de testes repetidos.
- Impacto científico: Duplicidade não invalida Holm, mas não são evidências independentes. 1%+5% não garante erro familiar global de 5% entre análises.
- Necessidade de ajuste: DOCUMENTAR; nenhuma mudança aplicada.
- Recomendação: Adendo futuro datado: família, bilateralidade, hipótese não estimável e regra sequencial explícita antes de analisar validação.
- Risco de não ajustar: Confirmação antecipada pode elevar erro além do declarado; reinterpretação retrospectiva.

## AUD-001-24 — Origem e temporalidade do pré-registro

- Categoria: Verificação inconclusiva por falta de evidência. Gravidade: **média**. Situação: **inconclusivo**.
- Arquivo/função: `docs/pre-registro.md; histórico Git; brutos com carimbo de coleta`.
- Evidência objetiva e resultado observado: Introdução 2409cfa em 01/11/2026 09:04 −03; adendo c176bfd às 17:13. Diário mostra descobertas e mudança de lista após resultados.
- Procedimento executado: Histórico de arquivo e comparação com datas declaradas, sem inferir ordem não registrada.
- Impacto científico: Git local não prova registro independente imutável nem prioridade exata da hipótese original; dados são vintages coletados depois do corte.
- Necessidade de ajuste: DOCUMENTAR; nenhuma mudança aplicada.
- Recomendação: Preservar histórico e obter registro público/datado; distinguir descoberta e validação.
- Risco de não ajustar: Apresentar toda descoberta como confirmatória pré-registrada.

## AUD-001-25 — Robustez de significância não é uniformidade

- Categoria: Risco metodológico. Gravidade: **alta**. Situação: **potencial**.
- Arquivo/função: `dados/resultados/robustez.csv; sensibilidade_regressoes.csv`.
- Evidência objetiva e resultado observado: VIX anterior 7/9 reproduzido, mas retirar cinco maiores Cook leva p=0,09984; subamostras posteriores p=0,347 e 0,500. Dólar pós-04/05 p=0,111.
- Procedimento executado: HAC 5/10/20, influência 1/5/15 e três períodos fixos.
- Impacto científico: Não sustenta afirmação categórica não depende de poucos dias; sinais/tamanhos variam. Não prova quebra estrutural.
- Necessidade de ajuste: TESTAR; nenhuma mudança aplicada.
- Recomendação: Reportar sensibilidade completa e, futuramente, testes conjuntos de estabilidade/poder.
- Risco de não ajustar: Escolher só especificações significativas e confundir falta de poder com prova de estabilidade.

## AUD-001-26 — Mediana desenhada difere do normal da regressão

- Categoria: Erro comprovado. Gravidade: **média**. Situação: **confirmado**.
- Arquivo/função: `relatorio.fig_serie:72 versus analise._anormal:32`.
- Evidência objetiva e resultado observado: Gráfico usa rolling sem shift; legenda chama de normal usado no ágio anormal. Diferença máxima 0,0800594 p.p.
- Procedimento executado: Comparação das duas séries com 1520 dias.
- Impacto científico: Afeta legenda/figura, não coeficientes ou base de análise.
- Necessidade de ajuste: CORRIGIR; nenhuma mudança aplicada.
- Recomendação: Em tarefa futura, alinhar a curva ou corrigir a legenda de modo explícito.
- Risco de não ajustar: Leitor atribui ao gráfico referência diferente da estatística.

## AUD-001-27 — Contagem nominal de eventos nas trajetórias

- Categoria: Erro comprovado. Gravidade: **média**. Situação: **confirmado**.
- Arquivo/função: `analise.trajetoria_evento:280,297; relatorio.fig_trajetorias:182`.
- Evidência objetiva e resultado observado: Rótulos fiscal=47, externo=54, monetário=48; valores efetivos não nulos por dia: 46–47,53,47.
- Procedimento executado: Matrizes de −5 a +10, contagem de NaN por posição.
- Impacto científico: Faixa usa n nominal enquanto nanmean ignora valores ausentes; precisão e contagem não coincidem.
- Necessidade de ajuste: CORRIGIR; nenhuma mudança aplicada.
- Recomendação: Exibir n efetivo por dia ou definir amostra completa comum em revisão autorizada.
- Risco de não ajustar: Faixas e legendas podem superestimar informação.

## AUD-001-28 — Significado das faixas de 95%

- Categoria: Risco metodológico. Gravidade: **média**. Situação: **potencial**.
- Arquivo/função: `analise.trajetoria_evento; figuras 06,07,09`.
- Evidência objetiva e resultado observado: Percentis ponto a ponto de médias placebo; não são IC da média observada nem banda simultânea de trajetória. Figura 08 usa 1,96×EP; Huber não tem HAC.
- Procedimento executado: Inspeção da geração, escalas e legendas nas dez figuras.
- Impacto científico: Cruzar a faixa em um dia não equivale a rejeitar teste CAR nem teste simultâneo.
- Necessidade de ajuste: DOCUMENTAR; nenhuma mudança aplicada.
- Recomendação: Explicitar referência, n, exclusões por tipo, ausência de simultaneidade e IC assintótico da robustez.
- Risco de não ajustar: Interpretar inspeção visual como novo teste confirmatório.

## AUD-001-29 — Google Trends e textos antigos

- Categoria: Inconsistência documental. Gravidade: **baixa**. Situação: **confirmado**.
- Arquivo/função: `docs/resultados.md:189,197; relatorio.tabelas; dados/resultados/exploratorio_*`.
- Evidência objetiva e resultado observado: Trends importado e reproduzido; duas figuras presentes; narrativa ainda diz não importado e enumera oito figuras. Quadro textual cita V3–V5, omite V6.
- Procedimento executado: Confronto artefatos, histórico e narrativa.
- Impacto científico: Dificulta saber o que já foi analisado.
- Necessidade de ajuste: DOCUMENTAR; nenhuma mudança aplicada.
- Recomendação: Atualizar por documento novo/errata autorizado, mantendo diário histórico e origem exploratória.
- Risco de não ajustar: Leitor recebe estado desatualizado da pesquisa.

## AUD-001-30 — Afirmações causais e irrelevância fiscal

- Categoria: Inconsistência documental. Gravidade: **alta**. Situação: **confirmado**.
- Arquivo/função: `docs/resultados.md resumo, §§5,5.1,6,8; docs/decisoes.md`.
- Evidência objetiva e resultado observado: Texto usa não funciona como termômetro, é movido e vendas para realização. Juro de fechamento é negativo e significativo (p≈0,001); não positivo em nenhuma das nove especificações originais.
- Procedimento executado: Confronto de frases com resultados e desenho observacional.
- Impacto científico: Não significância não prova inexistência; sinal de juro não isola choque fiscal; modelo não identifica comportamento.
- Necessidade de ajuste: DOCUMENTAR; nenhuma mudança aplicada.
- Recomendação: Usar não confirmada nesta amostra e associação; preservar hipótese original e resultados contrários.
- Risco de não ajustar: Conclusão do TCC extrapola evidência observacional.

## AUD-001-31 — Unidade do volume no episódio

- Categoria: Erro comprovado. Gravidade: **média**. Situação: **confirmado**.
- Arquivo/função: `docs/resultados.md §3.1; episodio.resumo; janela.volume_janela`.
- Evidência objetiva e resultado observado: 17,1457→26,0686 milhões são volume_base em USDT, descritos como R$ 17,1→26,1 mi. Proxy de valor HLC3×volume: R$87,23→134,36 mi.
- Procedimento executado: Rastreio da coluna desde candles até tabela narrativa.
- Impacto científico: Não altera aumento de volume em unidades base, mas erra escala monetária.
- Necessidade de ajuste: CORRIGIR; nenhuma mudança aplicada.
- Recomendação: Corrigir unidade em errata futura; não confundir proxy monetária com volume_brl exato.
- Risco de não ajustar: Erro factual na descrição de liquidez.

## AUD-001-32 — Episódio: janela e mecanismo

- Categoria: Risco metodológico. Gravidade: **alta**. Situação: **potencial**.
- Arquivo/função: `episodio.montar; docs/resultados.md §3.1`.
- Evidência objetiva e resultado observado: Tabela refere-se a 01/06–14/08 (54 dias), não só 24/06–meados de julho. Recorte suplementar 24/06–17/07: ágio Binance 1,052%, MB 0,733%, correlação 0,76.
- Procedimento executado: Reprodução da janela original e diagnóstico alternativo explicitamente identificado.
- Impacto científico: Ágio persistente nas duas fontes é observado; escassez de vendedores e atrito específico não são identificados por ticket/taker.
- Necessidade de ajuste: DOCUMENTAR; nenhuma mudança aplicada.
- Recomendação: Separar período de diagnóstico, núcleo do episódio e interpretação exploratória.
- Risco de não ajustar: Atribuição de comportamento e médias a um período diferente.

## AUD-001-33 — Oferta global: não significância não descarta escassez

- Categoria: Inconsistência documental. Gravidade: **alta**. Situação: **confirmado**.
- Arquivo/função: `docs/resultados.md:76,196; analise.regressao_oferta_usdt`.
- Evidência objetiva e resultado observado: Coeficiente +0,031, p≈0,051 reproduzido; variável é 100 log(S_t/S_t−5), deslocada um dia de calendário. Texto afirma escassez global descartada.
- Procedimento executado: Replay DefiLlama e regressão exploratória, inspeção temporal.
- Impacto científico: Sinal não sustenta hipótese negativa específica, mas não prova ausência de escassez ou oferta local suficiente.
- Necessidade de ajuste: DOCUMENTAR; nenhuma mudança aplicada.
- Recomendação: Trocar inferência conclusiva por hipótese não sustentada nesta especificação; manter causa não identificada.
- Risco de não ajustar: Refutação causal indevida com proxy global e erro de medida.

## AUD-001-34 — Procedência e disponibilidade histórica dos dados

- Categoria: Verificação inconclusiva por falta de evidência. Gravidade: **alta**. Situação: **inconclusivo**.
- Arquivo/função: `dados/bruto; fontes.defillama / tesouro / google_trends`.
- Evidência objetiva e resultado observado: Arquivos preservados e valores reproduzíveis, mas não há recibos assinados/vintages históricos de publicação; datas não provam hora de disponibilização real da oferta ou taxa da manhã.
- Procedimento executado: Inspeção de arquivos, metadados e consultas externas somente metodológicas/de procedência.
- Impacto científico: Não certifica autenticidade independente de cada observação, dado em tempo real nem todas as notícias de 2026.
- Necessidade de ajuste: TESTAR; nenhuma mudança aplicada.
- Recomendação: Completar cadeia de custódia e fontes primárias; não substituir silenciosamente histórico.
- Risco de não ajustar: Confundir consistência interna com validação externa integral.

## AUD-001-35 — Testes, dependências e preservação computacional

- Categoria: Oportunidade de melhoria. Gravidade: **baixa**. Situação: **confirmado**.
- Arquivo/função: `pyproject.toml; tests/*; git_antes.txt; versoes.json`.
- Evidência objetiva e resultado observado: 41 testes passaram; um warning de precisão em caso sintético. Dependências têm limites mínimos sem lock; dados principais não rastreados apesar do diário mencionar CSV versionado.
- Procedimento executado: pytest isolado, inventário de versões e Git.
- Impacto científico: Ambiente atual reproduz; clone do commit sozinho não contém toda baseline.
- Necessidade de ajuste: DOCUMENTAR; nenhuma mudança aplicada.
- Recomendação: Arquivar bundle de dados, hashes, versões e comandos; testes de fronteira em tarefa futura.
- Risco de não ajustar: Clone futuro não reproduz e mudanças de biblioteca afetam execução.

## AUD-001-36 — Figuras e tabelas regeneradas

- Categoria: Verificação concluída sem problemas. Gravidade: **informativa**. Situação: **aprovado**.
- Arquivo/função: `relatorio.gerar; cli.buscas; episodio.rodar`.
- Evidência objetiva e resultado observado: Dez figuras solicitadas idênticas byte a byte; episódio também idêntico em processo separado; tabelas idênticas exceto data.
- Procedimento executado: Regeneração, SHA-256/pixels e inspeção visual do contato; episódio em processo separado elimina rcParams herdados.
- Impacto científico: Concordância com gerador e dados, ressalvados erros semânticos acima.
- Necessidade de ajuste: MANTER; nenhuma mudança aplicada.
- Recomendação: Manter arquivos oficiais; anotar ordem/processo de geração e ressalvas de legenda.
- Risco de não ajustar: Igualdade de pixels não valida interpretação científica.
