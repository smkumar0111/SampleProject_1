pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt -r requirements-dev.txt
                    mkdir -p reports build
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    . venv/bin/activate
                    flake8 app tests --max-line-length=100
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest --junitxml=reports/tests.xml --cov=app --cov-report=xml:reports/coverage.xml
                '''
            }
            post {
                always {
                    junit 'reports/tests.xml'
                }
            }
        }

        stage('Security: Dependency Scan (pip-audit)') {
            steps {
                sh '''
                    . venv/bin/activate
                    pip-audit -r requirements.txt -f json -o reports/pip-audit.json || true
                '''
            }
        }

        stage('Security: SAST (Bandit)') {
            steps {
                sh '''
                    . venv/bin/activate
                    bandit -r app -f json -o reports/bandit.json || true
                '''
            }
        }

        stage('Security: Secret Scan (Gitleaks)') {
            // Optional stage. Requires the gitleaks binary on the Jenkins agent,
            // or swap this for the Gitleaks Jenkins plugin / a Docker agent.
            // See SECURITY_CHECKS.md for install instructions.
            when {
                expression { return sh(script: 'command -v gitleaks', returnStatus: true) == 0 }
            }
            steps {
                sh 'gitleaks detect --source . --report-path reports/gitleaks.json --exit-code 0'
            }
        }

        stage('Build Artifact') {
            steps {
                sh '''
                    . venv/bin/activate
                    zip -r build/app-package.zip app requirements.txt
                '''
            }
        }

        stage('Archive') {
            steps {
                archiveArtifacts artifacts: 'reports/**, build/**', fingerprint: true, allowEmptyArchive: true
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished. See archived reports/ for lint, test, and security scan output.'
        }
    }
}
