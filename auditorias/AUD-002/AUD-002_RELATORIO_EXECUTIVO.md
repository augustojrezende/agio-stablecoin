# AUD-002 — Relatório executivo

Versão V2 / AUD-002. Origem: `543fdea26bc734fbea6d0fa712e5213c0d75d06a`. Data de fechamento: 02/11/2026.

As sete correções comprovadas foram implementadas exclusivamente na cópia física independente. Nenhuma correção bloqueada ou pendente. O pesquisador autorizou incluir os arquivos não rastreados e definiu as duas políticas ambíguas antes da implementação: V1 exige pelo menos 10 eventos domésticos e 10 externos elegíveis; V5 indisponível conserva a posição na família de sete, com p observado ausente e 1 apenas internamente no cálculo conservador de Holm.

A suíte passou de 41 testes originais aprovados para 64 aprovados, zero falhas. Os 23 novos casos cobrem os sete achados. As falhas registradas antes dos patches demonstram regressões; não são falhas remanescentes. Há um aviso de precisão numérica em teste sintético preexistente. O pipeline foi reconstruído a partir dos arquivos brutos locais, sem nova coleta; as nove especificações de robustez executaram.

Preservados: 1.520 observações do indicador, 1.490 na regressão principal, coeficientes, valores-p das regressões, nove especificações de robustez e decisões das sete hipóteses. A amostra isolada passou de 62 para 60 eventos: as sobreposições de Copom 28/10/2021 e Fed 04/11/2021 foram corrigidas. O contraste domésticos–externos de ágio anormal isolado passou de p=0,0526 para 0,0434; esta passagem pelo limiar é explicitamente reportada, sem seleção de resultado. V5 passou de p=0,0348 / Holm=0,1044 para 0,024 / 0,072: continua sem confirmação após Holm. V1 permanece não confirmada.

Cinco figuras mudaram por mediana ou contagens efetivas; seis ficaram idênticas byte a byte. Médias e faixas das 12 trajetórias permanecem iguais. O episódio utiliza 17,1457 → 26,0686 milhões de USDT (+52,0411%), corrigindo a unidade antes apresentada como reais.

Dos 430 arquivos inventariados, 428 mantiveram hashes e duas referências internas .git/refs/codex/turn-diffs ficaram ausentes. O snapshot foi preservado. O aceite formal é parcial quanto à exigência de integridade integral, embora as sete correções estejam concluídas e os arquivos científicos preservados. Nenhum commit, push ou AUD-003 foi iniciado. Evidências detalhadas estão nos quatro documentos complementares, CSVs, logs, patch e manifesto de proveniência desta pasta.
