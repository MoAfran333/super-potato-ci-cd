```groovy
pipeline {
    agent any

    environment {
        PYTHONUNBUFFERED = '1'
        UV_PROJECT_ENVIRONMENT = '.venv'
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
                    echo "Python version:"
                    python3 --version

                    echo "uv version:"
                    uv --version

                    echo "Installing dependencies..."
                    uv sync --frozen
                '''
            }
        }

        stage('Lint / Basic Validation') {
            steps {
                sh '''
                    echo "Checking Python files..."

                    uv run python -m compileall \
                        main.py \
                        new_models.py \
                        test.py

                    echo "Python compilation successful."
                '''
            }
        }

        stage('Tests') {
            steps {
                sh '''
                    echo "Running tests..."
                    uv run pytest -v
                '''
            }
        }

        stage('MLflow Run') {
            steps {
                sh '''
                    echo "Running MLflow experiment..."

                    uv run python main.py
                '''
            }
        }

        stage('Verify MLflow Artifacts') {
            steps {
                sh '''
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
                    echo "Current directory:"
                    pwd

                    echo "Files:"
                    ls -la

                    echo "Copying index.html..."
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
```
