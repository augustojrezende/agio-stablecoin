# AUD-001 — Plano de ajustes para decisão do pesquisador

Nenhuma correção implementada. Este plano separa erro demonstrado de escolhas metodológicas defensáveis. Todos os itens que alterem baseline, pré-registro, classificação ou texto original dependem de autorização expressa do pesquisador em tarefa futura. Adendos devem ser datados, com versão original preservada; nenhuma hipótese deve ser reformulada retrospectivamente para coincidir com resultados.

Prioridade P1: antes de apresentação como resultado final ou inferência confirmatória; P2: melhorar auditabilidade e robustez; P3: manutenção. CORRIGIR aplica-se apenas a falhas demonstradas. DOCUMENTAR não deve apagar o histórico do diário.

## AUD-001-06 — CORRIGIR — P1

- Item: Falha do comando robustez com os lotes existentes.
- Justificativa: ValueError: cannot reindex on an axis with duplicate labels; pipeline.log:219–268. pd.concat conserva índices de cada lote.
- Arquivos potencialmente envolvidos: `cli._horas_do_bruto:330; cli.robustez:390; janela.preco_janela_ptax:36`.
- Ação proposta: Em tarefa futura autorizada, normalizar índices na concatenação e testar múltiplos lotes reais.
- Efeito esperado: Impede reprodução integral pelo comando atual. Os números recalculados coincidem exatamente; não se demonstrou que estavam errados.
- Risco científico se mantido sem tratamento: Rotina de robustez para de funcionar após novas coletas.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: sim, antes de qualquer alteração ou adoção de nova especificação; não solicitada nesta auditoria.
## AUD-001-10 — CORRIGIR — P1

- Item: Sobreposição calculada no calendário errado.
- Justificativa: Copom 28/10/2021 e Fed 04/11/2021 marcados nao; posições 262 e 266 na base (distância 4), janelas compartilham observação.
- Arquivos potencialmente envolvidos: `scripts/montar_eventos.py:157; divergencias_sobreposicao.csv`.
- Ação proposta: Futuro ajuste da regra com calendário efetivo, acompanhado de registro e reapresentação lado a lado.
- Efeito esperado: Lista sem sobrepostos contém dois eventos sobrepostos entre si. Sensibilidade isolada: diferença ajustada 0,8548, p=0,0306; não muda baseline.
- Risco científico se mantido sem tratamento: Amostras classificadas como isoladas não cumprem a regra.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: sim, antes de qualquer alteração ou adoção de nova especificação; não solicitada nesta auditoria.
## AUD-001-11 — TESTAR — P1

- Item: Dependência e comparabilidade nos testes de eventos.
- Justificativa: Sorteio placebo com reposição; 654 datas na lista completa e 1006 na isolada; CARs vizinhos dependentes; 47 dos 53 externos são Fed agendado.
- Arquivos potencialmente envolvidos: `analise.estudo_evento`.
- Ação proposta: Reportar sensibilidades temporais, agendados versus não agendados e intervalos compatíveis com dependência.
- Efeito esperado: Rótulos não são atribuídos aleatoriamente; mudanças de regime e natureza dos eventos afetam permutabilidade.
- Risco científico se mantido sem tratamento: p-valores podem refletir composição temporal, não origem do choque.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: sim, antes de qualquer alteração ou adoção de nova especificação; não solicitada nesta auditoria.
## AUD-001-12 — TESTAR — P1

- Item: Universo placebo muda ao excluir sobrepostos.
- Justificativa: Proibições usam somente eventos da lista passada. Isolados deixam eventos removidos nas datas placebo; gráficos excluem apenas o tipo do painel.
- Arquivos potencialmente envolvidos: `analise.estudo_evento:141; analise.trajetoria_evento:284`.
- Ação proposta: Contrastar placebo excluindo toda a lista original, sem substituir os resultados publicados.
- Efeito esperado: Comparação isolada muda simultaneamente eventos e referência nula; faixa gráfica não equivale ao teste formal.
- Risco científico se mantido sem tratamento: Atribuir sensibilidade apenas à exclusão de sobreposição.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: sim, antes de qualquer alteração ou adoção de nova especificação; não solicitada nesta auditoria.
## AUD-001-14 — TESTAR — P1

- Item: Datas e horários de eventos fiscais.
- Justificativa: PLDO/PLOA e RARDP gerados por prazos com aviso conferir data efetiva; _ultimo_util_ate só trata fins de semana. CSV não contém hora precisa.
- Arquivos potencialmente envolvidos: `scripts/montar_eventos.montar; docs/decisoes.md: lista fechada`.
- Ação proposta: Auditoria documental primária de publicação e horário dos eventos ainda não verificados.
- Efeito esperado: Janela pode não estar centrada no anúncio efetivo; já reconhecido pelo projeto.
- Risco científico se mantido sem tratamento: Erro de mensuração temporal e classificação de surpresa.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: sim, antes de qualquer alteração ou adoção de nova especificação; não solicitada nesta auditoria.
## AUD-001-18 — DOCUMENTAR — P1

- Item: VIX contemporâneo e previsão em tempo real.
- Justificativa: Fechamento contemporâneo do VIX ocorre depois da janela do ágio; d_vix_ant é defasado na base brasileira.
- Arquivos potencialmente envolvidos: `analise.montar_base:74; docs/resultados.md §9`.
- Ação proposta: Restringir linguagem a associação e testar especificação estritamente disponível em t−1 se houver objetivo preditivo.
- Efeito esperado: Regressão contemporânea é associativa ex post; não é previsão disponível às 13h.
- Risco científico se mantido sem tratamento: Vazamento informacional se resultados forem usados como previsão intradiária.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: sim, antes de qualquer alteração ou adoção de nova especificação; não solicitada nesta auditoria.
## AUD-001-19 — DOCUMENTAR — P1

- Item: Repasse: indicador não identifica vendas para realizar ganhos.
- Justificativa: Identidade de retornos verificada ≤3,84e−14; regressão de retorno USDT dá 0,8562 versus −0,1290 sobre ágio anormal.
- Arquivos potencialmente envolvidos: `analise.regressao_repasse; docs/resultados.md §5.1; pré-registro V6`.
- Ação proposta: Separar identidade, associação e mecanismo; preservar V4a/V4b/V6 como hipóteses registradas.
- Efeito esperado: Ágio anormal é nível relativo à mediana, não retorno. Soma −0,0798 não identifica motivo de negociação nem resposta causal acumulada.
- Risco científico se mantido sem tratamento: V6 pode confirmar padrão de sinal sem confirmar realização de ganhos.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: sim, antes de qualquer alteração ou adoção de nova especificação; não solicitada nesta auditoria.
## AUD-001-21 — CORRIGIR — P1

- Item: Regra de menos de dez eventos omite V1.
- Justificativa: n_eventos só tem V2 e V5. Exemplo sintético com dois eventos gera V1=nao, em vez de inconclusivo; hipoteses_teste_2_eventos.csv.
- Arquivos potencialmente envolvidos: `analise.quadro_hipoteses:365`.
- Ação proposta: Definir com pesquisador contagem mínima por braço e aplicar guarda V1 em mudança futura datada.
- Efeito esperado: Descoberta tem eventos suficientes; problema afeta implementação do plano futuro de validação.
- Risco científico se mantido sem tratamento: Resultado negativo indevido com amostra insuficiente.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: sim, antes de qualquer alteração ou adoção de nova especificação; não solicitada nesta auditoria.
## AUD-001-23 — DOCUMENTAR — P1

- Item: V4b e V6 e avaliações sequenciais.
- Justificativa: V4b e V6 usam o mesmo p bilateral, com sinais opostos; Holm inclui ambos. Intermediária 1% permite antecipar confirmação e final usa 5%, sem gasto alfa.
- Arquivos potencialmente envolvidos: `docs/pre-registro.md; analise.quadro_hipoteses`.
- Ação proposta: Adendo futuro datado: família, bilateralidade, hipótese não estimável e regra sequencial explícita antes de analisar validação.
- Efeito esperado: Duplicidade não invalida Holm, mas não são evidências independentes. 1%+5% não garante erro familiar global de 5% entre análises.
- Risco científico se mantido sem tratamento: Confirmação antecipada pode elevar erro além do declarado; reinterpretação retrospectiva.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: sim, antes de qualquer alteração ou adoção de nova especificação; não solicitada nesta auditoria.
## AUD-001-25 — TESTAR — P1

- Item: Robustez de significância não é uniformidade.
- Justificativa: VIX anterior 7/9 reproduzido, mas retirar cinco maiores Cook leva p=0,09984; subamostras posteriores p=0,347 e 0,500. Dólar pós-04/05 p=0,111.
- Arquivos potencialmente envolvidos: `dados/resultados/robustez.csv; sensibilidade_regressoes.csv`.
- Ação proposta: Reportar sensibilidade completa e, futuramente, testes conjuntos de estabilidade/poder.
- Efeito esperado: Não sustenta afirmação categórica não depende de poucos dias; sinais/tamanhos variam. Não prova quebra estrutural.
- Risco científico se mantido sem tratamento: Escolher só especificações significativas e confundir falta de poder com prova de estabilidade.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: sim, antes de qualquer alteração ou adoção de nova especificação; não solicitada nesta auditoria.
## AUD-001-30 — DOCUMENTAR — P1

- Item: Afirmações causais e irrelevância fiscal.
- Justificativa: Texto usa não funciona como termômetro, é movido e vendas para realização. Juro de fechamento é negativo e significativo (p≈0,001); não positivo em nenhuma das nove especificações originais.
- Arquivos potencialmente envolvidos: `docs/resultados.md resumo, §§5,5.1,6,8; docs/decisoes.md`.
- Ação proposta: Usar não confirmada nesta amostra e associação; preservar hipótese original e resultados contrários.
- Efeito esperado: Não significância não prova inexistência; sinal de juro não isola choque fiscal; modelo não identifica comportamento.
- Risco científico se mantido sem tratamento: Conclusão do TCC extrapola evidência observacional.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: sim, antes de qualquer alteração ou adoção de nova especificação; não solicitada nesta auditoria.
## AUD-001-32 — DOCUMENTAR — P1

- Item: Episódio: janela e mecanismo.
- Justificativa: Tabela refere-se a 01/06–14/08 (54 dias), não só 24/06–meados de julho. Recorte suplementar 24/06–17/07: ágio Binance 1,052%, MB 0,733%, correlação 0,76.
- Arquivos potencialmente envolvidos: `episodio.montar; docs/resultados.md §3.1`.
- Ação proposta: Separar período de diagnóstico, núcleo do episódio e interpretação exploratória.
- Efeito esperado: Ágio persistente nas duas fontes é observado; escassez de vendedores e atrito específico não são identificados por ticket/taker.
- Risco científico se mantido sem tratamento: Atribuição de comportamento e médias a um período diferente.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: sim, antes de qualquer alteração ou adoção de nova especificação; não solicitada nesta auditoria.
## AUD-001-33 — DOCUMENTAR — P1

- Item: Oferta global: não significância não descarta escassez.
- Justificativa: Coeficiente +0,031, p≈0,051 reproduzido; variável é 100 log(S_t/S_t−5), deslocada um dia de calendário. Texto afirma escassez global descartada.
- Arquivos potencialmente envolvidos: `docs/resultados.md:76,196; analise.regressao_oferta_usdt`.
- Ação proposta: Trocar inferência conclusiva por hipótese não sustentada nesta especificação; manter causa não identificada.
- Efeito esperado: Sinal não sustenta hipótese negativa específica, mas não prova ausência de escassez ou oferta local suficiente.
- Risco científico se mantido sem tratamento: Refutação causal indevida com proxy global e erro de medida.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: sim, antes de qualquer alteração ou adoção de nova especificação; não solicitada nesta auditoria.
## AUD-001-34 — TESTAR — P1

- Item: Procedência e disponibilidade histórica dos dados.
- Justificativa: Arquivos preservados e valores reproduzíveis, mas não há recibos assinados/vintages históricos de publicação; datas não provam hora de disponibilização real da oferta ou taxa da manhã.
- Arquivos potencialmente envolvidos: `dados/bruto; fontes.defillama / tesouro / google_trends`.
- Ação proposta: Completar cadeia de custódia e fontes primárias; não substituir silenciosamente histórico.
- Efeito esperado: Não certifica autenticidade independente de cada observação, dado em tempo real nem todas as notícias de 2026.
- Risco científico se mantido sem tratamento: Confundir consistência interna com validação externa integral.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: sim, antes de qualquer alteração ou adoção de nova especificação; não solicitada nesta auditoria.
## AUD-001-13 — TESTAR — P2

- Item: Precisão Monte Carlo e cálculo b/B.
- Justificativa: 5000 sorteios, seed 42; p=b/5000, sem inclusão da observação; resolução 0,0002; EP MC aproximado 0,00253 para p=0,033.
- Arquivos potencialmente envolvidos: `analise.estudo_evento:156,175`.
- Ação proposta: Avaliar (b+1)/(B+1), maior B e erro Monte Carlo em revisão autorizada.
- Efeito esperado: Há risco de p=0 e subestimação discreta; não demonstra inversão de conclusão publicada.
- Risco científico se mantido sem tratamento: Falsa precisão perto de limiares e problemas de multiplicidade.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: sim, antes de qualquer alteração ou adoção de nova especificação; não solicitada nesta auditoria.
## AUD-001-15 — DOCUMENTAR — P2

- Item: Janela PTAX é aproximação.
- Justificativa: Usa 10:00≤hora<13:00 (13,14,15 UTC); exclui a consulta após 13h; HLC3 ponderado não é VWAP de negócios. Há robustez 10–14.
- Arquivos potencialmente envolvidos: `janela.preco_janela_ptax; docs/decisoes.md`.
- Ação proposta: Descrever limites exatos e HLC3; manter teste 10–14 como sensibilidade.
- Efeito esperado: Melhora sincronização, mas não replica os quatro instantes de consulta.
- Risco científico se mantido sem tratamento: Alegação de alinhamento exato exagera qualidade da medida.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: sim, antes de qualquer alteração ou adoção de nova especificação; não solicitada nesta auditoria.
## AUD-001-16 — TESTAR — P2

- Item: Candles incompletos e cobertura de corretoras.
- Justificativa: 13 linhas corretora-dia da amostra têm menos de três candles (2 Binance, 11 MB); sem janelas com volume total zero; horas_janela conta candles, não horas com negócios.
- Arquivos potencialmente envolvidos: `janela.preco_janela_ptax; verificacoes_finais.json`.
- Ação proposta: Quantificar cobertura por fonte e sensibilidade a janelas completas, sem excluir silenciosamente.
- Efeito esperado: Precisão da medida varia; alta concentração Binance já documentada.
- Risco científico se mantido sem tratamento: Tratar preços com suporte distinto como equivalentes.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: sim, antes de qualquer alteração ou adoção de nova especificação; não solicitada nesta auditoria.
## AUD-001-22 — CORRIGIR — P2

- Item: Família de Holm encolhe se V5 não estiver disponível.
- Justificativa: Entrada grupos_ajustado_isolados=None produz seis linhas, embora adendo defina sete hipóteses.
- Arquivos potencialmente envolvidos: `analise.quadro_hipoteses:351`.
- Ação proposta: Preservar família registrada, registrando não testável explicitamente, em implementação autorizada.
- Efeito esperado: Não afeta quadro atual; muda proteção múltipla em validação com eventos ausentes.
- Risco científico se mantido sem tratamento: Decisões futuras variam com disponibilidade de uma hipótese.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: sim, antes de qualquer alteração ou adoção de nova especificação; não solicitada nesta auditoria.
## AUD-001-24 — DOCUMENTAR — P2

- Item: Origem e temporalidade do pré-registro.
- Justificativa: Introdução 2409cfa em 01/11/2026 09:04 −03; adendo c176bfd às 17:13. Diário mostra descobertas e mudança de lista após resultados.
- Arquivos potencialmente envolvidos: `docs/pre-registro.md; histórico Git; brutos com carimbo de coleta`.
- Ação proposta: Preservar histórico e obter registro público/datado; distinguir descoberta e validação.
- Efeito esperado: Git local não prova registro independente imutável nem prioridade exata da hipótese original; dados são vintages coletados depois do corte.
- Risco científico se mantido sem tratamento: Apresentar toda descoberta como confirmatória pré-registrada.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: sim, antes de qualquer alteração ou adoção de nova especificação; não solicitada nesta auditoria.
## AUD-001-26 — CORRIGIR — P2

- Item: Mediana desenhada difere do normal da regressão.
- Justificativa: Gráfico usa rolling sem shift; legenda chama de normal usado no ágio anormal. Diferença máxima 0,0800594 p.p.
- Arquivos potencialmente envolvidos: `relatorio.fig_serie:72 versus analise._anormal:32`.
- Ação proposta: Em tarefa futura, alinhar a curva ou corrigir a legenda de modo explícito.
- Efeito esperado: Afeta legenda/figura, não coeficientes ou base de análise.
- Risco científico se mantido sem tratamento: Leitor atribui ao gráfico referência diferente da estatística.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: sim, antes de qualquer alteração ou adoção de nova especificação; não solicitada nesta auditoria.
## AUD-001-27 — CORRIGIR — P2

- Item: Contagem nominal de eventos nas trajetórias.
- Justificativa: Rótulos fiscal=47, externo=54, monetário=48; valores efetivos não nulos por dia: 46–47,53,47.
- Arquivos potencialmente envolvidos: `analise.trajetoria_evento:280,297; relatorio.fig_trajetorias:182`.
- Ação proposta: Exibir n efetivo por dia ou definir amostra completa comum em revisão autorizada.
- Efeito esperado: Faixa usa n nominal enquanto nanmean ignora valores ausentes; precisão e contagem não coincidem.
- Risco científico se mantido sem tratamento: Faixas e legendas podem superestimar informação.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: sim, antes de qualquer alteração ou adoção de nova especificação; não solicitada nesta auditoria.
## AUD-001-28 — DOCUMENTAR — P2

- Item: Significado das faixas de 95%.
- Justificativa: Percentis ponto a ponto de médias placebo; não são IC da média observada nem banda simultânea de trajetória. Figura 08 usa 1,96×EP; Huber não tem HAC.
- Arquivos potencialmente envolvidos: `analise.trajetoria_evento; figuras 06,07,09`.
- Ação proposta: Explicitar referência, n, exclusões por tipo, ausência de simultaneidade e IC assintótico da robustez.
- Efeito esperado: Cruzar a faixa em um dia não equivale a rejeitar teste CAR nem teste simultâneo.
- Risco científico se mantido sem tratamento: Interpretar inspeção visual como novo teste confirmatório.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: sim, antes de qualquer alteração ou adoção de nova especificação; não solicitada nesta auditoria.
## AUD-001-31 — CORRIGIR — P2

- Item: Unidade do volume no episódio.
- Justificativa: 17,1457→26,0686 milhões são volume_base em USDT, descritos como R$ 17,1→26,1 mi. Proxy de valor HLC3×volume: R$87,23→134,36 mi.
- Arquivos potencialmente envolvidos: `docs/resultados.md §3.1; episodio.resumo; janela.volume_janela`.
- Ação proposta: Corrigir unidade em errata futura; não confundir proxy monetária com volume_brl exato.
- Efeito esperado: Não altera aumento de volume em unidades base, mas erra escala monetária.
- Risco científico se mantido sem tratamento: Erro factual na descrição de liquidez.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: sim, antes de qualquer alteração ou adoção de nova especificação; não solicitada nesta auditoria.
## AUD-001-07 — DOCUMENTAR — P3

- Item: Base estatística oficial anterior à inclusão de Trends.
- Justificativa: Reprodução acrescenta busca_usdt, busca_dólar e seus anormais; 17 colunas comuns idênticas, quatro novas.
- Arquivos potencialmente envolvidos: `dados/resultados/base_teste.csv; cli.testar`.
- Ação proposta: Identificar qual execução produziu cada base/relatório.
- Efeito esperado: Evidencia artefatos de rodadas distintas; não altera regressão principal.
- Risco científico se mantido sem tratamento: Confusão entre rodadas ao reproduzir tudo de uma vez.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: sim, antes de qualquer alteração ou adoção de nova especificação; não solicitada nesta auditoria.
## AUD-001-29 — DOCUMENTAR — P3

- Item: Google Trends e textos antigos.
- Justificativa: Trends importado e reproduzido; duas figuras presentes; narrativa ainda diz não importado e enumera oito figuras. Quadro textual cita V3–V5, omite V6.
- Arquivos potencialmente envolvidos: `docs/resultados.md:189,197; relatorio.tabelas; dados/resultados/exploratorio_*`.
- Ação proposta: Atualizar por documento novo/errata autorizado, mantendo diário histórico e origem exploratória.
- Efeito esperado: Dificulta saber o que já foi analisado.
- Risco científico se mantido sem tratamento: Leitor recebe estado desatualizado da pesquisa.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: sim, antes de qualquer alteração ou adoção de nova especificação; não solicitada nesta auditoria.
## AUD-001-35 — DOCUMENTAR — P3

- Item: Testes, dependências e preservação computacional.
- Justificativa: 41 testes passaram; um warning de precisão em caso sintético. Dependências têm limites mínimos sem lock; dados principais não rastreados apesar do diário mencionar CSV versionado.
- Arquivos potencialmente envolvidos: `pyproject.toml; tests/*; git_antes.txt; versoes.json`.
- Ação proposta: Arquivar bundle de dados, hashes, versões e comandos; testes de fronteira em tarefa futura.
- Efeito esperado: Ambiente atual reproduz; clone do commit sozinho não contém toda baseline.
- Risco científico se mantido sem tratamento: Clone futuro não reproduz e mudanças de biblioteca afetam execução.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: sim, antes de qualquer alteração ou adoção de nova especificação; não solicitada nesta auditoria.
## AUD-001-01 — MANTER — P3

- Item: Integridade física da baseline.
- Justificativa: 154 arquivos protegidos, inclusive não rastreados; comparação final em integridade_final.json.
- Arquivos potencialmente envolvidos: `Repositório; hashes_antes.json / hashes_depois.json`.
- Ação proposta: Manter o snapshot e os manifests desta execução.
- Efeito esperado: Preserva história e separa novos artefatos.
- Risco científico se mantido sem tratamento: Perda de rastreabilidade se descartados.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: não há mudança proposta; necessária somente se ampliar escopo.
## AUD-001-02 — MANTER — P3

- Item: Reconstrução dos tratados.
- Justificativa: 14 tabelas tratadas reproduzidas exatamente no recorte até 30/10/2026; comparacoes.csv.
- Arquivos potencialmente envolvidos: `fontes/*.py; janela.py; indicador.py; comportamento.py`.
- Ação proposta: Preservar os brutos e as regras da descoberta.
- Efeito esperado: Não foi necessário substituir dados por consultas novas.
- Risco científico se mantido sem tratamento: Reprodução futura depende da disponibilidade desses arquivos.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: não há mudança proposta; necessária somente se ampliar escopo.
## AUD-001-03 — MANTER — P3

- Item: Indicador, unidades e mediana causal no tempo.
- Justificativa: Ágio = P/PTAX−1; agio_pct = 100×ágio; anormal em p.p.; mediana independente coincide, diferença máxima zero.
- Arquivos potencialmente envolvidos: `indicador.calcular_agio / consolidar; analise._anormal`.
- Ação proposta: Manter distinção proporção, percentual e ponto percentual.
- Efeito esperado: Sem vazamento do próprio dia na referência da regressão.
- Risco científico se mantido sem tratamento: Confusão de escala se documentação omitir unidades.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: não há mudança proposta; necessária somente se ampliar escopo.
## AUD-001-04 — MANTER — P3

- Item: Regressão principal e HAC.
- Justificativa: n=1490; R²=0,0953508683; curtose Pearson=15,3378; MQO independente difere ≤2,23e−16 e covariância HAC ≤2,38e−14.
- Arquivos potencialmente envolvidos: `analise.regressao; regressao_agio_anormal.csv`.
- Ação proposta: Documentar inferência normal assintótica, intercepto e ausência de correção de pequena amostra.
- Efeito esperado: Coeficientes, erros-padrão e p-valores publicados reproduzem.
- Risco científico se mantido sem tratamento: Reprodução não resolve identificação causal.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: não há mudança proposta; necessária somente se ampliar escopo.
## AUD-001-05 — MANTER — P3

- Item: Regressões complementares, eventos e tabelas.
- Justificativa: 30 CSVs de resultados reproduzidos diretamente; quadro, seis estudos e comparações coincidem; Markdown igual salvo data de geração.
- Arquivos potencialmente envolvidos: `cli.testar / buscas / oferta_usdt; relatorio.tabelas`.
- Ação proposta: Conservar resultados originais como descoberta.
- Efeito esperado: Valores de referência são computacionalmente sustentados.
- Risco científico se mantido sem tratamento: Nenhum erro numérico demonstrado nesses resultados.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: não há mudança proposta; necessária somente se ampliar escopo.
## AUD-001-08 — DOCUMENTAR — P3

- Item: Reconciliação de 158 para 154 eventos.
- Justificativa: Copom 29/10/2020, Fed 06/11/2020 e relatório fiscal 21/11/2020 sem histórico/janela válida; Fed 29/10/2026 sem +3 completo.
- Arquivos potencialmente envolvidos: `analise._posicoes_eventos / _car; reconciliacao_eventos.csv`.
- Ação proposta: Publicar a tabela de fluxo de exclusões, datas cadastradas e efetivas.
- Efeito esperado: Exclusões são explicadas, sem indício de seleção por sinal.
- Risco científico se mantido sem tratamento: Contagem 158/154 parece contraditória sem fluxo explícito.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: sim, antes de qualquer alteração ou adoção de nova especificação; não solicitada nesta auditoria.
## AUD-001-09 — MANTER — P3

- Item: Definição de domésticos e externos.
- Justificativa: Domésticos=fiscal+político (50); externos=externo (53) na lista completa; isolados 32 e 15. Copom/regulação não entram no contraste.
- Arquivos potencialmente envolvidos: `analise.DOMESTICOS / EXTERNOS; decisões e pré-registro V1`.
- Ação proposta: Explicitar o universo no texto e não acrescentar categorias retrospectivamente.
- Efeito esperado: Coerente com a regra documentada; não representa todo choque brasileiro.
- Risco científico se mantido sem tratamento: Generalização indevida para todo risco doméstico.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: não há mudança proposta; necessária somente se ampliar escopo.
## AUD-001-17 — DOCUMENTAR — P3

- Item: Fusos, dias disponíveis e controles defasados.
- Justificativa: Candles UTC convertidos via America/Sao_Paulo; dias PTAX determinam a base; 11 VIX carregados de data anterior, atraso máximo três dias.
- Arquivos potencialmente envolvidos: `fontes.binance / mercadobitcoin; janela; analise.montar_base`.
- Ação proposta: Explicitar calendário observado e tratamento de feriados estrangeiros.
- Efeito esperado: Não há backfill futuro nessas junções; diferenças são por dias da base, não sessões americanas consecutivas.
- Risco científico se mantido sem tratamento: Confundir variação de um intervalo irregular com retorno diário homogêneo.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: sim, antes de qualquer alteração ou adoção de nova especificação; não solicitada nesta auditoria.
## AUD-001-20 — MANTER — P3

- Item: Holm e hipótese conjunta V1 na descoberta.
- Justificativa: Sete hipóteses; comparação com statsmodels multipletests idêntica. V1 usa máximo dos dois p-valores e exige ambos sinais.
- Arquivos potencialmente envolvidos: `analise.holm / quadro_hipoteses; hipoteses.csv`.
- Ação proposta: Manter quadro bruto+Holm e origem exploratória explícita.
- Efeito esperado: Holm pode ser usado sob dependência se p-valores marginais forem válidos; não corrige seleção anterior de análises.
- Risco científico se mantido sem tratamento: Confundir controle desta família com correção dos cerca de 40 testes exploratórios.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: não há mudança proposta; necessária somente se ampliar escopo.
## AUD-001-36 — MANTER — P3

- Item: Figuras e tabelas regeneradas.
- Justificativa: Dez figuras solicitadas idênticas byte a byte; episódio também idêntico em processo separado; tabelas idênticas exceto data.
- Arquivos potencialmente envolvidos: `relatorio.gerar; cli.buscas; episodio.rodar`.
- Ação proposta: Manter arquivos oficiais; anotar ordem/processo de geração e ressalvas de legenda.
- Efeito esperado: Concordância com gerador e dados, ressalvados erros semânticos acima.
- Risco científico se mantido sem tratamento: Igualdade de pixels não valida interpretação científica.
- Dependências: preservar snapshot/hash; revisar evidência citada e decidir procedimento antes de nova rodada.
- Aprovação do pesquisador: não há mudança proposta; necessária somente se ampliar escopo.

## ADIAR — P2 — Identificação do mecanismo e confirmação fora da amostra

- Justificativa: agregados de negócios/taker/ticket e oferta global não identificam decisões individuais, escassez de vendedores ou arbitragem local.
- Arquivos potenciais: documentos novos do projeto e protocolo futuro; preservar V4a/V4b/V6 e descoberta.
- Efeito esperado: separar confirmação de padrão estatístico da identificação causal do mecanismo.
- Risco científico: antecipar explicações como fatos ou chamar repetição de sinais de prova de motivação.
- Dependências: dados microestruturais e estratégia de identificação; amostra futura; financiamento/acesso, se pertinente.
- Aprovação do pesquisador: sim, para novo desenho. Nenhuma coleta proposta foi iniciada.

Alternativas defensáveis incluem pré-especificar um único teste final, orçamento alfa entre avaliações ou método sequencial calibrado. Não foi escolhida unilateralmente uma nova baseline. Para eventos, permutação por ano melhora comparabilidade temporal, mas pode perder poder e não elimina dependência; deslocamentos conjuntos preservam mais dependência, mas supõem estabilidade dentro de período. Decisão deve levar em conta pergunta científica, não o menor p.
