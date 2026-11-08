# DAA Assignment 4 - City Search & Spell-Check

Student: **[Shugay Nurtile]**  
Group: **[SE-2518]**  

Minimal Maven project: three Levenshtein edit distances, Naive and KMP search,
instrumented counters, deterministic inputs, JUnit 5 tests and measured results.
No application frameworks or external Java runtime libraries are needed.

## Build and test

Requirements: JDK 17+ and Maven 3.9+ (or IntelliJ IDEA's bundled Maven).
First Maven build needs Internet access to download build plugins and JUnit.
Open this folder's `pom.xml` in IntelliJ as a Maven project and select JDK 17 or newer.

```sh
mvn clean test
```

Seven JUnit test methods cover all reference values, both empty-string directions,
empty patterns, long patterns, overlaps, 100 random edit pairs, 100 random search
pairs and counter reset behavior. The stored test output records the actual run.

## Run experiment and regenerate charts

From this project folder:

```sh
mvn -q compile
java -cp target/classes daa.Experiment
python -m pip install -r scripts/requirements.txt
python scripts/plots.py
```

On Linux, use `python3` if `python` is unavailable. On Windows the same Java commands
work in PowerShell. In IntelliJ you can run `Experiment.main` directly with the
working directory set to this project folder. CSV and PNG results are already
included, so Python is only needed to recreate plots.

To regenerate both report formats after new measurements (optional):

```sh
python -m pip install reportlab
python scripts/report.py
```

The report script assumes the checked-in test and repeatability validation has
also been rerun if you change algorithm code; review its conclusions after changes.

The experiment overwrites `results/results.csv` with 120 measured rows: 5 algorithms
x 2 input types x 4 sizes x 3 runs. One additional warm-up per case is excluded.
It prints the median times. The generator uses seed 20261108. Inputs, answers and
counters reproduce exactly; elapsed times depend on the machine and cannot repeat
exactly. `n` is first-string/text length and `m` is second-string/pattern length.
`result` is edit distance or number of matches. `operations` means `calls`, `cells`
or `comparisons` as specified by the `counter` column. These units are not interchangeable.
The seed column is the base seed; case seed derivation is in `InputGenerator.java`.

## Project map / requirement checklist

| Requirement | Location |
|---|---|
| Recursive, full-table, two-row distance; DP design comments | `src/main/java/daa/*EditDistance.java` |
| Shared interfaces for both families | `EditDistance.java`, `StringSearch.java` |
| Naive, KMP, public LPS, overlaps and argument rules | `NaiveSearch.java`, `KmpSearch.java` |
| Counters incremented inside algorithms | Algorithm classes; reset on every public algorithm call |
| Fixed-seed generator and 3 timed runs | `InputGenerator.java`, `Experiment.java` |
| Plan recorded before execution | `EXPERIMENT_PLAN.md` (first Git commit) |
| JUnit 5 reference, edge and random tests | `src/test/java/daa/AlgorithmsTest.java` |
| Raw runs / three PNG plots | `results/results.csv`, `results/plots/` |
| Design card, findings, four short answers, time paragraph | `REPORT.md`, four-page `REPORT.pdf` |
| Build, tests, experiment and AI acknowledgement | This README |
| Main branch, incremental commits, final v1.0 tag | Included `.git` directory |

Strings are processed as Java UTF-16 `char` values. Null arguments are outside the
assignment contract. The two-row version computes a distance, not an edit script.
Counters are not thread-safe; the experiment runs sequentially.

## Finish your submission

1. Replace the name, group and GitHub URL placeholders above. Rename the outer ZIP
   to `DAA_Assignment4_name_surname_group.zip` with your actual name and group.
2. Create an empty GitHub repository (do not initialize it with a README).
3. The ZIP includes `.git`, small commits on `main` and local tag `v1.0`. Preserve
   that folder when extracting. Do not run `git init` again.
4. Edit the placeholders before updating the final local tag, then run:

```sh
git config user.name "Your Name"
git config user.email "your-email@example.com"
git add README.md
git commit -m "docs: add student details and repository link"
git tag -f v1.0
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
git push origin v1.0
```

The tag move above is for the supplied **local, unpublished** tag only.
After editing, ZIP the project folder again, excluding `target/`, and submit it to
Moodle with your GitHub link. GitHub publication and Moodle submission are not
performed by this package. The assignment deadline is 08.11.2026 23:59 as stated
in the provided assignment; use the LMS deadline/timezone as authoritative.

