# Diário de decisões metodológicas

Cada entrada: data, decisão, motivo, alternativa descartada. Vira a seção de método do TCC.

## 2026-10-30 — Definição do indicador

- **Decisão:** ágio = fechamento diário do USDT/BRL ÷ PTAX de venda − 1.
- **Motivo:** a PTAX é a referência oficial e pública; o USDT concentra a maior parte do volume de stablecoins negociado em reais.
- **Descartado:** dólar comercial de mercado (fonte paga) e USDC como série principal (volume menor; pode entrar como robustez).

## 2026-10-30 — Dias considerados

- **Decisão:** ágio só em dias úteis com PTAX; preços de fim de semana ficam guardados.
- **Motivo:** não existe referência oficial no fim de semana.
- **A testar:** usar a PTAX do último dia útil para cobrir fins de semana em choques que começam no domingo (como o segundo turno de 2026).

## 2026-10-30 — Descasamento de horário

- **Decisão:** aceitar, por ora, o descasamento entre a PTAX (por volta das 13h de Brasília) e o fechamento do candle (21h de Brasília).
- **Motivo:** simplicidade na primeira versão; o efeito é ruído.
- **Próximo passo:** candles horários, pegando o preço por volta das 13h, para alinhar com a PTAX.

## 2026-10-30 — Consolidação entre corretoras

- **Decisão:** ágio diário consolidado ponderado pelo volume de cada corretora.
- **Motivo:** evita que uma corretora pequena e ilíquida domine o indicador.
- **Robustez:** manter o ágio por corretora em `agio_por_fonte.csv` para comparar.

## 2026-10-30 — Armazenamento

- **Decisão:** respostas brutas em JSON com horário da coleta; tabelas tratadas em CSV versionado no Git.
- **Motivo:** reprodutibilidade e diferenças legíveis no Git. Migrar para Parquet ou DuckDB quando a base crescer (mestrado).

## 2026-10-31 — Sinais de comportamento coletivo

- **Decisão:** incluir três sinais de mercado (pressão compradora, número de negócios, ticket médio em reais) e o interesse de busca do Google Trends.
- **Motivo:** completar a tríade economia, comportamento e TI, explicando por que o ágio sobe (medo, efeito manada, atenção), não só se sobe.
- **Limite:** dados agregados; o texto fala em comportamento coletivo, sem atribuir motivações individuais (falácia ecológica).
- **Descartado no TCC:** questionário com investidores (exige comitê de ética e alonga o prazo); fica para o mestrado.

## 2026-10-31 — Google Trends por CSV

- **Decisão:** importar CSVs exportados manualmente, em janelas de até 8 meses sobrepostas em 30 dias ou mais, encadeadas pela razão média na sobreposição.
- **Motivo:** bibliotecas não oficiais costumam ser bloqueadas e mudam sem aviso; o CSV é reproduzível e citável.
- **Cuidado:** guardar os CSVs originais no repositório e registrar a data de exportação, porque o Google reamostra os dados a cada consulta.

## 2026-10-31 — Ágio alinhado à janela da PTAX

- **Decisão:** a medida principal passa a usar o preço médio do USDT, ponderado pelo volume, entre 10h e 13h de Brasília (13h a 16h UTC), a mesma janela em que o Banco Central forma a PTAX. O ágio de fechamento (candle diário, 21h) fica como comparação.
- **Motivo:** na primeira coleta (out/2020 a out/2026), os menores ágios da série caíram justamente em dias de choque: 09/04/2025 (−3,5%), 26/10/2026 (−2,1%, dia seguinte ao segundo turno) e 06/11/2024 (−1,8%). A explicação provável é o horário: a PTAX registra o câmbio da manhã, e o fechamento das 21h registra o mercado já acalmado. O descasamento é maior exatamente nos dias que mais importam para o estudo.
- **Detalhes:** preço típico de cada hora, (máxima + mínima + fechamento) / 3, ponderado pelo volume; sem volume na janela, média simples dos fechamentos. O Brasil não tem horário de verão desde 2019, então a janela é fixa em UTC.
- **A verificar:** quantos dias ficam sem negociação na janela no início da série (2020–2021), quando o volume era baixo.

## 2026-10-31 — Resultados preliminares da série alinhada (out/2020 a out/2026)

*Análise descritiva, sem teste formal. Ágio anormal = ágio do dia menos a mediana dos 60 dias úteis anteriores.*

- **A correção de horário funcionou:** 09/04/2025 passou de −3,5% (fechamento) para cerca de 0% (janela da PTAX). A correlação entre as duas medidas é 0,54, e o desvio padrão de 2025 caiu de 0,53 para 0,19 p.p.
- **Custo:** a correlação entre corretoras caiu de 0,91 para 0,68, porque a janela de 3 horas tem menos negócios, sobretudo no Mercado Bitcoin. A consolidação por volume reduz o efeito.
- **Choques domésticos não elevaram o ágio:** pacote fiscal (29/11/2024, −1,5 p.p. anormal), segundo turno (26/10/2026, −0,8 p.p.). Primeiro turno (05/10/2026): +0,24 p.p.
- **O maior ágio anormal foi externo:** 05/08/2024, +3,0 p.p. (turbulência global).
- **A participação reage com força:** o número de negócios dobra ou triplica nas crises (dez/2024: 140 a 170 mil por dia contra cerca de 60 mil; 05/08/2024: 179 mil; 26/10/2026: 105 mil contra cerca de 46 mil), e o ticket médio cai (entrada do varejo).
- **Interpretação a testar:** quando o dólar oficial dispara, detentores de USDT vendem para realizar ganho e seguram o preço; a pressão compradora abaixo de 0,5 nesses dias é compatível.
- **Episódio a investigar:** de 24/06 a meados de julho de 2026, ágio entre 1% e 1,7% por semanas seguidas, sem paralelo na série. Verificar mudança tributária ou regulatória sobre stablecoins no período.
- **Possível reformulação da hipótese (só depois do teste formal):** o medo fiscal se manifestaria na participação no mercado de dólar digital, e não no prêmio de preço.

### Próximos testes

1. Regressão do ágio anormal controlando pela variação do dólar oficial no dia.
2. Janela da PTAX incluindo a hora das 13h: o Banco Central consulta às 10h, 11h, 12h e 13h, e a janela atual vai até 12h59.
3. Mesma análise de evento para o número de negócios e o ticket médio.

## 2026-10-31 — Teste formal: desenho e regra de decisão

- **Regressão (todos os dias, Newey-West com 5 defasagens):** ágio anormal ~ variação do dólar oficial + variação do juro real de 10 anos (bp) + variação do VIX (no dia e no anterior) + tamanho do mercado. O mesmo para número de negócios e ticket médio.
- **Juro real de 10 anos:** taxas de compra da manhã dos títulos Tesouro IPCA+ (sem cupom), interpoladas no prazo de 10 anos. Taxa da manhã para coincidir com a janela da PTAX.
- **VIX:** o fechamento em Nova York sai depois da janela da PTAX; por isso entram a variação do dia e a do dia anterior.
- **Estudo de evento:** janela de −1 a +3 dias úteis; ágio anormal acumulado; teste t e teste de permutação contra datas sorteadas fora de ±10 dias úteis dos eventos; comparação domésticos (fiscal, político) x externos por permutação de rótulos.
- **Ágio ajustado pelo dólar:** resíduo da regressão do ágio anormal sobre a variação do dólar, para o estudo de evento não confundir o efeito mecânico do câmbio com reação ao medo.
- **Regra de decisão:** hipótese original confirmada se o coeficiente do juro real for positivo e significativo a 5% e os domésticos tiverem ágio anormal maior que os externos; versão comportamental confirmada se a participação for significativamente maior nas crises.
- **Lista de eventos:** rascunho com 15 eventos marcados como A CONFIRMAR; a versão final deve ser fixada, com fontes, antes de interpretar os resultados.

## 2026-10-31 — Primeira rodada do teste (sem juro real e VIX)

- **Efeito mecânico do dólar confirmado:** coeficiente de −0,11 (t = −9,6): cada 1% de alta do dólar oficial no dia reduz o ágio em 0,11 p.p. O controle é indispensável.
- **Estudo de evento com 15 eventos:** nenhum grupo significativo, nem no ágio nem no número de negócios. Nos negócios, o teste t contra zero dá p = 0,013 para todos os eventos, mas a permutação dá p = 0,25: o número de negócios anormal é positivo em média (mercado em crescimento), e a comparação certa é com datas sorteadas.
- **Leitura:** com 2 a 6 eventos por grupo, o teste tem pouco poder. Prioridade: ampliar a lista (todas as reuniões do Copom, anúncios fiscais) e incluir juro real e VIX.
