
pipeline {
    agent any

    environment {
        PYTHONUNBUFFERED = '1'
        UV_PROJECT_ENVIRONMENT = '.venv'
        PATH = "/var/lib/jenkins/.local/bin:${env.PATH}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Environment') {
            steps {
                sh '''
                    set -eu

                    echo "===== Environment ====="

                    echo "Current user:"
                    whoami

                    echo "Current directory:"
                    pwd

                    echo "Python version:"
                    python3 --version

                    echo "Python location:"
                    which python3

                    echo "uv version:"
                    uv --version

                    echo "uv location:"
                    which uv

                    echo "Python executable:"
                    python3 -c "import sys; print(sys.executable)"

                    echo "Python home:"
                    python3 -c "import os; print(os.path.expanduser('~'))"

                    echo "HOME:"
                    echo "$HOME"

                    echo "Installing dependencies..."
                    uv sync --frozen
                '''
            }
        }

        stage('Lint / Basic Validation') {
            steps {
                sh '''
                    set -eu

                    echo "Checking Python files..."

                    uv run python -m compileall \
                        main.py \
                        new_models.py \
                        test.py

                    echo "Python compilation successful."
                '''
            }
        }

        stage('MLflow Run') {
            steps {
                sh '''
                    set -eu

                    echo "===== MLflow Environment ====="

                    echo "User:"
                    whoami

                    echo "HOME:"
                    echo "$HOME"

                    echo "Python:"
                    which python3
                    python3 --version

                    echo "uv:"
                    which uv
                    uv --version

                    echo "uv Python:"
                    uv run python -c "import sys; print(sys.executable)"

                    echo "Python home:"
                    uv run python -c "import site; print(site.getsitepackages())"

                    echo "MLflow:"
                    uv run python -c "import mlflow; print(mlflow.__version__)"
                    uv run python -c "import mlflow; print('Tracking URI:', mlflow.get_tracking_uri())"

                    echo "===== Running experiment ====="

                    uv run python main.py

                    echo "===== Workspace after MLflow ====="

                    pwd
                    find . -maxdepth 3 -type d | sort
                '''
            }
        }

        stage('Verify MLflow Artifacts') {
            steps {
                sh '''
                    set -eu

                    echo "Checking MLflow artifacts..."

                    test -d mlruns || {
                        echo "ERROR: mlruns directory was not created."
                        exit 1
                    }

                    echo "MLflow artifacts:"
                    find mlruns -maxdepth 3 -type f | sort | head -100
                '''
            }
        }

        stage('Deploy Website') {
            steps {
                sh '''
                    set -eu

                    echo "Current directory:"
                    pwd

                    echo "Files:"
                    ls -la

                    echo "Copying index.html..."

                    test -f index.html || {
                        echo "ERROR: index.html not found."
                        exit 1
                    }

                    cp index.html /var/www/html/index.html

                    echo "Web directory:"
                    ls -la /var/www/html/

                    echo "Deployment complete."
                '''
            }
        }

        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: '''
                    mlruns/**,
                    mlflow.db,
                    pyproject.toml,
                    uv.lock
                ''',
                allowEmptyArchive: true,
                fingerprint: true
            }
        }
    }

    post {
        success {
            echo '======================================'
            echo ' CI/CD PIPELINE PASSED'
            echo '======================================'
        }

        failure {
            echo '======================================'
            echo ' CI/CD PIPELINE FAILED'
            echo '======================================'
        }

        always {
            echo "Build #${BUILD_NUMBER} finished."
        }
    }
}