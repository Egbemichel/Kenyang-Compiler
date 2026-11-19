# Contributing & Git Workflow Guide

This repository uses a simple, clean **feature-branch workflow** so all 4 group members can work at the same time without overwriting each other's code.

---

## 1. Branching Rules

- **`main`**: Always stable and working. **Never commit directly to `main`** after initial setup; all work enters `main` via Pull Requests (PRs) after tests pass.
- **Area / Feature Branches**: Create a branch for your area or task using one of these prefixes:
  - `area-2/parser-ast` (Member 2: Grammar, Parser, AST)
  - `area-3/semantics` or `area-3/optimiser` (Member 3: Symbol Table, Semantic Analyser, Optimiser)
  - `area-4/codegen-runtime` (Member 4: Intermediate Code, Codegen, Runtime)
  - `feat/<short-description>` for new features (e.g., `feat/while-loop-ast`)
  - `fix/<short-description>` for bug fixes (e.g., `fix/string-escape-line-no`)

---

## 2. First-Time Setup (For Teammates)

1. **Clone the repository and enter the folder:**
   ```powershell
   git clone <REPO_URL>
   cd "Compiler construction"
   ```
2. **Install Python dependencies and verify tests pass:**
   ```powershell
   pip install -r requirements.txt
   python -m pytest -v
   ```

---

## 3. Daily Workflow (Step-by-Step)

1. **Make sure your `main` is up to date:**
   ```powershell
   git checkout main
   git pull origin main
   ```
2. **Create your working branch:**
   ```powershell
   git checkout -b area-2/parser-ast
   ```
3. **Write code and run tests before committing:**
   ```powershell
   python -m pytest -v
   ```
4. **Stage and commit your changes (use clear commit messages):**
   ```powershell
   git status
   git add src/ tests/
   git commit -m "feat(parser): add AST nodes and expression rules"
   ```
   **Commit message prefixes:**
   - `feat(area): ...` — new feature
   - `fix(area): ...` — bug fix
   - `docs: ...` — documentation updates
   - `test: ...` — adding or fixing tests
5. **Push your branch and open a Pull Request:**
   ```powershell
   git push -u origin area-2/parser-ast
   ```
   Then open a **Pull Request** into `main` on GitHub/GitLab and ask one teammate to review it.

---

## 4. Keeping Your Branch Up to Date

If someone else merges into `main` while you are working:

```powershell
git fetch origin
git merge origin/main
```

Fix any conflicts if prompted, re-run `python -m pytest -v`, then push again.

---

## 5. Checklist Before Opening a Pull Request

- [ ] `python -m pytest -v` passes with **0 failures**.
- [ ] `python -m src.lexer --check-keywords` passes with **0 collisions** (if `keywords.json` changed).
- [ ] No temporary files (`__pycache__`, `.pytest_cache`, `.exe`, `.o`) are staged.
- [ ] New behavior includes unit tests in `tests/`.
