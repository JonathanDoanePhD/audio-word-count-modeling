"""Audit archived feature tables and evaluate final word counts, without audio decoding."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

FEATURES = ['num_onsets', 'onset_stren_mean', 'dom_freq']
COUNTERS = [f'count_{ms}_n-{threshold}_{level}'
            for threshold in range(1, 5) for level in range(13, 17)
            for ms in range(13, 17)]


def select_counts(frame, predicted_ids):
    """Round to nearest ID (NumPy ties-to-even), bound to grid, then look up count."""
    ids = np.clip(np.rint(predicted_ids).astype(int), 0, len(COUNTERS) - 1)
    return frame[COUNTERS].to_numpy()[np.arange(len(frame)), ids]


def metrics(reference, predicted):
    reference = np.asarray(reference, dtype=float)
    predicted = np.asarray(predicted, dtype=float)
    if reference.shape != predicted.shape or reference.size == 0:
        raise ValueError('Reference and predictions must have equal, nonempty shapes')
    if not np.isfinite(reference).all() or not np.isfinite(predicted).all() or (reference <= 0).any():
        raise ValueError('Finite counts and positive reference counts are required')
    error = predicted - reference
    return dict(mae_words=float(np.abs(error).mean()), mse_words_squared=float((error ** 2).mean()),
                mean_relative_error=float((np.abs(error) / reference).mean()),
                signed_bias_words=float(error.mean()), exact_match_rate=float((error == 0).mean()))


def run(data_dir, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    tables, audit = {}, {'files': {}, 'speaker_overlap': {}}
    for split, prefix in [('train', 'TR'), ('validation', 'VA'), ('test', 'TE')]:
        path = data_dir / f'{prefix}_MED_df.tsv'
        frame = pd.read_csv(path, sep='\t')
        required = FEATURES + COUNTERS + ['num_words', 'MEDIAN_func_num', 'client_id', 'aud_path', 'sentence']
        missing = set(required) - set(frame.columns)
        if missing:
            raise ValueError(f'{split}: missing columns {sorted(missing)}')
        if frame[FEATURES + COUNTERS + ['num_words', 'MEDIAN_func_num']].isna().any().any():
            raise ValueError(f'{split}: missing model inputs or count data')
        if not np.isfinite(frame[FEATURES + COUNTERS + ['num_words', 'MEDIAN_func_num']].to_numpy()).all():
            raise ValueError(f'{split}: nonfinite numeric values')
        if (frame.num_words <= 0).any() or frame.aud_path.duplicated().any() or frame.client_id.isna().any():
            raise ValueError(f'{split}: invalid reference, duplicate audio path, or missing speaker')
        if not frame.MEDIAN_func_num.between(0, 63).all():
            raise ValueError(f'{split}: analyzer labels outside grid')
        tables[split] = frame
        audit['files'][split] = dict(sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
            rows=len(frame), speakers=int(frame.client_id.nunique()),
            missing_accent=int(frame.accent.isna().sum()),
            transcript_count_mismatches=int((frame.sentence.str.split().str.len() != frame.num_words).sum()))
    for left, right in [('train', 'validation'), ('train', 'test'), ('validation', 'test')]:
        overlap = len(set(tables[left].client_id) & set(tables[right].client_id))
        audit['speaker_overlap'][f'{left}/{right}'] = overlap
        if overlap:
            raise ValueError(f'Speaker overlap: {left}/{right}: {overlap}')
        lp = tables[left].aud_path.str.replace('\\', '/', regex=False).str.rsplit('/').str[-1]
        rp = tables[right].aud_path.str.replace('\\', '/', regex=False).str.rsplit('/').str[-1]
        if set(lp) & set(rp):
            raise ValueError(f'Audio filename overlap: {left}/{right}')
    train = tables['train']
    train_errors = np.abs(train[COUNTERS].to_numpy() / train.num_words.to_numpy()[:, None] - 1).mean(axis=0)
    fixed = COUNTERS[int(np.argmin(train_errors))]
    model = LinearRegression().fit(train[FEATURES], train.MEDIAN_func_num)
    audit['model'] = dict(features=FEATURES, target='MEDIAN_func_num',
        training_r2=float(model.score(train[FEATURES], train.MEDIAN_func_num)),
        coefficients=model.coef_.tolist(), intercept=float(model.intercept_),
        train_selected_counter=fixed, selection_metric='training mean absolute relative error',
        rounding='nearest integer, ties to even; clip to 0..63')
    rows, groups = [], []
    for split in ['validation', 'test']:
        frame = tables[split]
        predictions = {'Legacy fixed counter': frame['count_15_n-2_15'].to_numpy(),
                       'Train-selected fixed counter': frame[fixed].to_numpy(),
                       'Acoustic analyzer selector': select_counts(frame, model.predict(frame[FEATURES]))}
        for name, pred in predictions.items():
            rows.append(dict(split=split, method=name, n=len(frame), **metrics(frame.num_words, pred)))
            # Descriptive errors, not causal group comparisons. Preserve missing accent as Unknown.
            for column in ['gender', 'age', 'accent']:
                labels = frame[column].fillna('Unknown').astype(str)
                for group in sorted(labels.unique()):
                    mask = labels == group
                    groups.append(dict(split=split, method=name, dimension=column, group=group,
                                       n=int(mask.sum()), **metrics(frame.loc[mask, 'num_words'], pred[mask])))
    pd.DataFrame(rows).to_csv(output_dir / 'metrics.csv', index=False)
    pd.DataFrame(groups).to_csv(output_dir / 'subgroup_metrics.csv', index=False)
    (output_dir / 'data_audit.json').write_text(json.dumps(audit, indent=2) + '\n')
    print(pd.DataFrame(rows).to_string(index=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', type=Path, default=Path('.'))
    parser.add_argument('--output-dir', type=Path, default=Path('reports'))
    args = parser.parse_args()
    run(args.data_dir, args.output_dir)
