# pygloss Cleanup Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Strip Go artifacts, rename the Python package from `lipgloss` to `pygloss`, update `bubblepy` references to `bubblepy`, and update all documentation to reflect the new naming.

**Architecture:** Three independent concerns executed in sequence: (1) delete Go files, (2) rename the Python package directory and fix all import references, (3) rename bubbletea files/imports and update docs. Each concern is independently testable via `pytest`.

**Tech Stack:** Python 3.10+, pytest, sed for bulk text replacement, git mv for tracked renames.

---

### Task 1: Delete Go source files and Go-only configs

**Files to delete (all Go source + build artifacts):**
- Root-level `.go` files: `align.go`, `align_test.go`, `ansi_unix.go`, `ansi_windows.go`, `borders.go`, `borders_test.go`, `color.go`, `color_test.go`, `get.go`, `join.go`, `join_test.go`, `lipgloss.go`, `position.go`, `ranges.go`, `ranges_test.go`, `renderer.go`, `renderer_test.go`, `runes.go`, `runes_test.go`, `set.go`, `size.go`, `style.go`, `style_test.go`, `unset.go`, `whitespace.go`
- Go module files: `go.mod`, `go.sum`
- Go tooling: `.golangci.yml`, `.goreleaser.yml`, `Taskfile.yaml`
- Go sub-packages (directories): `list/`, `table/`, `tree/` (root-level only — NOT `lipgloss/list`, `lipgloss/table`, `lipgloss/tree`)
- Go examples: `examples/layout/`, `examples/list/`, `examples/ssh/`, `examples/table/`, `examples/tree/`
- Go CI workflows: `.github/workflows/build.yml`, `.github/workflows/lint.yml`, `.github/workflows/lint-sync.yml`, `.github/workflows/coverage.yml`, `.github/workflows/release.yml`, `.github/workflows/dependabot-sync.yml`
- Go GitHub config: `.github/dependabot.yml`, `.github/CODEOWNERS`

**Step 1: Delete root-level .go files**

```bash
cd /home/matt/github/pygloss
git rm *.go
```

Expected output: lists all .go files being removed.

**Step 2: Delete go.mod, go.sum, and Go tooling**

```bash
git rm go.mod go.sum .golangci.yml .goreleaser.yml Taskfile.yaml
```

**Step 3: Delete root-level Go sub-package directories**

```bash
git rm -r list/ table/ tree/
```

> Note: These are the Go `list/`, `table/`, `tree/` directories at the repo root — NOT `lipgloss/list/`, `lipgloss/table/`, `lipgloss/tree/` which are the Python sub-packages and must be kept.

**Step 4: Delete Go example subdirectories**

```bash
git rm -r examples/layout/ examples/list/ examples/ssh/ examples/table/ examples/tree/
```

**Step 5: Delete Go-specific GitHub Actions workflows and config**

```bash
git rm .github/workflows/build.yml .github/workflows/lint.yml .github/workflows/lint-sync.yml \
       .github/workflows/coverage.yml .github/workflows/release.yml \
       .github/workflows/dependabot-sync.yml \
       .github/dependabot.yml .github/CODEOWNERS
```

**Step 6: Verify Python package is intact**

```bash
python3 -c "import sys; sys.path.insert(0, '.'); import pygloss; print('OK')"
```

Expected: `OK`

**Step 7: Commit**

```bash
git commit -m "chore: remove Go source files and Go-only tooling"
```

---

### Task 2: Rename Python package directory `lipgloss/` → `pygloss/`

The package directory rename must be done with `git mv` so git tracks it. After renaming, all `import pygloss` and `from pygloss` statements in Python files need updating. The internal package files use relative imports (`from ..style import Style`) so they do NOT need updating.

**Files with `import pygloss` / `from pygloss` that must be updated:**
- `tests/conftest.py`
- `tests/test_borders.py`
- `tests/test_bubbletea_integration.py`
- `tests/test_color.py`
- `tests/test_join.py`
- `tests/test_list.py`
- `tests/test_position.py`
- `tests/test_renderer.py`
- `tests/test_runes.py`
- `tests/test_size.py`
- `tests/test_style.py`
- `tests/test_table.py`
- `tests/test_themes.py`
- `tests/test_tree.py`
- `examples/basic_style.py`
- `examples/bubbletea_counter.py`
- `examples/bubbletea_layout.py`
- `examples/layout.py`
- `examples/list.py`
- `examples/table.py`
- `examples/tree.py`

**Step 1: Rename the package directory**

```bash
cd /home/matt/github/pygloss
git mv lipgloss pygloss
```

**Step 2: Bulk-replace `import pygloss` → `import pygloss` in all Python files**

```bash
find tests/ examples/ -name "*.py" | xargs sed -i 's/import pygloss/import pygloss/g'
```

**Step 3: Bulk-replace `from pygloss` → `from pygloss` in all Python files**

```bash
find tests/ examples/ -name "*.py" | xargs sed -i 's/from pygloss/from pygloss/g'
```

**Step 4: Bulk-replace `lipgloss\.` references (e.g. `lipgloss.Style`) in tests and examples**

```bash
find tests/ examples/ -name "*.py" | xargs sed -i 's/lipgloss\./pygloss./g'
```

**Step 5: Verify the package imports correctly**

```bash
python3 -c "import sys; sys.path.insert(0, '.'); import pygloss; print(pygloss.__version__ if hasattr(pygloss,'__version__') else 'OK')"
```

Expected: `OK` (or a version string)

**Step 6: Run tests to confirm nothing is broken**

```bash
pytest tests/ -x -q --ignore=tests/test_bubbletea_integration.py 2>&1 | tail -5
```

Expected: all tests pass (bubbletea integration test excluded for now — handled in Task 3).

**Step 7: Commit**

```bash
git add -A
git commit -m "refactor: rename package lipgloss → pygloss"
```

---

### Task 3: Update bubbletea → bubblepy references

Three files reference `bubblepy`: two example files and one test file. Each needs its `import bubbletea` replaced with `import bubblepy`, and the files themselves renamed.

**Step 1: Rename example files with git mv**

```bash
cd /home/matt/github/pygloss
git mv examples/bubbletea_counter.py examples/bubblepy_counter.py
git mv examples/bubbletea_layout.py examples/bubblepy_layout.py
```

**Step 2: Rename the test file with git mv**

```bash
git mv tests/test_bubbletea_integration.py tests/test_bubblepy_integration.py
```

**Step 3: Rename BUBBLETEA_ISSUES.md**

```bash
git mv BUBBLETEA_ISSUES.md BUBBLEPY_ISSUES.md
```

**Step 4: Replace `import bubbletea` → `import bubblepy` in the renamed files**

```bash
sed -i 's/import bubbletea/import bubblepy/g' \
    examples/bubblepy_counter.py \
    examples/bubblepy_layout.py \
    tests/test_bubblepy_integration.py
```

**Step 5: Replace `bubblepy` module variable references (e.g. `bubbletea = pytest.importorskip...`)**

```bash
sed -i 's/bubbletea = pytest\.importorskip/bubblepy = pytest.importorskip/g' \
    tests/test_bubblepy_integration.py
```

**Step 6: Replace remaining `bubblepy` identifier references in BUBBLEPY_ISSUES.md header**

```bash
sed -i 's/Bubbletea Fork/Bubblepy Fork/g; s/tbdtechpro\/bubbletea/tbdtechpro\/bubblepy/g' BUBBLEPY_ISSUES.md
```

**Step 7: Run the integration test**

```bash
pytest tests/test_bubblepy_integration.py -v 2>&1 | tail -10
```

Expected: all integration tests pass (bubblepy is already installed at `/home/matt/github/bubblepy`).

**Step 8: Commit**

```bash
git add -A
git commit -m "refactor: rename bubbletea → bubblepy in examples, tests, and docs"
```

---

### Task 4: Update pyproject.toml and setup.py

**Files to modify:**
- `pyproject.toml`
- `setup.py`

**Step 1: Update pyproject.toml**

Changes to make:
- `name = "lipgloss"` → `name = "pygloss"`
- `description` → `"CSS-like terminal styling for Python — pygloss port of the Go Lip Gloss library"`
- `Homepage` → `"https://github.com/tbdtechpro/pygloss"`
- `Documentation` → `"https://github.com/tbdtechpro/pygloss#readme"`
- `Repository` → `"https://github.com/tbdtechpro/pygloss"`
- `Issues` → `"https://github.com/tbdtechpro/pygloss/issues"`
- `include = ["lipgloss*"]` → `include = ["pygloss*"]`
- `lipgloss = ["py.typed"]` → `pygloss = ["py.typed"]`
- `keywords`: replace `"lipgloss"` with `"pygloss"`
- `[tool.black]` paths: `lipgloss/` → `pygloss/`
- `[tool.mypy]` path: `lipgloss/` → `pygloss/`
- `[tool.pytest.ini_options]` — no change needed

```bash
cd /home/matt/github/pygloss
sed -i \
  's/^name = "lipgloss"/name = "pygloss"/' \
  's/include = \["lipgloss\*"\]/include = ["pygloss*"]/' \
  pyproject.toml
# Then manually update URLs and package-data key (see step 2 for sed)
```

Actually, do these replacements precisely with a single sed call:

```bash
sed -i \
  -e 's/^name = "lipgloss"/name = "pygloss"/' \
  -e 's|https://github.com/tbdtechpro/pygloss|https://github.com/tbdtechpro/pygloss|g' \
  -e 's/include = \["lipgloss\*"\]/include = ["pygloss*"]/' \
  -e 's/^lipgloss = \["py\.typed"\]/pygloss = ["py.typed"]/' \
  -e 's/"lipgloss"/"pygloss"/' \
  -e 's| lipgloss/| pygloss/|g' \
  pyproject.toml
```

**Step 2: Update setup.py**

```bash
sed -i \
  -e 's/name="lipgloss"/name="pygloss"/' \
  -e 's|https://github.com/tbdtechpro/pygloss|https://github.com/tbdtechpro/pygloss|g' \
  -e 's/"lipgloss": \["py\.typed"\]/"pygloss": ["py.typed"]/' \
  -e 's/"lipgloss"/"pygloss"/g' \
  setup.py
```

**Step 3: Update .github/workflows/python.yml paths**

The workflow references `lipgloss/` in its black, isort, flake8, mypy, and pytest commands:

```bash
sed -i 's/lipgloss\//pygloss\//g' .github/workflows/python.yml
```

**Step 4: Verify package installs cleanly under new name**

```bash
pip install -e ".[dev]" -q && python3 -c "import pygloss; print('pygloss import OK')"
```

Expected: `pygloss import OK`

**Step 5: Run full test suite**

```bash
pytest tests/ -q 2>&1 | tail -5
```

Expected: all tests pass.

**Step 6: Commit**

```bash
git add pyproject.toml setup.py .github/workflows/python.yml
git commit -m "chore: update package name to pygloss in pyproject.toml and setup.py"
```

---

### Task 5: Update documentation

**Files to update:**
- `README.md` — package name, install command, import examples, URLs, repo name
- `MVP_TASKS.md` — bubbletea → bubblepy, lipgloss → pygloss
- `lipgloss-improvements.md` — bubbletea → bubblepy, lipgloss → pygloss
- `BUBBLEPY_ISSUES.md` — already partially done in Task 3; do a final pass
- `CHANGELOG.md` — update package name references
- `CLAUDE.md` — update package name references
- `docs/python-guide.md` — update import examples

**Step 1: Bulk replace `lipgloss` → `pygloss` in all .md files (excluding the Go library URL)**

```bash
cd /home/matt/github/pygloss
# Replace package/repo references but preserve the charmbracelet/lipgloss upstream URL
find . -name "*.md" ! -path "./.git/*" | xargs sed -i \
  -e 's|tbdtechpro/pygloss|tbdtechpro/pygloss|g' \
  -e 's/`import pygloss`/`import pygloss`/g' \
  -e 's/pip install pygloss/pip install pygloss/g'
```

**Step 2: Replace bubbletea → bubblepy in .md files**

```bash
find . -name "*.md" ! -path "./.git/*" | xargs sed -i \
  -e 's/tbdtechpro\/bubbletea/tbdtechpro\/bubblepy/g' \
  -e 's/Python Bubblepy/Python Bubblepy/g' \
  -e 's/`bubblepy`/`bubblepy`/g' \
  -e 's/import bubbletea/import bubblepy/g'
```

**Step 3: Update README.md header and description**

Open `README.md` and update:
- Title: `# lipgloss — Python port (experiment)` → `# pygloss — Python port of Lip Gloss`
- Any `pip install pygloss` → `pip install pygloss`
- Any `import pygloss` → `import pygloss` in code blocks
- Status section note about "Go source remains as reference" → remove or update to note Go source has been removed; pygloss is the Python implementation

**Step 4: Run a final grep to catch any remaining stale references**

```bash
grep -rn "tbdtechpro/pygloss\|tbdtechpro/bubblepy\|import pygloss\|import bubbletea" \
  --include="*.md" --include="*.py" --include="*.toml" . | grep -v ".git" | grep -v "charmbracelet"
```

Expected: no output (all references updated).

**Step 5: Commit**

```bash
git add -A
git commit -m "docs: update all documentation to reflect pygloss and bubblepy naming"
```

---

### Task 6: Final verification and push

**Step 1: Run full test suite one last time**

```bash
pytest tests/ -v 2>&1 | tail -20
```

Expected: all tests pass.

**Step 2: Verify the package installs and imports correctly**

```bash
python3 -c "
import pygloss
from pygloss import Style, Color, join_horizontal, join_vertical
from pygloss.table import Table
from pygloss.list import List
from pygloss.tree import Tree
print('All imports OK')
"
```

Expected: `All imports OK`

**Step 3: Verify no stale references remain**

```bash
grep -rn "tbdtechpro/pygloss\|tbdtechpro/bubblepy\|import pygloss\|import bubbletea\|\"lipgloss\"" \
  --include="*.py" --include="*.toml" --include="*.md" --include="*.yml" . \
  | grep -v ".git" | grep -v "charmbracelet"
```

Expected: no output.

**Step 4: Push to origin**

```bash
git push origin master
```

Expected: all commits pushed to `https://github.com/tbdtechpro/pygloss`.
