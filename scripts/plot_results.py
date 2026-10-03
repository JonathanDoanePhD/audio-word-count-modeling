"""Regenerate the README figure from reports/metrics.csv."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

root = Path(__file__).resolve().parents[1]
data = pd.read_csv(root / 'reports/metrics.csv')
fig, ax = plt.subplots(figsize=(10, 5))
labels = ['Legacy fixed', 'Train-selected fixed', 'Acoustic selector']
colors = ['#475569', '#0f766e', '#7c3aed']
x = np.arange(2)
for i, method in enumerate(data.method.unique()):
    values = data.loc[data.method == method, 'mae_words'].to_numpy()
    bars = ax.bar(x + (i-1)*0.24, values, 0.24, label=labels[i], color=colors[i])
    ax.bar_label(bars, fmt='%.2f', padding=4, fontsize=10)
ax.set_xticks(x, ['Validation (400 clips)', 'Test (400 clips)'])
ax.set_ylabel('Mean absolute error (words) - lower is better')
ax.set_title('Final word-count evaluation', loc='left', fontweight='bold', fontsize=16)
ax.set_ylim(0, 6.5)
ax.legend(frameon=False, ncols=3, loc='upper left')
ax.spines[['top', 'right']].set_visible(False)
fig.text(0.11, 0.02, 'Retrospective evaluation of stored features and counts; no child-development outcomes measured.', fontsize=9, color='#475569')
fig.tight_layout(rect=[0, 0.06, 1, 1])
fig.savefig(root / 'reports/word-count-error.svg')
fig.savefig('/tmp/word-count-error.png', dpi=120)
