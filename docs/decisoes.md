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
