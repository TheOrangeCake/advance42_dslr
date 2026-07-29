# advance42_dslr

Datascience X Logistic Regression: rebuild a Hogwarts Sorting Hat from student
grades, using a logistic regression trained with gradient descent.

Everything is written with the standard library only (`csv`, `math`) apart from
`matplotlib` for the plots. No `numpy`, no `pandas`, no `sklearn` — every
statistic and every gradient step is computed by hand.

## Install

```sh
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

The `Makefile` calls `venv/bin/python3` directly, so activating the venv is only
needed when running things by hand:

```sh
source venv/bin/activate
```

(`make install` does the same two steps, but only once `venv/` already exists —
it invokes `venv/bin/python3` to create the venv it is supposed to be creating.)

## Run

Every target runs against `src/datasets/dataset_train.csv`:

| Command          | What it does                                            |
| ---------------- | ------------------------------------------------------- |
| `make describe`  | Print per-feature statistics                            |
| `make histogram` | Score distribution per course, per house                |
| `make scatter`   | Every feature pair, plus the two most similar features   |
| `make train`     | Train the model, write `weights.csv`                    |
| `make all`       | All of the above, in order                              |
| `make flake`     | Lint `src` with flake8                                  |
| `make require`   | Refresh `requirements.txt` from the venv                |

`make dummy` and `make dummy2` run `describe` against small edge-case datasets
(empty columns, non numeric columns) to check it does not crash.

Each script also runs standalone and takes the dataset path as its only
argument:

```sh
venv/bin/python3 src/model/logreg_train.py src/datasets/dataset_train.csv
```

Figures are written to `plots/<kind>/` and opened in a window.

## Part 1 — describe

`src/describe/describe.py` reimplements `DataFrame.describe()`. It keeps only
the numeric columns (`only_numeric()` drops `Index` and anything that fails to
parse as a float), sorts each column, then computes:

- `Min`, `Max` — first and last value of the sorted column
- `25%`, `50%`, `75%` — percentiles by linear interpolation between the two
  surrounding values
- `Range` — `Max - Min` (bonus)
- `NaN` — number of empty cells in the raw column (bonus)

Empty cells are skipped rather than counted as zero, so a missing grade does not
drag a percentile down.

`Count`, `Mean` and `Std` have display slots in `display.py` but are not
computed yet — `display()` skips any field left unset, which is why they are
absent from the current output.


## Part 2 — visualization

Both scripts colour by house (Gryffindor red, Ravenclaw blue, Hufflepuff yellow,
Slytherin green) and skip the non-course columns (`Index`, `Hogwarts House`,
names, `Birthday`, `Best Hand`).

**Histogram** (`plots/histogram/histogram.png`) — one subplot per course, four
overlaid transparent histograms, one per house. It answers *which course has a
homogeneous score distribution between all four houses?* A course is homogeneous
when the four coloured shapes sit on top of each other: the houses are
indistinguishable there, so the feature carries almost no information for
sorting. **Answer: Arithmancy and Care of Magical Creatures.**

**Scatter** (`plots/scatter/scatter_*.png`, `similar.png`) — every pair of
courses plotted against each other, nine per figure. It answers *what are the
two features that are similar?* Two features are similar when their scatter
collapses onto a straight line, meaning one is a rescaling of the other and the
second adds nothing new. **Answer: Astronomy and Defense Against the Dark Arts**
— `similar.png` shows that pair alone.

## Part 3 — training

`src/model/logreg_train.py` trains **four independent binary classifiers**, one
per house — the one-vs-all strategy. Each one only answers a yes/no question
("is this student a Gryffindor?"), and each one owns its own set of weights, one
weight per course.

### Preparing the data

1. **Min/max per feature** (`cal_min_max`) over the training set, reusing
   `cal_min`/`cal_max` from part 1.
2. **Normalize** (`normalize`) with `(value - min) / (max - min)`, mapping every
   course onto `[0, 1]`. Without this, Arithmancy (range ≈ 129 000) would
   completely drown Divination (range ≈ 19) and gradient descent would need a
   different step size per feature to converge. A missing grade becomes `0.5` —
   the middle of the range, the least opinionated guess available.
3. **Transpose** (`convert_to_rows`) the column-based dataset into a list of
   `(house, {feature: value})` rows, because training walks student by student.

### The math

**Hypothesis** — score a student, then squash the score into a probability:

```
hθ(x) = g(θᵀx)      θᵀx = θ₁x₁ + θ₂x₂ + ... + θₙxₙ
g(z)  = 1 / (1 + e⁻ᶻ)
```

`θᵀx` is a plain dot product: multiply each grade by that house's weight for the
course and sum. The sigmoid `g` maps the result into `(0, 1)`. `sigmoid()` is
written in two branches to avoid `math.exp` overflowing on large `|z|`.

**Cost** — how wrong the current weights are over the whole set:

```
J(θ) = −(1/m) Σ [ y·log(hθ(x)) + (1 − y)·log(1 − hθ(x)) ]
```

`y` is 1 when the student belongs to the house being trained, 0 otherwise. Only
one of the two terms survives per student. `log` is what makes confident
mistakes expensive: `log(0.5) = -0.69` but `log(0.01) = -4.6`. The leading minus
flips the sum positive, so **lower is better** and 0 is perfect.

**Gradient descent** — nudge every weight against the slope of the cost:

```
θⱼ := θⱼ − α · (1/m) Σ (hθ(x⁽ⁱ⁾) − y⁽ⁱ⁾) · xⱼ⁽ⁱ⁾
```

The `error = p - y` term does the intuitive thing: predicting 0.9 for a student
who is not in the house gives a large positive error, and each weight is pulled
down in proportion to how much that feature contributed.

### The loop

Weights all start at `0.0`. For each epoch, for each house, for each batch: open
a fresh accumulator, add up `error * value` per feature across the batch, then
apply one update using the batch **average** (dividing by `len(batch)` keeps the
step independent of batch size). The cost over the whole set is recorded once
per house per epoch into `history`.

### Hyperparameters

The three constants at the top of the file select the flavour of gradient
descent — `BATCH_SIZE` is what changes the algorithm, the other two are tuned to
match:

| Variant    | `STEP` | `EPOCHS` | `BATCH_SIZE` |
| ---------- | ------ | -------- | ------------ |
| Batch GD   | 0.5    | 1000     | `None`       |
| Mini-batch | 0.5    | 200      | 32           |
| Stochastic | 0.5    | 75       | 1            |

`None` means one batch containing the whole dataset: one update per epoch, very
smooth, many epochs needed. Smaller batches update far more often per epoch, so
they need far fewer epochs to reach the same place — at the cost of a noisier
descent.

### Output

`weights.csv` at the repo root holds everything needed to classify later:

```
Key        | Arithmancy | Astronomy | ...
min        | -24370.0   | -966.74   | ...
max        | 104956.0   | 1016.21   | ...
Gryffindor | -0.052190  | 1.363597  | ...
Ravenclaw  | ...
```

The `min`/`max` rows are saved alongside the weights on purpose: the weights
only mean something in the normalized coordinate system, so any later
prediction has to normalize with **these** bounds and not with bounds
recomputed from its own data.

`plots/model/training_history.png` plots `J(θ)` per epoch for the four houses.
It is the sanity check on the run: the curves must fall and then flatten. A
curve that rises means `STEP` is too large (the updates overshoot the minimum
and bounce further out each time); a curve still visibly falling at the last
epoch means `EPOCHS` is too small.

## Part 4 — using the saved weights

> Not implemented yet: `src/model/logreg_predict.py` does not exist. This is the
> general direction for classifying with `weights.csv`.

Classifying is the forward half of training with the gradient step removed:

1. **Load** `weights.csv` — the `min`/`max` rows and the four house rows.
2. **Normalize** each student with the saved `min`/`max` (not bounds recomputed
   from the file being classified), reusing the training formula.
3. **Score** the student once per house with `hypothesis()`, giving four
   probabilities.
4. **Pick** the house with the highest score and write `Index,Hogwarts House`
   to `houses.csv`.

`hypothesis()` and `sigmoid()` carry over from `logreg_train.py` unchanged.
Since `dataset_test.csv` has no house labels, measure accuracy by running the
same path over `dataset_train.csv` and comparing against the known houses — the
target is at least 98%.

## Resources

- [Logistic regression](https://www.geeksforgeeks.org/machine-learning/understanding-logistic-regression/)

## Dev

- Update the dependency list after installing something new:
```sh
pip freeze > requirements.txt
```
- Lint:
```sh
flake8 src
```

## General structure

dslr/
├── README.md                 Project setup instructions <b>
├── Makefile                  Short commands for running each part <b>
├── requirements.txt          External Python packages <b>
├── src/ <b>
│   ├── datasets/             Training, testing, and dummy CSV data <b>
│   ├── helper/               Code shared by multiple programs <b>
│   ├── describe/             Statistical analysis <b>
│   ├── visualization/        Histograms and scatter plots <b>
│   └── model/                Logistic-regression training <b>
└── subjects/ <b>
    ├── en.subject.pdf        Original school assignment <b>
    └── datasets/             Original copies of the datasets <b>


## The src subdirectories correspond to stages of a typical machine-learning workflow:

CSV data
   ↓
Read and clean data
   ↓
Describe statistics
   ↓
Visualize relationships
   ↓
Train a model
   ↓
Predict classes (not implemented yet)

## Project controls

The root [README.md](/home/syl/42/dslr/README.md) explains how to create a Python virtual environment and install the dependencies.
The [Makefile](/home/syl/42/dslr/Makefile) provides convenient commands:
make describe runs the statistical analysis.
make histogram generates histograms.
make scatter generates scatter plots.
make train trains the logistic-regression model.
make all runs all four in sequence.
make flake checks Python style.

