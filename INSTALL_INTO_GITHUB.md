# Apply this release to theninthfoundry/bhow

The ChatGPT GitHub integration currently has read permission but **no repository push permission**. No GitHub branch or PR was created here.

## Simplest method — Git checkout + overlay

1. Clone [theninthfoundry/bhow](https://github.com/theninthfoundry/bhow) into a clean local folder (or use your existing clean checkout).
2. Extract the entire release ZIP; copy **all files and folders from the ZIP root** into your cloned repository root, overwriting matching files. Keep `.git` unchanged. The legacy directory is intentionally still called `bhow-v0.2/`.
3. Review differences before committing: `git diff --stat` and `git diff`.
4. Run verification:

```bash
cd bhow-v0.2
python -m pip install -e '.[dev]'
ruff check src tests client
mypy --strict src/bhow_core
pytest -q
cd ..
git add README.md RELEASE_NOTES.md INSTALL_INTO_GITHUB.md SHA256SUMS.txt .github bhow-v0.2
git commit -m "fix: Bhow v0.3.1 CI and staging guardrails"
git push origin main
```

**Prefer a new feature branch and a pull request** on shared repositories. Do not force-push. Never commit `.env` or passwords.

For Windows PowerShell, activate your Python virtual environment and run the same Python and git commands (PowerShell supports these), or open a Git Bash terminal. The nested `.env.example` is a template; use your own protected environment variables for staging.

## Verification and scope

The package builds on local v0.3 audit remediation code, while the GitHub `main` revision observed on 2026-10-27 still has v0.2.1 source. Review differences so changes made by other collaborators are not accidentally overwritten. The archive is a **full replacement source tree** rather than a minimal four-line diff. Its staging Compose configuration does not deploy to the public internet.
