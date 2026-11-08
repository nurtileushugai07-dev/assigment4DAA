# Experiment Design Card (recorded before running)

| Field | Planned experiment |
|---|---|
| Question | Edit: how do recursive calls and DP cell updates grow? Search: how much repeated work does KMP avoid on a late mismatch? |
| Sizes | Recursive: n=m=3,6,9,12 (4x range; exponential growth limits sizes). Table and two rows: n=m=128,256,512,1024 (8x range). Search: text n=4096,8192,16384,32768; pattern m=n/32 (8x range). |
| Inputs | Edit random: two fixed-seed strings over ABCD, showing typical character matches; edit worst: A repeated n times vs B repeated n times, forcing all recursive branches. Search random: independent ABCD text/pattern; search worst: text A^n and pattern A^(m-1)B, forcing late mismatches at every naive start. |
| Metrics | Edit counts recursive calls including base calls, or interior DP cell updates (different work units, explicitly labeled). Search counts character comparisons including KMP LPS construction. Record each of 3 timed runs in milliseconds with nanoTime, after one unrecorded warm-up per case; use medians in plots. |
| Prediction | Recursive worst-case work grows exponentially; both DP versions update n*m cells and doubling n quadruples work. Two rows reduces stored DP integers from (n+1)(m+1) to 2(m+1). Naive worst-case comparisons grow quadratically because m grows with n; KMP grows linearly in n+m. Random searches should be close to linear. |
| Plots | 1. Edit work vs length, logarithmic y-axis, with separate panels for recursion and DP. 2. Search comparisons vs text length, logarithmic y-axis, random and worst panels. 3. Median time vs length (ms, logarithmic y-axis), separate recursive, DP and search panels. |
| Reproducibility | Seed 20261108; a fresh seed derived from family, input type and n for each case. Inputs, results and counters repeat exactly; wall-clock times inevitably vary. Timing includes counters and result allocation, excludes input generation, CSV writing and correctness checks. |

No changes to this plan are made after measurements.
