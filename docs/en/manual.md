# agio-stablecoin user manual

*English translation of [`docs/manual.md`](../manual.md), version of 01/11/2026 · Augusto Rezende. The Portuguese original is the authoritative version; if the two differ, the Portuguese text prevails.*

*Commands, parameters, file names and column names are part of the code and stay in Portuguese. A short glossary is at the end.*

## Contents

1. [Overview](#overview)
2. [What is a stablecoin](#what-is-a-stablecoin)
3. [What is the premium (ágio)](#what-is-the-premium-ágio)
4. [How it works](#how-it-works)
5. [Technologies](#technologies)
6. [Data sources](#data-sources)
7. [Installation](#installation)
8. [Commands and parameters](#commands-and-parameters)
9. [Typical use](#typical-use)
10. [Output files](#output-files)
11. [Methods](#methods)
12. [Quality, reproducibility and licences](#quality-reproducibility-and-licences)
13. [Limitations and next steps](#limitations-and-next-steps)
14. [How to cite](#how-to-cite)
15. [Glossary of Portuguese terms](#glossary-of-portuguese-terms)

## Overview

**agio-stablecoin** is a command-line Python program that builds a daily indicator of the premium (*ágio*) of the digital dollar (USDT) traded in Brazilian reais over the official dollar rate (PTAX), and tests how this premium reacts to domestic and external shocks. It is the empirical basis of the undergraduate thesis "The stablecoin premium in reais: reaction to domestic and external shocks in Brazil (2020–2026)".

**What it does:**

- Collects, from free public sources, USDT/BRL prices, the PTAX, the 10-year real interest rate, the VIX, Google searches and the global supply of USDT.
- Computes the daily premium in the same time window as the PTAX (10:00 to 13:00 Brasília time), per exchange and consolidated.
- Runs the thesis tests: regressions, event study with permutation tests, robustness in 9 specifications and the table of pre-registered hypotheses.
- Produces the figures and tables of the thesis.

**What it is for:**

- Measuring, with daily data since October 2020, a new channel of demand for dollars that official statistics capture poorly.
- Allowing any researcher to reproduce all thesis results with a few commands and to extend the series with new data.
- Serving as a basis for papers and for graduate research (out-of-sample validation until 2028).

**In numbers:** 1,520 business days analysed (13/10/2020 to 30/10/2026), 7 data sources, 12 commands, 158 events with sources, 64 automated tests.

## What is a stablecoin

A **stablecoin** is a crypto asset designed to be worth the same as a traditional currency, almost always US$ 1. It works as a "digital dollar": it circulates on blockchain networks, can be sent at any time to any country, and is traded on crypto exchanges.

**How it keeps its value:** the issuer holds reserves (bank deposits and US Treasury bills) and promises to exchange each unit for US$ 1. If the price falls below US$ 1, it pays to buy and redeem; if it rises above, it pays to issue and sell. This arbitrage keeps the price close to US$ 1.

**USDT:** the stablecoin used in this program is USDT, issued by Tether. It is the largest in the world (about US$ 180 billion in circulation in October 2026, according to DefiLlama) and accounts for almost 90% of the stablecoin operations declared to Brazil's Federal Revenue Service.

| | Dollar in the official FX market | USDT (digital dollar) |
| --- | --- | --- |
| Where to buy | Banks and FX brokers | Crypto exchanges (Binance, Mercado Bitcoin) |
| Trading hours | Business days, business hours | 24 hours, every day |
| Payment | FX contract, IOF tax | Pix (instant payment) in reais |
| Reference price | PTAX, computed by the Central Bank of Brazil | Set by supply and demand on each exchange |
| Who guarantees it | Regulated banking system | The issuer and its reserves |

**Why Brazilians use it:** to protect savings from the depreciation of the real, to make international payments and transfers, and to trade other crypto assets.

**Risks:** it depends on trust in the issuer's reserves; it can lose its peg in crises; and regulation is still being built. In Brazil, the Central Bank began regulating virtual asset service providers with Resolutions 519, 520 and 521 (November 2025) and treating part of stablecoin operations as FX operations.

**Why it matters for the program:** since USDT trades in reais on Brazilian exchanges, its price reveals how much people are willing to pay for dollars outside the official FX market. The difference between this price and the official dollar is the premium, explained next.

## What is the premium (ágio)

The **premium** (*ágio*) is how much an asset trades **above** its reference price, in percent. When the price is **below** the reference, it is a **discount** (*deságio*, a negative premium).

In this program, the asset is USDT (a digital dollar that promises to be always worth US$ 1) and the reference is the Central Bank's official dollar rate (PTAX). In theory, both should cost the same in reais; the difference is the premium.

```math
\text{premium} = \frac{\text{USDT price in reais}}{\text{PTAX}} - 1
```

| Situation | PTAX | USDT on exchanges | Premium | Reading |
| --- | --- | --- | --- | --- |
| Positive premium | R$ 5.00 | R$ 5.05 | +1.0% | Buyers of digital dollars pay 1% more than the official rate |
| No premium | R$ 5.00 | R$ 5.00 | 0% | The two markets are aligned |
| Discount | R$ 5.00 | R$ 4.98 | −0.4% | The digital dollar is cheaper than the official one |

**An analogy:** the same concert ticket sold at the official box office and by resellers. If many people want tickets and the box office cannot serve everyone, resellers charge more; that difference is the premium. If there are tickets left over, resellers must sell below the official price: a discount.

**Why the premium exists if it is "the same dollar":** moving money from one market to the other has costs, delays and rules (FX contracts, taxes, limits). While this friction exists, the two prices can differ. When many people seek digital dollars at the same time, the premium tends to rise; when many sell, it tends to fall.

**Why it is interesting:** the premium works as a thermometer of the demand for dollars outside the official FX system. The program measures it every day and tests which kinds of news it reacts to.

**Abnormal premium:** the "normal" premium changes over time (about 1% in 2020 and 0.2% in 2026). The analyses therefore use the day's premium minus the typical premium of the previous 12 weeks: how far that day departed from the usual.

## How it works

The program works in four stages, always in the same order. Each stage reads what the previous one wrote to disk, so any stage can be redone without repeating the others.

1. **Collection (raw layer):** downloads data from the APIs and saves the responses exactly as received, in `dados/bruto/`, with the collection time. Nothing in this folder is edited.
2. **Processing (clean layer):** converts each source into a standardised CSV table (`dados/tratado/`). If the same day is collected again, the most recent collection prevails.
3. **Computation:** builds the premium per exchange and consolidated, the behavioural signals and the daily panel.
4. **Analysis and report:** runs the statistical tests, saves the results in `dados/resultados/` and produces figures and tables in `docs/`.

### Modules

| Module | Function |
| --- | --- |
| `cli.py` | Command line: receives commands and parameters and calls the other modules |
| `fontes/` | One module per source (`bcb`, `binance`, `mercadobitcoin`, `tesouro`, `fred`, `google_trends`, `defillama`), each with `baixar()` (download) and `tratar()` (process) |
| `http.py` | API access with automatic retries and pauses |
| `armazenamento.py` | Writes and reads the raw and clean layers |
| `janela.py` | USDT price in the PTAX window (10:00–13:00 Brasília time) |
| `indicador.py` | Premium computation and volume-weighted consolidation |
| `comportamento.py` | Collective behaviour signals and daily panel |
| `analise.py` | Regressions, event study, permutation, robustness and hypothesis table |
| `relatorio.py` | Thesis figures and tables |
| `episodio.py` | Diagnosis of periods with an unusual premium |
| `scripts/montar_eventos.py` | Builds the list of 158 events from a fixed rule |
| `scripts/coleta_semanal.sh` | Automatic weekly collection (scheduled on macOS) |

## Technologies

Language: **Python 3.10 or later** (tested on 3.13 and 3.14), with no server or database: everything runs on the researcher's computer and writes CSV and JSON files.

| Library | Minimum version | Use in the program |
| --- | --- | --- |
| pandas | 2.1 | Tables, dates, merging sources, rolling medians |
| statsmodels | 0.14 | OLS regressions with Newey-West errors and Huber robust regression |
| SciPy | 1.11 | t-tests and statistical functions |
| NumPy | (installed with pandas) | Permutation draws and vectorised computations |
| Matplotlib | 3.8 | Figures |
| Requests | 2.31 | Access to public APIs |
| pytest | 8 (development only) | Automated tests |

**Other tools:** Git and GitHub (versioning and publication), setuptools (installation as a package, with the `agio` command), macOS launchd (scheduling of the weekly collection).

**Cost:** zero. No source requires an access key or subscription.

## Data sources

| Source | Data | Access | Coverage |
| --- | --- | --- | --- |
| Central Bank of Brazil (Olinda and SGS) | PTAX selling rate (closing) and daily Selic | Public API | Whole period |
| Binance | Daily and hourly USDT/BRL candles, number of trades and taker buy volume | `data-api.binance.vision` | Since 13/10/2020 |
| Mercado Bitcoin | Daily and hourly USDT/BRL candles | Public API v4 | Since 11/03/2023 |
| Tesouro Transparente (National Treasury) | Purchase rates of Tesouro IPCA+ bonds (10-year real rate) | Public CSV, about 14 MB | Whole period |
| Cboe (FRED as alternative) | VIX, daily close | Public CSV | Whole period |
| Google Trends | Search interest for "dólar" and "USDT" in Brazil | CSV exported by hand | Daily, 11 chained windows |
| DefiLlama | Global USDT supply in circulation | Public API | Since 2017 (exploratory use) |

The program handles the format differences of each source (for example, "<1" in Google Trends, "." as a missing value in FRED, different date formats) inside each module's `tratar()`. If a source changes its format, only that part needs adjusting.

**Google Trends, step by step.** There is no stable official API, so the import is by CSV: on trends.google.com, choose Brazil, the terms and windows of up to 8 months (longer windows become weekly data), overlapping by at least 30 days; export "Interest over time" to `dados/manual/google_trends/`, one file per window; run `agio importar-trends` and `agio calcular`.

## Installation

Requirements: Python 3.10 or later and Git. Works on macOS, Linux and Windows.

```bash
git clone https://github.com/augustojrezende/agio-stablecoin.git
cd agio-stablecoin
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest                             # 64 tests, no network access
```

After that, the `agio` command is available in the terminal while the virtual environment (`.venv`) is active. All dates use the `YYYY-MM-DD` format.

## Commands and parameters

General form: `agio <command> [parameters]`. `agio <command> --help` shows the parameters of each command.

### Collection

| Command | What it does | Parameters |
| --- | --- | --- |
| `coletar` | Downloads the PTAX, the Selic and the daily USDT/BRL candles from the exchanges | `--inicio` (required): first day; `--fim` (optional): last day, default = today |
| `coletar-horario` | Downloads the hourly candles and computes the price in the PTAX window | `--inicio` (required); `--fim` (optional, default = today) |
| `coletar-controles` | Downloads the history of the 10-year real rate (Treasury) and the VIX (FRED or, if it fails, Cboe) | `--so-vix`: VIX only; `--so-juro`: real rate only (cannot be combined; with neither, downloads both) |
| `importar-trends` | Reads the Google Trends CSVs in `dados/manual/google_trends/` and chains the windows into a single series | None |

### Computation

| Command | What it does | Parameters |
| --- | --- | --- |
| `calcular` | Computes the premium (PTAX window and closing price), the behavioural signals and the daily panel | None |
| `grafico` | Quick chart of the premium per exchange (`dados/grafico_agio.png`) | None |

### Analysis

| Command | What it does | Parameters |
| --- | --- | --- |
| `testar` | Formal test: regressions (premium, trades, average ticket and pass-through), event study (full list and non-overlapping list) and table of hypotheses V1 to V6 with Holm correction | `--inicio` (optional): only days from this date; `--fim` (optional): only days before this date. Without them, uses the whole period. With them, it is the out-of-sample validation (results in their own folder) |
| `robustez` | Repeats the premium regression in 9 alternative specifications | None |
| `buscas` | Exploratory: Google searches around events and as a predictor of the premium | None (requires `importar-trends` and `calcular` first) |
| `oferta-usdt` | Exploratory: global USDT supply as a variable in the premium regression | `--sem-coleta`: uses the supply already downloaded, without accessing DefiLlama |
| `episodio` | Diagnosis of a period with an unusual premium, against the previous 90 days | `--inicio` and `--fim` (both required): start and end of the period |

### Report

| Command | What it does | Parameters |
| --- | --- | --- |
| `relatorio` | Produces the figures (`docs/figuras/`) and the tables (`docs/resultados_tabelas.md`) from the results | None (requires `testar` and `robustez` first) |

### Helper scripts

| Script | What it does |
| --- | --- |
| `python scripts/montar_eventos.py` | Builds `dados/manual/eventos.csv` (158 events) from the rule recorded in the decision log; overlaps use the calendar of days with a PTAX |
| `./scripts/coleta_semanal.sh` | Collects the last 10 days, recomputes the premium and writes a log to `dados/logs/` |
| `./scripts/agendar_coleta_mac.sh` | Schedules the weekly collection on macOS (Monday, 20:00) |

### Constants in the code

These are not command-line parameters; they were fixed before the tests and are recorded in the decision log.

| Constant | Value | Where |
| --- | --- | --- |
| PTAX window | 10:00 to 13:00 Brasília time | `janela.py` |
| Window of the "normal" level for the abnormal premium | 60 business days (minimum of 30) | `analise.py` |
| Event study window | −1 to +3 business days | `analise.py` |
| Placebo exclusion | 4 business days around each event | `analise.py` |
| Newey-West lags | 5 | `analise.py` |
| Permutation draws | 5,000, seed 42 | `analise.py` |

## Typical use

### Reproducing the thesis results from scratch

```bash
agio coletar --inicio 2020-10-01            # daily prices, PTAX and Selic (a few minutes)
agio coletar-horario --inicio 2020-10-01    # hourly prices for the PTAX window
agio coletar-controles                      # real rate and VIX
agio importar-trends                        # optional: Google searches (CSVs in dados/manual/google_trends)
agio calcular                               # premium, signals and daily panel
agio testar                                 # formal test
agio robustez                               # 9 specifications
agio relatorio                              # figures and tables
```

To reproduce only the thesis sample (until 30/10/2026), use `--fim 2026-10-31` in the collection commands.

### Keeping the series up to date

```bash
./scripts/coleta_semanal.sh       # manual test
./scripts/agendar_coleta_mac.sh   # schedules every Monday at 20:00 (macOS)
```

Collection is idempotent: running the same period again only replaces it with the most recent data. Exchange APIs do not always keep long histories, so collection must continue regularly.

### Out-of-sample validation (pre-registration)

```bash
agio testar --inicio 2026-11-02 --fim 2027-10-30   # descriptive reading (data until 29/10/2027)
agio testar --inicio 2026-11-02 --fim 2028-11-01   # decision (data until 31/10/2028, α = 5%)
```

`--fim` is exclusive: only days before the date are included. In the 2027 reading the program still prints the `confirma` columns, but under addendum 2 of the pre-registration they are not a decision. Before each analysis, the event list for the period is built and versioned (`python scripts/montar_eventos.py`, with the calendar taken from the PTAX dates), without running any test.

### Investigating a specific period

```bash
agio episodio --inicio 2026-06-01 --fim 2026-08-15
```

## Output files

| Folder | Main files | Content |
| --- | --- | --- |
| `dados/bruto/` | One JSON or CSV per collection, with date and time in the name | API responses as received (do not edit) |
| `dados/tratado/` | `ptax.csv`, `precos_usdt_brl.csv`, `precos_janela_ptax.csv`, `juro_real_10a.csv`, `vix.csv`, `google_trends.csv`, `usdt_oferta.csv` | Standardised sources, one row per day (and per exchange) |
| `dados/tratado/` | `agio_diario.csv`, `agio_por_fonte.csv`, `agio_fechamento_diario.csv` | The indicator: main measure (PTAX window) and comparison (closing price) |
| `dados/tratado/` | `sinais_comportamento.csv`, `painel_diario.csv` | Trades, buying pressure, average ticket, searches and premium in a single panel |
| `dados/manual/` | `eventos.csv`, `google_trends/*.csv` | Event list (built by script) and Google Trends exports |
| `dados/resultados/` | `relatorio.txt`, `regressao_*.csv`, `eventos_*.csv`, `hipoteses.csv`, `robustez.csv`, `base_teste.csv` | Results of each test |
| `dados/resultados/` | `exploratorio_*.csv` and `.txt`, `episodio_*.csv` | Exploratory analyses and diagnoses |
| `docs/figuras/` | `01_serie_agio.png` to `09_buscas_*.png` | Thesis figures (labels in Portuguese) |
| `docs/` | `resultados.md`, `resultados_tabelas.md`, `decisoes.md`, `pre-registro.md` | Narrative report, automatic tables, decision log and pre-registration |
| `dados/logs/` | `coleta_*.log` | Log of each weekly collection |

## Methods

### Premium in the PTAX window

For each day and exchange, the price is the volume-weighted average of the typical prices of the hourly candles between 10:00 and 13:00 Brasília time; the typical price of each hour is (high + low + close) / 3.

```math
A_{i,t} = \frac{P^{USDT}_{i,t}}{PTAX_t} - 1, \qquad A_t = \frac{\sum_i V_{i,t} A_{i,t}}{\sum_i V_{i,t}}
```

where *i* is the exchange, *t* the business day and *V* the volume traded in the window.

### Abnormal premium

```math
AA_t = A_t - {median}(A_{t-60}, \dots, A_{t-1})
```

The median uses only previous days (minimum of 30). The same transformation is applied to the log of the number of trades, the average ticket and the searches.

### Main regression

```math
AA_t = \alpha + \beta_1 \Delta d_t + \beta_2 \Delta j_t + \beta_3 \Delta VIX_t + \beta_4 \Delta VIX_{t-1} + \beta_5 \ln M_t + \varepsilon_t
```

where Δd is the daily change in the PTAX (100 × log difference), Δj the change in the 10-year real rate in basis points, and M the median volume of the previous 60 days. Estimated by OLS with Newey-West errors (5 lags).

### 10-year real interest rate

For each day, the morning purchase rates of the Tesouro IPCA+ bonds (zero coupon) are linearly interpolated at the 10-year maturity.

### Event study

- **Cumulative effect (CAR):** sum of the abnormal premium from −1 to +3 business days around each event.
- **Permutation test:** 5,000 draws of dates without events (outside 4 business days of any event), of the same size as the group; the p-value is the share of draws whose mean is as far from the placebo mean as the events' mean.
- **Domestic × external:** permutation of the labels between the two groups.

### Robustness and multiple testing

- Winsorisation at the 1st and 99th percentiles; Huber robust regression (statsmodels HuberT norm).
- Holm correction over the 7 hypotheses of the pre-registration.

### Google Trends

Each exported window is normalised from 0 to 100. Overlapping windows are rescaled by the ratio of the means on common days with searches on both sides, forming a single daily series per term.

## Quality, reproducibility and licences

- **Automated tests:** 64 tests (pytest) that run without network access, with synthetic data of known effect (two of them, which check the event list and the hourly batches against the real data, only run after collection). They cover reading each source, computing the premium and the window, recovering known effects in the regression and the event study, and the commands end to end.
- **Immutable raw data:** every transformation comes from code; nothing is edited by hand.
- **Rule-based event list:** built by script, with the source of each event; 17 dates checked by the researcher.
- **Decision log** (`docs/decisoes.md`, in Portuguese): every methodological choice with date, reason, and errors found and corrected.
- **Pre-registration** (`docs/pre-registro.md`; [English translation](pre-registration.md)): hypotheses and rules fixed before the validation data, with dated addenda.
- **Explicit separation** between confirmatory and exploratory analyses in the program output.
- **Independent audits** (`auditorias/`, in Portuguese): diagnosis, correction and final opinion in Nov/2026; seven errors corrected, none changed the decision on any hypothesis.
- **Full history in Git:** every change went in through a pull request with a description. The original discovery version is under the tag `descoberta-v1`, and the version frozen for validation under `congelamento-v2`.
- **Licences:** code under MIT; derived data (premium series) under Creative Commons Attribution 4.0 (CC BY 4.0). Source data remain subject to the terms of each source.

## Limitations and next steps

**Limitations:**

- Two exchanges, with Binance concentrating the volume; in practice, the indicator is Binance's.
- Aggregate data: they measure collective behaviour, not individual motivations.
- The real interest rate is an indirect measure of fiscal stress (CDS was left out because of cost).
- Google Trends requires manual export, and Google resamples the data on each query.
- Collection depends on public APIs that may change format or limit history.

**Next steps:**

- Out-of-sample validation: descriptive reading in Oct/2027 and decision in Oct/2028.
- New exchanges and other stablecoins (for example, USDC).
- Moving storage to Parquet or DuckDB when the dataset grows.
- On-chain data (blockchain flows), in graduate research.

## How to cite

REZENDE, Augusto. *agio-stablecoin*: code and data for the stablecoin premium in Brazilian reais. GitHub, 2026. Available at: https://github.com/augustojrezende/agio-stablecoin.

Associated work: REZENDE, Augusto. *O ágio da stablecoin em reais*: reação a choques domésticos e externos no Brasil (2020–2026) [The stablecoin premium in reais: reaction to domestic and external shocks in Brazil (2020–2026)]. Undergraduate thesis (Economics). In preparation.

## Glossary of Portuguese terms

| Portuguese | English |
| --- | --- |
| ágio / deságio | premium / discount |
| ágio anormal | abnormal premium |
| PTAX | Central Bank of Brazil reference USD/BRL rate, fixed from four quotes between 10:00 and 13:00 Brasília time |
| janela da PTAX | PTAX window (10:00–13:00 Brasília time) |
| fechamento | closing price (daily candle close, 21:00 Brasília = 00:00 UTC) |
| corretora | exchange |
| juro real | real interest rate |
| negócios / ticket médio | number of trades / average trade size |
| evento, sobreposto | event, overlapping (event windows that share days) |
| doméstico / externo / monetário / fiscal / político / regulatório | domestic / external / monetary / fiscal / political / regulatory |
| confirma / confirma_holm | confirmed (raw p-value) / confirmed (Holm-adjusted p-value) |
| coletar, calcular, testar, robustez, relatório | collect, compute, test, robustness, report |
| dados/bruto, tratado, resultados | data/raw, processed, results |
