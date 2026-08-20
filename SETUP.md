# ASTR 5820 — Python Setup

*Do this before Tuesday of Week 2. Budget thirty minutes. If it takes longer than
an hour, stop and post on the course Slack — an afternoon lost to a broken conda
install teaches you nothing about planet formation.*

You are building one toolbox, `astrotools`, over the whole semester. Week 2 adds
three functions to it; Week 13 imports what Week 5 wrote. Set it up once, keep it
in git, and never copy a constant from one script into another.

---

## 1. Install

**macOS and Linux — the default path.**

Install [Miniforge](https://conda-forge.org/download/) if you do not already have
conda. Then, from wherever you keep coursework:

```bash
git clone <course-repository-url> astr5820
cd astr5820
conda env create -f environment.yml
conda activate astr5820
pip install -e .
```

`pip install -e .` installs the toolbox in editable mode, so `import astrotools`
works from any directory and picks up your edits immediately. It is the single
step that prevents the most common failure of the semester, which is an
`ImportError` that depends on which folder you happened to be in.

**Windows.** One package in the course, `rebound`, does not build natively on
Windows. It is not needed until Week 9, but set up a working path now rather than
in the middle of Set 4. Either:

- **WSL2** (recommended): install Ubuntu from the Microsoft Store, then follow the
  macOS/Linux instructions inside it. You get a real Linux toolchain and VS Code
  attaches to it directly.
- **GitHub Codespaces**: open the repository on GitHub → *Code* → *Codespaces* →
  *Create codespace*. The `.devcontainer/` configuration installs everything and
  runs the check for you. Free-tier hours are ample for this course.

**Plain virtualenv**, if you would rather not use conda:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt && pip install -e .
```

## 2. Verify

```bash
python check_setup.py
```

Every line should read `OK`. The script checks your Python version, your packages,
that the toolbox imports, that the provided Euler integrator runs, and that
matplotlib can write a file.

It finishes by reporting how many Problem Set 1 tests pass. Nearly all of them
**will fail** — that is the assignment. Setup problems appear above the line of
equals signs; assignment problems appear below it.

## 3. What is in here

```
astrotools/          the toolbox you are building
  constants.py       every number the course uses. Import from here, always.
  cloud/collapse.py  Set 1, stage A  <- you write three functions
  nbody/twobody.py   orbits, initial conditions, conserved quantities (provided)
  nbody/integrators.py  Set 1, stage B  <- you write rk4_step
  data.py            loaders for the archival datasets
tests/               the specification for each coding exercise
ps1/                 driver scripts for the two Problem Set 1 figures
data/                archival data, with provenance in data/README.md
check_setup.py       this file's companion
```

## 4. How a coding exercise works

Every week follows the same three steps.

1. **Read the test first.** `tests/` is the specification. It states the fiducial
   value your function must reproduce and the scaling it must obey. Nothing is
   hidden in it.
2. **Write the function until the test passes.**
   ```bash
   pytest tests/test_ps1a_collapse.py -v
   ```
   Add `-x` to stop at the first failure and `-k jeans` to run one test.
3. **Then apply it to real data.** The tests confirm your code is right; they say
   nothing about whether the physics is. The scientific question — *does the
   predicted spread of disk radii match the observed one, and which input
   dominates it?* — is answered in the figure and the write-up, and that is where
   most of the credit lives.

A passing test is the floor, not the ceiling.

## 5. Handing work in

Submit a single PDF containing your derivations, your figures, and your answers,
plus a link to your repository at the commit you are submitting. Figures must
state where their data came from. Committing as you go is strongly advised: "it
worked last night" is not a recoverable state unless you committed it.

---

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| `ModuleNotFoundError: No module named 'astrotools'` | You skipped `pip install -e .`, or you are in the wrong environment. Run `conda activate astr5820`, then `pip install -e .` from the repository root. |
| `ModuleNotFoundError` for numpy or scipy after installing them | Two Pythons. `python check_setup.py` prints the interpreter path — confirm it sits inside your `astr5820` environment. |
| `rebound` fails to build on Windows | Expected. Use WSL2 or Codespaces (§1). Not needed before Week 9. |
| `conda env create` hangs on "Solving environment" | Use Miniforge rather than Anaconda; the conda-forge-only channel list resolves much faster. |
| Figures do not appear when running a script | Scripts save to `figures/` rather than opening a window. Open the file. In Jupyter, add `%matplotlib inline`. |
| A test fails by roughly a factor of 1.5 | Almost always µ: mass density is `n(H2) * mu * m_H`, and `sqrt(2.33) = 1.53`. |
| A test fails by orders of magnitude | Units. Everything in this course is SI, including inputs. Convert at the boundary, never inside a formula. |
| Jupyter cannot see the environment | `python -m ipykernel install --user --name astr5820`, then pick that kernel. |

Still stuck after fifteen minutes? Post the full output of `python check_setup.py`
on Slack. Someone else has the same problem.
