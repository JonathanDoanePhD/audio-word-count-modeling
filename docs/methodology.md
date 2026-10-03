# Evaluation methodology and research audit

## Retrospective workflow

`scripts/evaluate.py` consumes the committed derived tables, validates required fields, checks transcript counts, rejects overlapping speaker IDs or duplicate audio filenames across partitions, fits the three-feature linear selector on training observations, and evaluates final word counts on validation and test.

Analyzer order follows the original grid construction: silence threshold -1 through -4, normalization level 13 through 16, and minimum silence length 13 through 16 in the inner loop. ID 0 maps to `count_13_n-1_13`; ID 63 maps to `count_16_n-4_16`. Predicted IDs are rounded using NumPy nearest-integer rounding (ties to even), then clipped to 0–63. This is an explicit retrospective decoding rule, not a recovered historical production rule.

The second fixed baseline is chosen by minimizing mean absolute relative error on training rows only. It selects `count_16_n-4_15`. The baseline choice and model are frozen before evaluation. The historical test set has already been examined in the original notebooks, so this review is not a newly blinded confirmatory experiment.

## Metrics

All method comparisons use the same reference: `num_words`.

- MAE: average absolute difference between estimated and reference word count.
- MSE: average squared difference in words squared; larger errors receive more weight.
- Mean relative error: average absolute difference divided by reference word count.
- Signed bias: average estimated minus reference count; positive means overcounting.
- Exact-match rate: fraction of clips with the correct integer count.

No conversion from MSE to an undefined “accuracy” score is made. Subgroup results report sample size and descriptive errors; they are not significance tests or evidence of a causal demographic effect.

## Issues found in original notebooks

| Original location | Finding | Treatment in this review |
| --- | --- | --- |
| `03_1_ValTest_of_ML_Models`, cells 9, 12, 14, 21, 22 | Selector MSE compares predicted IDs with `MEDIAN_func_num`; fixed-counter MSE compares count/reference ratios with those same IDs. These are different quantities. | Replace headline comparisons with final word-count metrics. Retain historical outputs in the archive. |
| `03_2_ValTest_of_MLR_Model`, cell 14 | `TR_df['pred_y'] = y` uses answer-derived training labels, not `model.predict`. The visualization therefore does not establish predicted-count performance. | Do not reuse the figure as performance evidence. |
| `03_1_ValTest_of_ML_Models`, cell 16 | Training dummy columns are assigned into validation frames by row index. | Exclude this logistic-regression output from comparative conclusions. |
| `01_2_Augment_DF_MESSY`, cell 13 | Dominant frequency uses `argmax` on complex FFT values and is assigned from filesystem iteration order. | Flag the derived feature and alignment as unverified until audio-level reconstruction. |
| `01_1_EDA_DongJoanne`, initial data loading | Validation frame is overwritten with test columns. | Preserve the notebook, use distinct committed tables in the supported workflow. |
| Original counting functions | +13 to +16 dBFS targets can clip PCM audio. | Preserve historical derived counts; do not present these settings as recommended audio processing. |
| Feature-selection notebooks | Many feature combinations are scored on training data; some use `median_func_num`, others `MEDIAN_func_num`. | Freeze the archived three-feature model for this review; distinguish targets and require grouped validation for future tuning. |
| Original notebooks | Windows-only paths, notebook imports, implicit variables, and unseeded random exploration. | Use a separate portable, deterministic table-evaluation script. Original notebooks are historical artifacts, not the supported runtime. |

## Scope of verification

The review reproduces the archived three-feature analyzer-ID MSE (validation 326.9903387; test 338.1291980) and training R² (0.1071412), then evaluates a correctly decoded selector on final counts. It verifies table-level completeness and split separation, and unit-tests metric definitions and analyzer-grid decoding.

It does not rerun feature extraction or silence segmentation on the original WAV files. Stored features and candidate counts inherit the historical pipeline's limitations. No bootstrap confidence intervals or inferential subgroup tests are supplied. Hashes in the audit describe the UTF-8 table copies used in this execution; check regenerated hashes in your own checkout, since line endings can differ.
