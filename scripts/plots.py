"""Generate the three required PNG charts using measured CSV rows only."""
import csv
import statistics
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
with (ROOT / 'results/results.csv').open() as stream:
    rows = list(csv.DictReader(stream))
COLORS = {'recursive': '#a43b33', 'table': '#245ea8', 'two_rows': '#008577', 'naive': '#a43b33', 'kmp': '#245ea8'}
plt.rcParams.update({'font.size': 10, 'axes.spines.top': False, 'axes.spines.right': False})

def series(ax, algorithm, kind, field):
    data = [r for r in rows if r['algorithm'] == algorithm and r['input'] == kind]
    sizes = sorted({int(r['n']) for r in data})
    values = [statistics.median(float(r[field]) for r in data if int(r['n']) == n) for n in sizes]
    ax.plot(sizes, values, 'o-' if kind == 'worst' else 's--', color=COLORS[algorithm],
            label=algorithm.replace('_', ' ') + ' / ' + kind, linewidth=1.7, markersize=4)

def finish(fig, axes, title, filename):
    fig.suptitle(title, fontsize=14, fontweight='bold')
    for ax in axes:
        ax.set_yscale('log')
        ax.grid(True, which='major', alpha=.2)
        ax.legend(fontsize=8)
    fig.tight_layout(rect=(0, 0, 1, .93))
    fig.savefig(ROOT / 'results/plots' / filename, dpi=180)
    plt.close(fig)

fig, axes = plt.subplots(1, 2, figsize=(10, 3.4))
for kind in ['random', 'worst']:
    series(axes[0], 'recursive', kind, 'operations')
    for algorithm in ['table', 'two_rows']:
        series(axes[1], algorithm, kind, 'operations')
axes[0].set(title='Direct recursion', xlabel='String length n (characters)', ylabel='Calls per run (count, log scale)')
axes[1].set(title='DP curves overlap exactly', xlabel='String length n (characters)', ylabel='Interior updates per run (count, log scale)')
finish(fig, axes, 'Edit distance: measured work', '01_edit_work.png')

fig, axes = plt.subplots(1, 2, figsize=(10, 3.4))
for ax, kind in zip(axes, ['random', 'worst']):
    for algorithm in ['naive', 'kmp']:
        series(ax, algorithm, kind, 'operations')
    ax.set(title=kind.capitalize() + ' input; pattern m = n/32', xlabel='Text length n (characters)',
           ylabel='Comparisons per run (count, log scale)')
finish(fig, axes, 'String search: comparisons including LPS construction', '02_search_work.png')

fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))
for ax, algorithms, title in zip(axes, [['recursive'], ['table', 'two_rows'], ['naive', 'kmp']],
                               ['Recursion', 'Dynamic programming', 'String search']):
    for algorithm in algorithms:
        for kind in ['random', 'worst']:
            series(ax, algorithm, kind, 'time_ms')
    ax.set(title=title, xlabel='Length n (characters)', ylabel='Median time (ms, log scale)')
finish(fig, axes, 'Elapsed time: median of 3 measured runs after one warm-up', '03_median_time.png')
print('Created 3 PNG plots in results/plots/.')
