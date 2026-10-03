# Research brief

## Why this question matters

Measurement helps educators and families see patterns that may otherwise remain invisible. LENA's work inspired the team's interest in estimating spoken-word counts. Our narrower question was whether acoustic features could guide the selection of a simple counter for each recording.

The intended analytic contribution was an interpretable comparison of fixed and adaptive measurement approaches. This study was not a validation of LENA's technology or its program impact.

## Study design

The archived Common Voice subset contains 2,800 English clips across training (2,000), validation (400), and test (400) tables. The retrospective audit found 595, 167, and 244 distinct speaker IDs respectively, with no shared IDs between partitions. All reference word counts match whitespace-separated transcript token counts. This does not establish that every recording perfectly matches its supplied transcript.

The counter varies minimum silence length (13–16 milliseconds), silence threshold (-1 to -4 dBFS), and normalization target (+13 to +16 dBFS). Those positive normalization targets are preserved as historical settings; they can introduce clipping and require redesign before further audio experiments.

The selector uses three acoustic inputs and predicts `MEDIAN_func_num`, an analyzer label generated using the known transcript count. Label generation is appropriate for supervised training, but those answer-derived labels cannot be used in place of predictions during evaluation.

## What the corrected evaluation shows

On validation, the acoustic selector's MAE is 4.280 words compared with 4.580 for the original fixed counter. On test, that relationship reverses: 4.910 compared with 4.675. The fixed counter chosen using training relative error achieves a test MAE of 4.395 words, but its test MSE is slightly higher than the original counter's.

These results support a modest conclusion: acoustic information has some relationship with analyzer choice, but the particular regression selector does not demonstrate better test word-count accuracy. Different loss functions also favor different fixed configurations.

## Practical implications

For a partner-facing report, the useful message is that a promising development result needs confirmation on held-out observations using the metric tied to the actual task. A clear explanation of error magnitude and direction is more useful than an ambiguous claim of “accuracy.”

Data preparation also matters. Missing accent values affect 505 training, 144 validation, and 117 test clips. The supplied subset restricts age and recorded gender categories, so it is not representative of all speakers. Subgroup error tables are descriptive; small groups and repeated recordings per speaker limit comparisons.

## Next experiments

1. Rebuild features from audio, matching by clip filename rather than directory enumeration. Verify spectral peak extraction uses magnitude rather than the complex FFT values.
2. Normalize to a physically feasible level with explicit clipping checks; compare segmentation parameters in interpretable units.
3. Compare direct word-count regression with models of each analyzer's expected error, avoiding a numerical ordering assumption for analyzer IDs.
4. Use speaker-grouped resampling within development data and report uncertainty at the speaker level. Treat the historical test set as already examined; use new held-out data for future model selection.
5. Only after establishing a read-speech result, evaluate realistic noise, overlap, languages, and caregiver-child settings with appropriate consent and reference annotation.
