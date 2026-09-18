# Jenkins Sample Project

A small, transparent sample repository for testing a Jenkins CI/CD
pipeline: a working Flask app, unit tests, lint, and a Jenkinsfile with
real security-scanning stages.

## What's in here

```
.
├── Jenkinsfile              # Pipeline: checkout → setup → lint → test → security scans → build → archive
├── app/
│   └── main.py               # Tiny Flask app (health check + add endpoint)
├── tests/
│   └── test_main.py          # pytest unit tests
├── requirements.txt          # Runtime dependency (Flask)
├── requirements-dev.txt      # Lint/test/security tooling
├── SECURITY_CHECKS.md        # What security checks run, and why
├── test-data/                # Generated filler data (see below) — Git LFS tracked
├── .gitattributes            # LFS config for test-data/*.bin
└── .gitignore
```

## Why is this ~200 MB?

You asked for a sample project around 200 MB, which is unusual for
application code — so almost all of that size lives in `test-data/`,
as clearly-labeled random binary files (`.bin`), generated locally with
`/dev/urandom`. That's a common way to test how a Jenkins job handles
cloning, checking out, and archiving a larger repository, without
touching real customer data or shipping any actual executable content.

Those files are configured for **Git LFS** in `.gitattributes` rather
than committed directly, which is best practice for large binaries in
git. If you'd rather commit them directly (no LFS), just remove the
`.gitattributes` entry before your first commit.

## Running locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt

# run the app
python app/main.py

# lint
flake8 app tests

# tests
pytest --cov=app

# security checks (see SECURITY_CHECKS.md for details)
bandit -r app
pip-audit -r requirements.txt
```

## Importing into git / Jenkins

```bash
cd jenkins-sample-project
git init
git lfs install
git add .
git commit -m "Initial commit: Jenkins sample project"
git remote add origin <your-repo-url>
git push -u origin main
```

Then in Jenkins: **New Item → Pipeline → Pipeline script from SCM**,
point it at your repo, and set the script path to `Jenkinsfile`. The
pipeline agent needs `python3`, `pip`, and `zip` available; `gitleaks`
is optional (that stage is skipped automatically if it's not installed).

## Safety notes

- No external network calls in the app code, no data collection, no
  obfuscation — everything is readable at a glance.
- No credentials, tokens, or secrets anywhere in the repo.
- The only "unusual" content is the labeled random-byte filler in
  `test-data/`, explained in `test-data/README.md`.
