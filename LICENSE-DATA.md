# Data licence

*English translation of [`LICENSE-DADOS.md`](LICENSE-DADOS.md). The Portuguese original prevails.*

The derived data in `dados/tratado/` (consolidated USDT/BRL price series and series of the premium over the PTAX), when distributed, are licensed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)** licence.

You may copy, redistribute and adapt the data **for non-commercial purposes**, provided that you:

- **give credit:**

  > Rezende, Augusto. *O ágio da stablecoin em reais: reação a choques domésticos e externos no Brasil (2020–2026)* [The stablecoin premium in reais: reaction to domestic and external shocks in Brazil (2020–2026)]. https://github.com/augustojrezende/agio-stablecoin

- **distribute adaptations under the same licence.**

Full licence text: https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.en

**Why non-commercial.** The series are computed from public Binance prices. The Binance Vision terms of use ask that data derived from their datasets be redistributed with attribution under CC BY-NC-SA 4.0. The project uses the public market-data API (`data-api.binance.vision`); as a precaution, it follows the same licence. Until 10/11/2026 the data were under CC BY 4.0 (recorded in `docs/decisoes.md`).

The source data (PTAX and Selic from the Central Bank of Brazil; prices from the Binance and Mercado Bitcoin exchanges) remain subject to each source's terms of use. The files in `dados/bruto/` reproduce the responses of these sources and are not covered by this licence.

The project's source code is licensed separately under the MIT licence (file `LICENSE`).
