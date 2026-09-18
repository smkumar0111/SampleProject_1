# Security Checks in This Sample Project

This repo is a **synthetic sample** built for testing a Jenkins pipeline.
Everything in it is plain, human-readable, and does exactly what it says.
Nothing here makes external network calls, collects data, or hides
behavior. Here's what's included and why:

## 1. Static Application Security Testing (SAST) — Bandit
`bandit` scans the Python source in `app/` for common insecure patterns
(hardcoded passwords, use of `eval`/`exec`, insecure bind addresses,
weak crypto, etc.). Run manually with:

```bash
bandit -r app
```

## 2. Dependency Vulnerability Scan — pip-audit
`pip-audit` checks `requirements.txt` against known CVE databases (OSV).
Run manually with:

```bash
pip-audit -r requirements.txt
```

## 3. Secret Scanning — Gitleaks (optional)
The Jenkinsfile includes an optional stage that runs `gitleaks` if it's
installed on the agent, to catch accidentally committed credentials,
API keys, or tokens. To enable it:

- Install: https://github.com/gitleaks/gitleaks#installing
- Or run it as a Docker step: `docker run -v $(pwd):/repo zricethezav/gitleaks:latest detect -s /repo`

## 4. Lint — flake8
Basic style/quality checks, run before tests so obvious issues fail fast.

## What's deliberately absent
- No `eval`/`exec`/dynamic imports anywhere in `app/`
- No outbound HTTP requests from the app code
- No embedded credentials, tokens, or API keys
- No obfuscated, minified, or base64-packed code
- No executable files in `test-data/` — just raw random bytes (see below)

## About `test-data/`
This project was requested at roughly 200 MB in size (for testing how
the Jenkins job handles cloning/building a larger repository). The
`test-data/` folder contains a few files of random binary data
(generated locally with `/dev/urandom`, nothing downloaded) purely to
reach that size. They're tracked with **Git LFS** (see `.gitattributes`)
rather than committed straight into git history, which is the
recommended way to handle large binary blobs in a git repo. See
`test-data/README.md` for details.
