# AUD-002 — Integridade

Versão V2 / AUD-002. Origem: `543fdea26bc734fbea6d0fa712e5213c0d75d06a`. Data de fechamento: 02/11/2026.

Original: `/Users/augustojrezende/Projetos/agio-stablecoin`. Cópia física: `/Users/augustojrezende/Projetos/agio-stablecoin_v2`. Branch de origem: main. Não foi usado worktree.

Verificados 430 arquivos por SHA-256 antes/depois, incluindo .git; 428 hashes iguais e duas referências internas de checkpoints/capturas do Codex ausentes (ver integridade_final.json). Não houve comando desta auditoria para removê-las; a causa não foi verificada. Assim, não se afirma integridade integral dos 430 arquivos. Listas completas: hashes_original_antes.json e hashes_original_depois.json. O inventário e tamanhos constam em inventario_original.json. O snapshot preserva 150 arquivos e coincide com os hashes iniciais. Nenhum hardlink compartilhado entre os arquivos inventariados. A preparação registrou ausência de symlinks e cópia física independente do ambiente, com .pth direcionado à V2 e caches próprios.

O estado inicial tinha zero modificações rastreadas e 121 arquivos não rastreados; sua inclusão foi autorizada. Estados Git estão em git_original_inicial.txt, git_original_final.txt e git_v2_final.txt. A configuração remota e HEAD mantiveram hashes; a exceção são as duas referências internas do Codex mencionadas. Não houve commit/push. A alteração do conteúdo rastreado da V2 está em alteracoes_v2.patch; os novos arquivos integram o pacote.

Comandos e procedimentos: preparar.py registra cópia e ambiente; aplicar_cinco.py e aplicar_hipoteses.py registram patches de uso único; validar.py executa testes, comando real robustez, replay offline e comparações. comandos_validacao.json registra subprocessos; pipeline_v2.log e episodio_v2.log registram execução. Não reexecute os scripts de patch sobre código já corrigido.

Reprodução no ambiente preparado: `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python auditorias/AUD-002/validar.py`, a partir da V2. O script guarda caminhos absolutos locais e usa o snapshot; ao mover o pacote é necessário ajustar R e recriar ambiente. Dependências e sys.prefix constam em validacao_resumo.json. Nenhum download é necessário para esta execução local preparada.

manifesto_proveniencia_v2.json associa cada resultado a versão, commit, código/entradas com hashes, parâmetros, datas e razão/impacto. A data de modificação de cada saída é registrada separadamente da data de fechamento documental. O ZIP tem inventário SHA-256 interno; exclui .git, ambiente virtual e caches, preservando código, dados, documentos e evidências necessários. O pacote não substitui a cópia operacional independente.
