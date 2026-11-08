# Congelamento da versão para a validação

*Registrado em 05/11/2026, junto com o adendo 2 ao pré-registro. A tag `congelamento-v2` aponta para o commit que incorpora este arquivo. Para conferir: `git checkout congelamento-v2` e `sha256sum` nos arquivos abaixo.*

## Versões

| Referência | O que é |
| --- | --- |
| tag `descoberta-v1` (commit `543fdea`) | Versão original da descoberta, examinada pela AUD-001 |
| tag `congelamento-v2` | Versão corrigida pela AUD-002, com o adendo 2; é a usada na validação |

## Arquivos congelados (SHA-256)

| Arquivo | SHA-256 |
| --- | --- |
| `dados/manual/eventos.csv` | `d1a4a320d376a78aee7ad0571ea44af9a72f9517fad96b8493b2f65e615ca129` |
| `docs/pre-registro.md` | `74c52e6cf00e0d7f7961fe9091c0d419617374d0af3e252695f4c27cc71d2b3e` |
| `pyproject.toml` | `94930b782455be90c4908cfc251c08d27958c12ca164ef96878561845c9f0306` |
| `scripts/agendar_coleta_mac.sh` | `db299674ecc385db3538f9ad6ff9fd49b2d4271f08c12381ea11868cec4db8d9` |
| `scripts/coleta_semanal.sh` | `95ed0fa180704bc46983814703730434ce745a519ca926cd09bc6566afb49e86` |
| `scripts/montar_eventos.py` | `c3926d7f5f15446f9022d93b7047628314e43bf42e4efb358b3ecedd6a707df1` |
| `src/agio/__init__.py` | `fe5781dc3f63ba5a4859ad9faa1cf709902c6384425ec3dd2c2783d1f742d4f5` |
| `src/agio/analise.py` | `dbaa39791b0b5bea7bc77c26e53792c5354f9c47b75d19aa388fd0cdcbd973e1` |
| `src/agio/armazenamento.py` | `4e342724a8014a849592d4687fac993054a2250f1c61510fa34921523876b1b4` |
| `src/agio/cli.py` | `3ff8dd6f95ae9ece735217c0a2d161caa13f028e2a69e45d60c636ea8f39c235` |
| `src/agio/comportamento.py` | `baf2577d6d4403d940501de2a5b59fbb8527009e645e4d3c23ad1aecab98f1d5` |
| `src/agio/episodio.py` | `443899323866e147ee858be02196c5655e24836eb43ac509bed3c374ae47593b` |
| `src/agio/fontes/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `src/agio/fontes/bcb.py` | `c660a940e82b079136a2dd89fe25c3290927ed1c3b7b022462c0a12dc95c261d` |
| `src/agio/fontes/binance.py` | `7a09a292128c66fd096d8f19169464d211f924061945f8f027edddc2db3451ce` |
| `src/agio/fontes/defillama.py` | `aa41c516f935f702c52028636b116d65dba3d7d3a70661b3458962dd6f8f319d` |
| `src/agio/fontes/fred.py` | `364b983c527fa2ed3dc75450714104189e1951e572c2ceec8b3e8de94bd33a15` |
| `src/agio/fontes/google_trends.py` | `d2dd869629227b417f023c02579860d915f6f276600800cb8f27dbe3a2cbb27a` |
| `src/agio/fontes/mercadobitcoin.py` | `462b3d85328503ce0032b6f4551a1f5ef974636b2dfacc6306399ec89f294e77` |
| `src/agio/fontes/tesouro.py` | `df6dd70a890b1cd5dde45e1a742f9fce84ca8a13ed3961188e44bc6920db14bb` |
| `src/agio/http.py` | `c545a97a4b78001933f20211bfd22f1e88471e6e56eca23d7c43004fce00b835` |
| `src/agio/indicador.py` | `4ae32ecd9d9435fab6c9b9761de9fb0e62f17b2162b8ea274ec83055a80f3711` |
| `src/agio/janela.py` | `47846b7a818c0c423196642a8ba73a8b085d246d3211a9574a1ea8038b9f97b7` |
| `src/agio/relatorio.py` | `a32893a24d433253fe02a4defadbf5b411fb75b706cd2b923e00fe069299ee21` |
| `tests/test_analise.py` | `aff4448ee7e7048a3584db44185ecc5f78b8b34682f122a1df12b76b6907309c` |
| `tests/test_aud002.py` | `bb2ad1770ac571586343568b27ba115e87184b3de36a7567c9e16bca11731aa8` |
| `tests/test_aud002_hipoteses.py` | `9afdf27d1df09ce504ba8fb2930bf9884ec021bdf1b861084a8af570a1766698` |
| `tests/test_comportamento.py` | `89c479ddc7b7b00941c03c397ee920a33e4c2afe700b31adfa4f81433b6d9504` |
| `tests/test_janela.py` | `172f3f882814b87ab93257cd5bb49b1fb6834272795a4d86031bbd3974644ac7` |
| `tests/test_tratamento.py` | `35e33906a53d6fb041e956dd0d972b54e9a76cc99e31859bd52d3514610a12f9` |

Os hashes de `docs/pre-registro.md` e deste arquivo não se aplicam a adendos futuros, que entram no fim do pré-registro com data.

### Atualizações previstas no adendo 2 (P4)

Inclusão de calendários da validação, registrada em `decisoes.md`. A versão original de cada arquivo continua na tag `congelamento-v2`.

| Data | Arquivo | SHA-256 novo | Motivo |
| --- | --- | --- | --- |
| 07/11/2026 | `scripts/montar_eventos.py` | `34c1a45cd5747c70ff242cafc98bef2690eb21da4a07f2d59fb6809d551f5e5d` | Copom e Fed de nov/dez 2026 e 2027; fiscais por regra de 2027. `eventos.csv` não muda |

## Dependências

`pyproject.toml` fixa versões mínimas (pandas ≥ 2.1, statsmodels ≥ 0.14, scipy ≥ 1.11, matplotlib ≥ 3.8, requests ≥ 2.31). Os resultados da descoberta foram reproduzidos de forma idêntica em dois ambientes:

| Pacote | Auditoria (macOS) | Reprodução independente (Linux) |
| --- | --- | --- |
| Python | 3.14.6 | 3.13.18 |
| pandas | 3.1.0 | 3.0.5 |
| numpy | 2.5.4 | 2.5.3 |
| scipy | 1.18.1 | 1.18.1 |
| statsmodels | 0.15.0 | 0.15.0 |
| matplotlib | 3.11.2 | 3.11.2 |

Diferenças só na última casa decimal (cerca de 1e−16) nos CSVs das figuras; resultados estatísticos idênticos. As imagens PNG diferem byte a byte entre ambientes, sem diferença de conteúdo.

## Exposição a dados posteriores a 30/10/2026

- **Coletado:** a coleta semanal gravou dados de 31/10 e 01/11/2026 (fim de semana, sem PTAX) e continua gravando, como exige o pré-registro.
- **Analisado:** nenhum comando de análise (`testar`, `robustez`, `relatorio`, `grafico`, `episodio`, `buscas`, `oferta-usdt`) rodou sobre datas a partir de 02/11/2026. A amostra de descoberta termina em 30/10/2026 (última PTAX usada).
- **Auditorias:** reutilizaram os dados brutos já coletados, sem novas consultas e sem datas da validação.

## Verificação antes da tag

- `pytest`: 64 testes aprovados com os dados coletados; num clone sem dados, 62 aprovados e 2 pulados (os que conferem a lista de eventos e os lotes horários com os dados reais).
- `agio testar` e `agio robustez` com os caminhos de sempre: resultados idênticos aos de `resultados_v2` da AUD-002; só muda o rótulo da V6.
- `python scripts/montar_eventos.py`: gera exatamente `dados/manual/eventos.csv` (158 eventos).
