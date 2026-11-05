# AUD-001 — Reprodutibilidade e rastreabilidade

## Snapshot e ambiente

Branch `main`; commit `543fdea26bc734fbea6d0fa712e5213c0d75d06a`. Git não apresentava alterações em arquivos rastreados, mas havia numerosos arquivos não rastreados preexistentes (brutos, tratados, resultados e .DS_Store). Relação integral em git_antes.txt. Auditoria é somente diretório novo `auditorias/AUD-001/`; não houve commit, push, coleta remota, mudança em src/tests/dados/docs/scripts ou instalação de dependências.

Snapshot de **154 arquivos** fora de .git/.venv/caches/auditorias: hashes_antes.json e hashes_depois.json. Esses arquivos incluem código, documentação, figuras, manuais e todos os brutos/tratados/resultados encontrados. Integridade final: ver integridade_final.json. Hash prova preservação do conteúdo local, não autenticidade da fonte externa. Git, caches e ambiente virtual não são tratados como dados científicos protegidos.

Python `3.14.6 (main, Jun 10 2026, 10:03:53) [Clang 21.0.0 (clang-2100.0.123.102)]`; `macOS-27.0-arm64-arm-64bit-Mach-O`.

| pacote | versão |
|---|---|
| numpy | 2.5.4 |
| pandas | 3.1.0 |
| scipy | 1.18.1 |
| statsmodels | 0.15.0 |
| matplotlib | 3.11.2 |
| requests | 2.34.2 |
| pytest | 9.2.0 |

O pyproject aceita Python≥3.10 e dependências sem limite superior. Não foi validada compatibilidade de todas as versões permitidas (por exemplo, uso de include_groups depende da versão pandas). O ambiente acima é a evidência efetiva, sem atualização de pacote.

## Isolamento e comandos

Cópia temporária em `/private/tmp/AUD-001-62cglz_p`. Módulos importados exclusivamente de `/private/tmp/AUD-001-62cglz_p/src`; Python do ambiente existente. Rede de requests bloqueada explicitamente no replay. Nenhum endpoint de dados foi consultado. Brutos foram ordenados por carimbo de coleta, último lote prevalece por chave; observações posteriores a 30/10/2026 foram removidas antes da construção final. Para Trends, janelas também foram cortadas antes de encadear. As coletas são vintages de 01/11/2026; isso não certifica informação disponível em tempo real no passado.

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

| Fonte | Bruto/insumo | Transformação | Saída/variável | Análise/regra | Resultado/figura | Situação |
|---|---|---|---|---|---|---|
| BCB Olinda/SGS | dados/bruto/bcb_ptax, bcb_selic | fontes.bcb.tratar_ptax/tratar_sgs; atualizar_tratado | ptax.csv, selic.csv | indicador e d_dolar | ágio, regressões, figs 01–05 | reproduzido; Selic não integra regressão principal |
| Binance e Mercado Bitcoin | dados/bruto/{binance,mercadobitcoin} e *_1h | tratar/tratar_horario; janela.preco_janela_ptax | precos_usdt_brl; precos_janela_ptax | HLC3×volume, ágio; sinais_mercado | agio_*; painel; figs 01–07 | reproduzido; índice duplicado bloqueia CLI robustez |
| Tesouro Transparente | dados/bruto/tesouro_direto/*.csv | tesouro.tratar; juro_real_10a | juro_real_10a.csv | diferença×100 bp; MQO/HAC | regressao_*; fig08 | reproduzido; vintage não comprova hora de publicação |
| Cboe (fallback FRED) | dados/bruto/cboe_vix/*.csv | fred.tratar_cboe; merge_asof backward | vix.csv | d_vix e shift anterior | regressões, robustez | reproduzido; contemporâneo ex post |
| Google Trends manual | dados/manual/google_trends/*.csv | ler_csv; encadear razão de médias de sobreposição | google_trends; painel | log1p, mediana anterior; buscas | exploratorio_atencao/eventos; 09_buscas_* | reproduzido; comprar dólar excluído por suporte insuficiente |
| DefiLlama | dados/bruto/defillama_usdt/*.json | defillama.tratar; regressao_oferta_usdt | usdt_oferta.csv | log retorno 5 observações diárias, +1 dia calendário | exploratorio_oferta_usdt; episódio | reproduzido; latência histórica não provada |
| Calendários/notícias/prazos | scripts/montar_eventos.py; manual/eventos.csv | montar; _posicoes_eventos; _car | 158 cadastrados,154 elegíveis | −1,+3; placebos; rótulos; trajetórias | eventos_*.csv; figs 04,06,07,09 | script igual célula a célula; calendário de sobreposição tem erro |
| Tratados anteriores | 14 CSVs tratados | analise.montar_base; _anormal; ajustar_pelo_dolar | base_teste; base_buscas | MQO, HAC, repasse, Holm | resultados/*.csv; resultados_tabelas.md | comuns exatos; quatro colunas Trends ausentes na base antiga |

Inventário físico completo: inventario_arquivos.csv; cobertura, faltantes e duplicidades por tabela: inventario_dados.json; validação de candles: horarios.json. Os preços diários mantêm datas de abertura UTC e fecham aproximadamente às 21h de Brasília; negócios/ticket usam o dia completo, incluindo horas posteriores à janela PTAX. Não devem ser lidos como comportamento exclusivamente durante a janela.

## Comparação quantitativa

Tolerância declarada: `abs(a-b) ≤ 1e-10 + 1e-8×abs(b)`, NaN apenas igual a NaN; diferenças relativas usam denominador mínimo 1e−12 para evitar divisão por zero. São tolerâncias de arredondamento, não econômicas. As tabelas que coincidiram tiveram diferença observada zero, inclusive coeficientes, EP e p-valores. Comparação matricial independente admite arredondamento numérico (máximo 2,38e−14 para covariância).

| arquivo | n_original | n_reproduzido | divergencias | max_abs | status |
|---|---|---|---|---|---|
| dados/tratado/agio_diario.csv | 1520 | 1520 | 0 | 0 | reproduzido |
| dados/tratado/agio_fechamento_diario.csv | 1520 | 1520 | 0 | 0 | reproduzido |
| dados/tratado/agio_fechamento_por_fonte.csv | 2434 | 2434 | 0 | 0 | reproduzido |
| dados/tratado/agio_por_fonte.csv | 2434 | 2434 | 0 | 0 | reproduzido |
| dados/tratado/google_trends.csv | 4502 | 4502 | 0 | 0 | reproduzido |
| dados/tratado/juro_real_10a.csv | 5314 | 5314 | 0 | 0 | reproduzido |
| dados/tratado/painel_diario.csv | 1520 | 1520 | 0 | 0 | reproduzido |
| dados/tratado/precos_janela_ptax.csv | 3537 | 3537 | 0 | 0 | reproduzido |
| dados/tratado/precos_usdt_brl.csv | 3539 | 3539 | 0 | 0 | reproduzido |
| dados/tratado/ptax.csv | 1527 | 1527 | 0 | 0 | reproduzido |
| dados/tratado/selic.csv | 1527 | 1527 | 0 | 0 | reproduzido |
| dados/tratado/sinais_comportamento.csv | 3539 | 3539 | 0 | 0 | reproduzido |
| dados/tratado/usdt_oferta.csv | 3258 | 3258 | 0 | 0 | reproduzido |
| dados/tratado/vix.csv | 9306 | 9306 | 0 | 0 | reproduzido |
| dados/resultados/base_buscas.csv | 1520 | 1520 | 0 | 0 | reproduzido |
| dados/resultados/base_teste.csv | 1520 | 1520 | -1 | 0 | colunas comuns exatas; 4 colunas Trends novas |
| dados/resultados/episodio_20260601_20260815.csv | 115 | 115 | 0 | 0 | reproduzido |
| dados/resultados/eventos_agio_ajustado_dolar.csv | 154 | 154 | 0 | 0 | reproduzido |
| dados/resultados/eventos_agio_ajustado_dolar_sem_sobrepostos.csv | 62 | 62 | 0 | 0 | reproduzido |
| dados/resultados/eventos_agio_anormal.csv | 154 | 154 | 0 | 0 | reproduzido |
| dados/resultados/eventos_agio_anormal_sem_sobrepostos.csv | 62 | 62 | 0 | 0 | reproduzido |
| dados/resultados/eventos_comparacao_agio_ajustado_dolar.csv | 1 | 1 | 0 | 0 | reproduzido |
| dados/resultados/eventos_comparacao_agio_ajustado_dolar_sem_sobrepostos.csv | 1 | 1 | 0 | 0 | reproduzido |
| dados/resultados/eventos_comparacao_agio_anormal.csv | 1 | 1 | 0 | 0 | reproduzido |
| dados/resultados/eventos_comparacao_agio_anormal_sem_sobrepostos.csv | 1 | 1 | 0 | 0 | reproduzido |
| dados/resultados/eventos_comparacao_negocios_anormal.csv | 1 | 1 | 0 | 0 | reproduzido |
| dados/resultados/eventos_comparacao_negocios_anormal_sem_sobrepostos.csv | 1 | 1 | 0 | 0 | reproduzido |
| dados/resultados/eventos_grupos_agio_ajustado_dolar.csv | 8 | 8 | 0 | 0 | reproduzido |
| dados/resultados/eventos_grupos_agio_ajustado_dolar_sem_sobrepostos.csv | 7 | 7 | 0 | 0 | reproduzido |
| dados/resultados/eventos_grupos_agio_anormal.csv | 8 | 8 | 0 | 0 | reproduzido |
| dados/resultados/eventos_grupos_agio_anormal_sem_sobrepostos.csv | 7 | 7 | 0 | 0 | reproduzido |
| dados/resultados/eventos_grupos_negocios_anormal.csv | 8 | 8 | 0 | 0 | reproduzido |
| dados/resultados/eventos_grupos_negocios_anormal_sem_sobrepostos.csv | 7 | 7 | 0 | 0 | reproduzido |
| dados/resultados/eventos_negocios_anormal.csv | 154 | 154 | 0 | 0 | reproduzido |
| dados/resultados/eventos_negocios_anormal_sem_sobrepostos.csv | 62 | 62 | 0 | 0 | reproduzido |
| dados/resultados/exploratorio_atencao.csv | 8 | 8 | 0 | 0 | reproduzido |
| dados/resultados/exploratorio_eventos_busca_dolar_anormal.csv | 8 | 8 | 0 | 0 | reproduzido |
| dados/resultados/exploratorio_eventos_busca_usdt_anormal.csv | 8 | 8 | 0 | 0 | reproduzido |
| dados/resultados/exploratorio_oferta_usdt.csv | 7 | 7 | 0 | 0 | reproduzido |
| dados/resultados/hipoteses.csv | 7 | 7 | 0 | 0 | reproduzido |
| dados/resultados/regressao_agio_anormal.csv | 6 | 6 | 0 | 0 | reproduzido |
| dados/resultados/regressao_negocios_anormal.csv | 6 | 6 | 0 | 0 | reproduzido |
| dados/resultados/regressao_repasse.csv | 9 | 9 | 0 | 0 | reproduzido |
| dados/resultados/regressao_repasse_soma.csv | 1 | 1 | 0 | 0 | reproduzido |
| dados/resultados/regressao_ticket_anormal.csv | 6 | 6 | 0 | 0 | reproduzido |
| dados/resultados/robustez.csv | 9 | 9 | 0 | 0 | CLI falhou; comparação inicial era cópia; ver robustez_recalculada_auditoria.csv |

Resumo: **14 tratados** exatos; **30 resultados CSV** reproduzidos diretamente; **uma base** com 17 colunas comuns exatas e quatro Trends novas; **uma robustez** cuja CLI falha, mas nove linhas recalculadas com funções coincidem exatamente. São 46 CSVs oficiais examinados. A linha inicial de comparação de robustez era uma cópia preservada: NÃO foi contada como replay da CLI. Evidência autônoma está em robustez_recalculada_auditoria.csv e complementos.json.

Comparacoes_colunas.csv contém nulos implícitos via comparação, mínimos/máximos/médias, diferenças absolutas e relativas por coluna. Não houve divergência de datas nos tratados recortados. PTAX tem 1527 dias desde 01/10/2020; sete dias anteriores ao início de negociação em 13/10 não entram no ágio. Ágio=1520 dias, regressão=1490 após mínimo de 30 dias. Para MB isolado, anormal é reconstruído na própria série e há 884 observações, não uma amostra emparelhada à Binance.

## Exclusões de eventos

| data | tipo | descricao | motivo |
|---|---|---|---|
| 2020-10-29 00:00:00 | monetario | Decisão do Copom | histórico mínimo de 30 dias / janela contém NaN |
| 2020-11-06 00:00:00 | externo | Decisão do Fed (FOMC) | histórico mínimo de 30 dias / janela contém NaN |
| 2020-11-21 00:00:00 | fiscal | Relatório de Avaliação de Receitas e Despesas Primárias, 5º bimestre de 2020 | histórico mínimo de 30 dias / janela contém NaN |
| 2026-10-29 00:00:00 | externo | Decisão do Fed (FOMC) | janela final incompleta |

No evento fiscal cadastrado 21/11/2020 (sábado), a data efetiva é 23/11; a janela ainda inclui dia sem anormal. As quatro exclusões valem para os resultados principais auditados. Cadastro não tem duplicata exata data/tipo/descrição; eventos distintos na mesma data são mantidos. 23 datas cadastradas são mapeadas ao próximo dia disponível, registrado em reconciliacao_eventos.csv. Lista completa elegível: fiscal46, político4, externo53, monetário47, regulatório4. Sem sobrepostos cadastrados:62. Todos os 158 eventos do script coincidem com o CSV, sem alteração manual detectável.

## Figuras, testes e limites

Dez figuras solicitadas reproduzidas com SHA idêntico e inspecionadas visualmente em contato_figuras.png. Figura adicional do episódio também idêntica quando gerada em processo separado: a primeira execução no mesmo processo herdou rcParams de relatorio, alterando aparência, não dados (episodio_render.json). Figura 05 mostra reta simples sem controles, corretamente distinta do coeficiente multivariado. Figura 08 usa os EPs oficiais, conferidos pelo recálculo. Figuras 06/07/09 usam −5,+10 e faixa placebo, não a mesma amostra/estatística do CAR −1,+3. Defeitos de legenda, n e medianas estão classificados na matriz.

**41 testes existentes passaram**, um warning de perda de precisão em dados sintéticos quase constantes. Nenhum teste da baseline foi alterado. Não foram executados testes de rede, novas coletas, validação fora da amostra ou afirmação de completude de todas as fontes primárias. Suplementos estão em scripts próprios, não em tests/.

Não declaramos reprodução integral automatizada do pipeline: a CLI robustez falha. Tampouco certificamos publicação histórica de cada dado, horários efetivos de todo anúncio fiscal, autenticidade externa de toda observação ou validação empírica 2027/2028. A reprodução local dos números é ampla e delimitada, não um certificado de validade causal.

## Fontes externas consultadas somente como documentação/metadados

Consulta em 02/11/2026; nenhum valor externo foi incorporado à amostra. BCB descreve quatro consultas com a última após 13h; isso sustenta a ressalva de janela aproximada: [BCB, metodologia PTAX](https://www.bcb.gov.br/detalhenoticia/12847/nota) e [REB 2018, seção PTAX](https://www.bcb.gov.br/content/publicacoes/relatorioeconomiabancaria/reb_2018.pdf). O calendário institucional confirma reunião FOMC em 27–28/10/2026, compatível com evento em 29/10: [Federal Reserve Bank of Chicago](https://www.chicagofed.org/utilities/about-us/federal-reserve-calendars). A norma oficial prevê informações para operações a partir de 03/11/2026; sua vigência é publicação: [Resolução BCB 574](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?numero=574&tipo=Resolu%C3%A7%C3%A3o+BCB). Não se certificou o horário da notícia de 18/06.

Para inferência, [documentação de HAC](https://www.statsmodels.org/dev/generated/statsmodels.stats.sandwich_covariance.cov_hac.html) foi usada como referência de método; defaults efetivos vieram do modelo instalado, não do default dessa função isolada. A ressalva do p Monte Carlo se apoia no artigo original [Phipson e Smyth](https://arxiv.org/abs/1603.05766). Consultas atuais são metadados de verificação e não reconstrução de dados posteriores ao corte.
