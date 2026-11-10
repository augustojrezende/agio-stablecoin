# The stablecoin premium in Brazilian reais

*English version of the [README](../../README.md). The Portuguese documentation is the authoritative version.*

A daily indicator of the premium of USDT traded in Brazilian reais over the official dollar rate (PTAX), and its reaction to domestic and external shocks (2020–2026). Open code and data for the undergraduate thesis in Economics *O ágio da stablecoin em reais: reação a choques domésticos e externos no Brasil (2020–2026)* [The stablecoin premium in reais: reaction to domestic and external shocks in Brazil (2020–2026)].

**[Public premium dashboard](https://augustojrezende.github.io/agio-painel/)** (in Portuguese): the daily series in the PTAX window and at the close, updated weekly, with explanations for newcomers.

**[Full program manual](manual.md)**: what it does, concepts, technologies, all commands and parameters, output files and methods.

## In a nutshell

A **stablecoin** is a crypto asset designed to be always worth US$ 1, a "digital dollar". The most used in Brazil is **USDT** (Tether), bought on crypto exchanges with Pix (instant payment), 24 hours a day.

The **premium** (*ágio*) is how much more expensive (or, as a discount, cheaper) USDT is than the Central Bank of Brazil's official dollar rate (PTAX), in percent. If the PTAX is R$ 5.00 and USDT costs R$ 5.05, the premium is 1%. The premium shows the demand for dollars outside the official FX market; the program measures it every day and tests which kinds of news it reacts to.

```
premium = USDT/BRL price in the PTAX window (10:00 to 13:00 Brasília time) / PTAX selling rate − 1
```

The measure uses the USDT price in the same time window in which the PTAX is formed, so that prices from the same moment are compared. Using the daily closing price instead (21:00 Brasília time, 00:00 UTC) produces spurious extreme values on news days and changes the sign of some results; see [results](results.md#2-check-the-measurement-time).

## Main results (Oct/2020 to Oct/2026)

- When the official dollar rises 1%, the premium falls about 0.13 percentage points on the same day and keeps falling for two days: USDT follows the official exchange rate only partly.
- Global fear (VIX) is associated with a higher premium (positive in 7 of 9 specifications), above all in 2020–2022.
- Domestic fiscal stress (10-year real interest rate) barely moves the premium, and fiscal announcements do not affect it more than ordinary days.

These are observed associations, not causal relationships. The new results will be confirmed with future data, as set out in the [pre-registration](pre-registration.md). The code went through three independent audits; reports (in Portuguese) in [`auditorias/`](../../auditorias/).

Details, figures and all checks in [results](results.md).

## Quick start

```bash
git clone https://github.com/augustojrezende/agio-stablecoin.git
cd agio-stablecoin
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest                             # 64 tests, no network

agio coletar --inicio 2020-10-01   # daily prices, PTAX and Selic
agio coletar-horario --inicio 2020-10-01
agio coletar-controles             # real interest rate and VIX
agio calcular                      # premium and daily panel
agio testar                        # formal test
agio robustez                      # 9 specifications
agio relatorio                     # figures and tables
```

Commands, file names and figure labels are in Portuguese; see the [glossary](manual.md#glossary-of-portuguese-terms).

## Commands

| Command | What it does |
| --- | --- |
| `coletar`, `coletar-horario` | USDT/BRL prices (daily and hourly), PTAX and Selic |
| `coletar-controles` | 10-year real interest rate and VIX |
| `importar-trends` | Google Trends searches (CSVs exported by hand) |
| `calcular`, `grafico` | Premium, behavioural signals, daily panel and quick chart |
| `testar` | Regressions, event study and hypothesis table; with `--inicio`/`--fim`, out-of-sample validation |
| `robustez` | The regression in 9 alternative specifications |
| `buscas`, `oferta-usdt`, `episodio` | Exploratory analyses and diagnosis of atypical periods |
| `relatorio` | Thesis figures and tables |

All parameters, with examples, are in the [manual](manual.md#commands-and-parameters).

## Sources (all free, no key required)

Central Bank of Brazil (PTAX and Selic), Binance and Mercado Bitcoin (USDT/BRL), Tesouro Transparente (real interest rate), Cboe/FRED (VIX), Google Trends (searches) and DefiLlama (USDT supply). Addresses and coverage in the [manual](manual.md#data-sources).

## Documentation in English

| File | Content |
| --- | --- |
| [`manual.md`](manual.md) | Program manual |
| [`results.md`](results.md) | All tests and checks, in the order they were done |
| [`pre-registration.md`](pre-registration.md) | Hypotheses and rules for the validation with data from 02/11/2026 onwards |
| [`freeze.md`](freeze.md) | Version frozen for the validation: commit, hashes, dependencies and exposure to new data |
| [`../../LICENSE-DATA.md`](../../LICENSE-DATA.md) | Data licence |

Available only in Portuguese: the decision log (`docs/decisoes.md`), the automatic tables (`docs/resultados_tabelas.md`) and the audit reports (`auditorias/`).

## Licences

- **Code:** MIT (file `LICENSE`).
- **Derived data** in `dados/tratado/` (consolidated price series and premium series): [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/) (file `LICENSE-DATA.md`).
- Source data remain subject to the terms of each source.

## How to cite

REZENDE, Augusto. *agio-stablecoin*: code and data for the stablecoin premium in Brazilian reais. GitHub, 2026. Available at: https://github.com/augustojrezende/agio-stablecoin.
