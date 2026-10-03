# Data dictionary and provenance

Source: Common Voice 2 subset from Kaggle; original subset notes in `commonvoice/README.txt` identify Mozilla release `en_1488h_2019-12-10`. Audio was converted from MP3 to WAV.

The supplied subset restricts observations to those with recorded age and gender, excludes the age category `teens`, and balances `male` and `female` categories within each partition. Training requires at least three up-votes; validation at least two. These selection rules limit representativeness.

| Field | Meaning and treatment |
| --- | --- |
| `client_id` | Source speaker identifier used to check partition separation. It is not a name. |
| `aud_path` | Historical audio path, often using Windows separators. Table evaluation does not open it. |
| `sentence` | Supplied transcript; whitespace tokens are the count reference. |
| `num_words` | Stored transcript token count, verified against `sentence`. |
| `up_votes`, `down_votes` | Source validation votes. |
| `age`, `age_num` | Recorded age band and numerical approximation; not exact age. |
| `gender` | Source-provided categorical field; original descriptions sometimes call this “sex.” Do not infer biological sex or comprehensive identity coverage. |
| `accent` | Recorded accent label; missing values retained as `Unknown` for descriptive reporting. |
| `num_onsets` | Archived detected acoustic onset count; not word count. |
| `onset_stren_mean` | Archived mean onset strength. |
| `dom_freq` | Archived frequency feature; extraction and row alignment require audio-level verification. |
| `count_<ms>_n-<threshold>_<target>` | Word estimate for one historical silence-based configuration. |
| `acc_ratio_count_*` | Estimated count divided by reference count. A ratio of 1 is exact, not “100% model accuracy” in a general sense. |
| `median_func_num` | Analyzer label derived within a fixed acceptance band; may be missing. |
| `MEDIAN_func_num` | Analyzer label using progressively relaxed acceptance bands. Regression target in the supported retrospective evaluation. |
| Numeric columns `0` through `63` | Intermediate grid bookkeeping; not predictive features. |

Only acoustic features are inputs to the supported selector. Transcript-derived counts and analyzer labels are evaluation references or supervised training targets, never predictor inputs.

The review's subgroup summaries retain the dataset's recorded categories. Neither balance in two categories nor descriptive differences demonstrate fairness or generalizability. This dataset does not represent early childhood conversational environments.
