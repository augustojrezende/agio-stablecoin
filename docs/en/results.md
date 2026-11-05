# Results: The stablecoin premium in reais: reaction to domestic and external shocks in Brazil (2020–2026)

*English translation of [`docs/resultados.md`](../resultados.md). The Portuguese original prevails. Figures (in `../figuras/`) and automatic tables (`../resultados_tabelas.md`) keep their Portuguese labels; see the glossary in the [manual](manual.md#glossary-of-portuguese-terms).*

*Complete record of the tests and checks of the discovery sample (13/10/2020 to 30/10/2026), in the order in which they were done. Table figures: `resultados_tabelas.md`, produced by `agio relatorio`. Decisions and reasons: `decisoes.md` (Portuguese). Out-of-sample validation: [pre-registration](pre-registration.md). Updated on 05/11/2026 with the corrections from audits AUD-001 to AUD-003 (section 11); the figures in this file are those of the corrected version.*

## Summary

| Question | Answer in the discovery sample | Status |
| --- | --- | --- |
| Does fiscal stress (10-year real interest rate) raise the premium? | No: small effect, only at 10% (p = 0.088), and fragile in robustness checks | Original hypothesis **not confirmed**; repeated in the validation (V1) |
| Do domestic announcements raise the premium more than external shocks? | Not in the full list (p = 0.77) | **Not confirmed** |
| Do crises raise market participation? | No more than on random days (p = 0.63) | Behavioural hypothesis **not confirmed**; repeated (V2) |
| Is global fear (VIX) associated with a higher premium? | Yes: positive in 7 of 9 specifications, but concentrated in 2020–2022 and sensitive to a few days | Exploratory; confirmation in the validation (V3) |
| Does the official exchange rate pass fully to USDT on the same day? | No: the USDT price follows about 86% of the PTAX change; the premium falls 0.13 p.p. per 1% rise | Exploratory; confirmation in the validation (V4a) |
| Does the premium bounce back on the following days? | No: it keeps falling for 2 more days (total of about −0.21 p.p. per 1%) | Contrary to V4b; new V6, negative persistence (addendum to the pre-registration); mechanism not identified |

**Provisional conclusion:** the USDT premium in reais did not behave as a thermometer of Brazilian fiscal stress as measured by the real interest rate, which does not prove that fiscal risk is irrelevant. The clearest associations are with the official exchange rate, which USDT follows only partly on the same day, and with global fear. These are observed associations, not causal relationships.

## 1. Data and coverage

- **Sources, all free:** PTAX selling rate (Central Bank of Brazil, Olinda); daily and hourly USDT/BRL candles (Binance since 13/10/2020, Mercado Bitcoin since 11/03/2023); 10-year real interest rate (Tesouro IPCA+, morning rate, interpolated); VIX (Cboe, because FRED was down).
- **Coverage:** 1,520 business days with a premium; 1,490 enter the regressions, because the abnormal premium needs at least 30 days of history.
- **Normal premium:** about 1% in 2020, falling to 0.2–0.3% in 2025–26 (Figure 1).

## 2. Check: the measurement time

**Problem found:** in the first collection, the lowest premiums in the series fell precisely on shock days: 09/04/2025 at −3.5%, 26/10/2026 at −2.1% and 06/11/2024 at −1.8%. The cause was timing. The PTAX is formed between 10:00 and 13:00, and the exchanges' daily candle closes at 21:00 (Brasília time).

**Correction:** the main measure now uses the volume-weighted USDT price between 10:00 and 13:00 Brasília time.

**Result of the check:**
- 09/04/2025 went from −3.5% to about 0%;
- the correlation between the two measures is 0.54 (Figure 2);
- the 2025 standard deviation fell from 0.53 to 0.19 p.p.

**Cost:** the correlation between exchanges fell from 0.91 to 0.68, because there are fewer trades in 3 hours (Figure 3). In practice, the consolidated indicator is Binance's, which concentrates the volume.

## 3. Descriptive analysis

- **Domestic shocks did not raise the premium.** Fiscal package (29/11/2024): −1.5 p.p. abnormal premium. Second round of the election (26/10/2026): −0.8 p.p.
- **The largest abnormal premium in the series was external.** On 05/08/2024 (global turmoil), +3.0 p.p. (Figure 4).
- **Participation soared in major shocks.** The number of trades doubled or tripled, and the average ticket fell.
- **Unexplained episode.** From 24/06 to mid-July 2026, the premium stayed between 1% and 1.7%. Diagnosis in section 3.1.

### 3.1 High-premium episode (24/06 to mid-July 2026)

*Diagnosis with `agio episodio --inicio 2026-06-01 --fim 2026-08-15`, comparing the period with the previous 90 days. Figure: `figuras/episodio_20260601_20260815.png`.*

| Check | Result | Reading |
| --- | --- | --- |
| Two exchanges? | Yes: correlation of 0.83 in the episode; mean of +0.50 p.p. on Binance and +0.35 p.p. on Mercado Bitcoin (before: 0.07 and 0.01) | Market phenomenon, not one exchange |
| Window and closing price? | Both rise together (closing: 0.17 → 0.67 p.p.) | Price level, not timing |
| Liquidity in the window | 3 hours with trades every day; volume 52% higher (17.1 → 26.1 million USDT) | Not a price from few trades |
| Which side did it come from? | The PTAX stayed at R$ 5.17–5.21 and USDT rose to R$ 5.28; then the PTAX fell and USDT followed slowly | USDT became expensive, and the gap took about 4 weeks to close |
| Who bought? | Average ticket 39% higher (R$ 6.5k → R$ 9.0k); same number of trades; lower buying pressure (0.55 → 0.51) | Larger trades, no buying rush; not a retail run |

- **Conclusion of the diagnosis:** the episode is real; it is not a measurement error.
- **The sign went against the mechanical effect.** On the first day (24/06), the dollar rose 0.69%, which by the mechanical effect would reduce the premium, and yet the premium jumped to 1.5%.
- **Pattern consistent with a lack of sellers**, more than with an excess of buyers: a high price without urgency to buy and slow convergence. In other words, arbitrage was slow for a few weeks.
- **Hypothesis tested (exploratory):** USDT scarcity. In June 2026 the global stablecoin supply had its largest monthly contraction since 2022, and USDT fell from about US$ 190 bn to US$ 184 bn.
- **Another possible factor:** risk aversion on 24/06 itself (gold −3.4%, Ibovespa −0.4%).
- **Ruled out by the news as the sole cause:** Resolution 574 (18/06), IOF on stablecoins (no decree), Resolution 561 (in force only from 01/10) and the exit of smaller exchanges. Details and sources in `decisoes.md`.
- **Exploratory test, outside the pre-registration (`agio oferta-usdt`):** the abnormal-premium regression gained one more variable, the 5-day change in the global USDT supply (DefiLlama), lagged by 1 day.

| Variable | Coefficient | p-value |
| --- | --- | --- |
| Change in USDT supply (5 days, %) | +0.031 | 0.051 |
| Change in the official dollar (%) | −0.128 | < 0.001 |
| Change in the 10-year real rate (bp) | +0.0018 | 0.118 |
| Change in the VIX on the day | +0.022 | 0.045 |
| Change in the VIX on the previous day | +0.016 | 0.008 |

  - **The scarcity hypothesis is not confirmed.** The sign is positive, the opposite of the prediction, and does not reach 5%.
  - **The monthly sequence confirms it:** supply fell from May to July (US$ 188.4 bn to 183.5 bn) and fell even more in October (180.1 bn), with no new jump in the premium.
  - **Reading of the positive sign:** supply seems to follow global demand. When demand rises, Tether issues more, and the premium rises with it.
  - **Side robustness gain:** with the extra variable, the VIX and the dollar do not change.
- **Conclusion on the episode:** it is a real market phenomenon, and its cause remains unidentified. Global scarcity was tested and ruled out. The most likely explanation is a local friction in arbitrage between the official FX market and the USDT market in Brazil, which the available data do not measure. It remains a question for graduate research (limits to arbitrage).

## 4. Design of the formal test (fixed before running)

- **Regression with all days.** Dependent variable: abnormal premium. Explanatory variables: change in the official dollar, in the 10-year real rate (in bp), in the VIX on the day and on the previous day, and market size. Estimated by OLS, with Newey-West errors.
- **Event study.** Window from −1 to +3 business days. t-test and permutation test against random dates. Comparison of domestic and external shocks.
- **Decision rule.**
  - The original hypothesis is confirmed if the real rate has a positive coefficient significant at 5% **and** domestic shocks have a larger premium than external ones.
  - The behavioural version is confirmed if participation is significantly higher in crises.

## 5. Regressions

**Abnormal premium** (1,490 days):

| Variable | Coefficient | p-value |
| --- | --- | --- |
| Change in the official dollar (%) | −0.129 | < 0.001 |
| Change in the 10-year real rate (bp) | +0.0019 | 0.088 |
| Change in the VIX on the day | +0.021 | 0.047 |
| Change in the VIX on the previous day | +0.016 | 0.008 |
| Market size (log) | +0.029 | 0.087 |

R² = 0.095; residual kurtosis = 15.3.

- **Real rate:** a strong fiscal shock of +20 bp moves the premium by about 0.04 p.p.
- **VIX:** a 10-point jump is associated with a premium about 0.2 p.p. higher on the day and 0.15 p.p. on the next day.
- **Participation:** the abnormal number of trades does not respond to the interest rate or the VIX. The average ticket falls when the dollar rises (p = 0.044).

### 5.1 Exchange-rate pass-through on the following days

The pass-through regression adds the change in the dollar 1, 2 and 3 days earlier:

| Variable | Coefficient | p-value |
| --- | --- | --- |
| Dollar on the day | −0.126 | < 0.001 |
| Dollar 1 day earlier | −0.057 | < 0.001 |
| Dollar 2 days earlier | −0.025 | 0.007 |
| Dollar 3 days earlier | +0.002 | 0.85 |
| Sum of the lags | −0.080 | < 0.001 |

- **The registered prediction (V4b) is not confirmed.** It said the premium would bounce back on the following days, because USDT would catch up with the dollar with a delay. The premium keeps falling for two more days, and the total effect reaches about −0.21 p.p. per 1% rise.
- **Possible readings, not tested.** One is profit-taking (USDT holders sell over a few days after the rise in the dollar). Others are sell orders that adjust slowly, delayed arbitrage, or the inventory of liquidity desks. Aggregate data do not distinguish between them.
- **Beware of the mechanical part.** Since premium = USDT price / PTAX − 1, if USDT reacts less than the PTAX, the premium falls by construction. With the same controls, the USDT return has a coefficient of 0.856 on the dollar (AUD-001): same-day pass-through is about 86%. Persistence in the lags is not an accounting identity, but it does not reveal the motive either.
- **How it stands in the pre-registration.** It entered as V6 in addendum 1, to be confirmed in the validation. V4b is still tested as written.

### 5.2 Check: extreme dollar days

The dollar chart (Figure 5) showed atypical daily changes. All were checked:

| Date | Dollar change | Gap since the previous day | What it was |
| --- | --- | --- | --- |
| 26/10/2026 | +8.8% | weekend | Day after the second round: dollar +8.21% and stock market −13.88% in the news |
| 05/10/2026 | −4.7% | weekend | Day after the first round of 2026 |
| 09/11/2020 | −4.6% | weekend | Outside the regression (no history yet for the abnormal premium) |
| 03/10/2022 | −3.9% | weekend | Day after the first round of 2022 |

- **These are real data, not gaps in the data.**
- **The largest domestic shock in the series** (26/10/2026) had a *negative* abnormal premium (−0.77 p.p.), consistent with the mechanical effect of the dollar and contrary to the fiscal hypothesis.
- **The results do not depend on these days:** the robust (Huber) and winsorised regressions keep the signs (section 6).

## 6. Robustness (Figure 8)

The test repeats the regression in 9 specifications: winsorised, Huber, closing-price premium, each exchange separately, before and after 04/05/2026, and a window up to 14:00.

- **Previous-day VIX:** significant in 7 of 9. The two exceptions have few data: Mercado Bitcoin, with 884 days, and the period after 04/05/2026, with 127 days.
- **Real rate:** never positive and significant at 5%. With the window up to 14:00, it falls to 0.0006 (p = 0.59). With the closing-price premium it comes out negative, which reflects the timing problem.
- **Dollar:** negative in all specifications; significant in all except after 04/05/2026 (p = 0.111, 127 days).
- **VIX sensitivity (AUD-001):** with HAC of 10 and 20 lags, p = 0.005 and 0.004. Without the 5 most influential days (the largest is 05/08/2024), the coefficient falls to 0.006 (p = 0.10); without 15, 0.008 (p = 0.02). By sub-period: 0.025 in 2020–2022 and 0.003 in 2025–2026. The association exists but is concentrated at the start of the sample.

## 7. Event list and event study (Figures 6 and 7)

**Problem:** the provisional list had 15 events, chosen one by one after looking at the data.

**Correction:** a fixed rule took over (`scripts/montar_eventos.py`), generating 158 events with sources:
- all Copom and Fed decisions;
- PLDO, PLOA (budget bills) and bimonthly fiscal reports;
- 5 fiscal announcements;
- elections;
- external shocks;
- Central Bank rules on crypto assets.

**Checks of the list:**
- **By the researcher:** 17 dates from Nov/2020 to Nov/2022 checked against the actual publication. All matched, except the time of a speech by Paulo Guedes, then Minister of Economy (20/10/2021, in the afternoon), which does not change the event date.
- **In the provisional list itself, two errors:**
  - the tariff pause was announced at 14:00 on 09/04/2025, so the event moves to 10/04;
  - the crypto reporting in the FX market scheduled for 04/05/2026 was postponed to 03/11/2026 by Resolution 574.

**Results:**

| List | Abnormal premium: all (perm. p) | Domestic − external (perm. p) | Trades: all (perm. p) |
| --- | --- | --- | --- |
| Full (154 events) | −0.175 (0.36) | +0.07 (0.77) | +0.43 (0.63) |
| Non-overlapping (60 events) | −0.300 (0.20) | +0.85 in the dollar-adjusted premium (0.031) | +0.59 (0.57) |

- **t-test versus permutation test.** The number of trades seems to rise around events by the t-test (p = 0.001), but it rises equally on random days, because the market grew over the period. The valid comparison is the permutation one.
- **Audit correction:** the overlap calendar lacked the All Souls' Day holiday. With the PTAX calendar, Copom 28/10/2021 and Fed 04/11/2021 become overlapping, and the isolated list falls from 62 to 60 events (32 domestic, 14 external, 14 monetary). The full list does not change.
- **Without overlapping events,** isolated external shocks are associated with a *lower* dollar-adjusted premium: −0.67 p.p. (p = 0.024, 14 events). This is where the difference between domestic and external comes from (+0.85, p = 0.031), since domestic events stay close to zero.
- **The difference does not survive time placebos.** Shuffling labels only within each year, p = 0.091 (adjusted) and 0.135 (abnormal); shifting the series within each year, p = 0.086 and 0.107. The p = 0.03 depends on comparing events from different years. Correct reading: a nominal difference, sensitive to the placebo design.
- **Beware of multiple testing.** There were about 40 tests, and at the 5% level about 2 significant results are expected by chance alone. The result for isolated external events is exploratory (V5 in the pre-registration) and does not survive the Holm correction (adjusted p = 0.072). V3 (0.031), V4a (< 0.001) and V6 (0.002) survive, which in the discovery sample is not a confirmation.
- **The origin label is not random.** 47 of the 53 external events are scheduled Fed decisions, and the domestic ones are almost all scheduled fiscal reports. The permutation compares groups; it does not measure a causal effect of the shock's origin.

### 7.1 Public attention (Google Trends), exploratory

*`agio buscas`: abnormal searches = log(1 + interest) minus the median of the previous 60 business days. Outside the pre-registration; discovery sample only. Figures 9a and 9b (`figuras/09_buscas_dolar.png`, `figuras/09_buscas_usdt.png`).*

| Event type | Searches for "dólar" (perm. p) | Searches for "USDT" (perm. p) |
| --- | --- | --- |
| External (53) | +0.38 (0.013) | +0.43 (0.62) |
| Political (4) | +3.01 (< 0.001) | +1.12 (0.64) |
| Fiscal (46) | +0.07 (0.92) | +0.32 (0.48) |
| Monetary (47) | +0.21 (0.26) | +0.32 (0.48) |
| All (154) | +0.30 (0.002) | +0.38 (0.29) |
| Unscheduled (13) | +1.12 (< 0.001) | +0.88 (0.78) |

- **Attention to the dollar reacts to external and political shocks, not fiscal ones.** In external shocks, searches jump on the event day and leave the band of random dates. In fiscal announcements, they stay within it.
- **Searches for USDT do not react to events.** Like the number of trades, they grow over time on any day.
- **Searches do not anticipate the premium.** In the regression with the previous day's searches: USDT +0.067 (p = 0.13) and dollar −0.061 (p = 0.21). Dollar and VIX do not change.
- **Reading:** the public pays attention to the dollar in elections and external shocks, but fiscal announcements do not even draw attention; and high attention does not turn into demand for the digital dollar or a premium.
- **Caveats:** the political group has 4 events (strong effect, few cases); there are about 12 more tests, so the analysis illustrates rather than confirms.

## 8. Application of the decision rule

| Hypothesis | Condition | Result |
| --- | --- | --- |
| Original | Real rate > 0, p < 5% | No (p = 0.088) |
| | and domestic > external | Not in the full list (p = 0.77); the rule uses the full list |
| Behavioural | Participation in crises > random days | No (p = 0.63) |

Neither thesis hypothesis is confirmed in the discovery sample.

## 9. Limitations

- **Aggregate data:** they measure collective behaviour, not each investor's motivation.
- **Weight of Binance:** in practice, the indicator is that of one exchange.
- **Fiscal stress proxy:** the 10-year real rate is an indirect measure; CDS was left out because of cost.
- **VIX timing:** the VIX closes after the PTAX window. The cleanest result is therefore the previous day's.
- **Little time since the regulation:** 127 days, without statistical power.
- **Pass-through and identity:** the PTAX is in the denominator of the premium; part of the relationship with the dollar is mechanical (section 5.1).
- **Event study:** the permutation does not reproduce a random assignment of the shocks' origin, and the contrast of isolated events depends on the placebo (section 7).
- **Multiple testing:** see section 7.
- **June–July 2026 episode:** cause not identified; global USDT scarcity was tested and not confirmed.

## 10. Next steps

1. **Out-of-sample validation** ([pre-registration](pre-registration.md), addendum 2): descriptive reading with data until 29/10/2027 and a single decision with data until 31/10/2028.
2. **June–July 2026 episode:** market phenomenon confirmed; global USDT scarcity ruled out (section 3.1). The cause remains open for graduate research.
3. **Bridge to graduate research:** incomplete exchange-rate pass-through and global fear, if confirmed in the validation.

## Record of errors found and corrected

| Date | Error | Correction |
| --- | --- | --- |
| 31/10/2026 | Closing-price premium distorted on shock days (timing) | Measure aligned with the PTAX window |
| 31/10/2026 | FRED down when collecting the VIX | Cboe alternative; shorter collection |
| 01/11/2026 | Event list chosen by hand, after looking at the data | Fixed rule, generated by script |
| 01/11/2026 | Tariff pause dated on the announcement day (14:00, after the window) | 10/04/2025 |
| 01/11/2026 | 04/05/2026 treated as the effective start of the reporting obligation | Recorded as the scheduled start; the postponement (Res. 574) enters as an event |
| 01/11/2026 | A 10-day placebo exclusion would exhaust the draws with 158 events | 4 business days (windows do not overlap) |
| 02/11/2026 | `agio robustez` failed with duplicate indices when joining batches (AUD-001-06) | New index and duplicate removal; 9 specifications unchanged |
| 02/11/2026 | Overlap calendar without holidays (AUD-001-10) | PTAX calendar; 62 → 60 isolated events |
| 02/11/2026 | V1 without a minimum number of events (AUD-001-21) | Minimum of 10 per group, otherwise inconclusive |
| 02/11/2026 | Holm family shrank without V5 (AUD-001-22) | Always seven positions |
| 02/11/2026 | Figure 1 median included the day itself (AUD-001-26) | Same median as the indicator |
| 02/11/2026 | Trajectories showed nominal n (AUD-001-27) | Valid n per day |
| 02/11/2026 | Episode volume labelled in reais (AUD-001-31) | USDT |

## 11. Independent audit (AUD-001 to AUD-003)

Three audits reviewed the project on 02/11/2026: diagnosis (AUD-001), correction in a separate copy (AUD-002) and final opinion (AUD-003). The reports, in Portuguese, are in `auditorias/`.

- **Seven proven errors, all corrected** (table above). None changed the main regression, the robustness checks or the decision on any hypothesis.
- **Reproduction:** with the corrected code, `agio testar` and `agio robustez` reproduce from scratch all results of the audited copy; 64 automated tests.
- **Opinion:** approved with reservations, as an observational and exploratory study. The reservations are in sections 5.1, 6, 7 and 9.
- **What changed in the figures:** the isolated list (section 7) and the V6 label, which now describes the pattern ("premium keeps falling after a rise in the dollar") instead of a mechanism.

## Figures

Produced by `agio relatorio` in `docs/figuras/` (Portuguese labels); full captions in `resultados_tabelas.md`.

1. Premium series (PTAX window, closing price and rolling median)
2. PTAX window versus closing price
3. Premium by exchange
4. Abnormal premium and unscheduled shocks
5. Official dollar and abnormal premium (incomplete pass-through)
6. Trajectory of the dollar-adjusted premium around events, against random dates
7. Trajectory of the number of trades around events
8. Robustness: coefficients and 95% intervals
