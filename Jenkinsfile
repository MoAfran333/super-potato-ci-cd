pipeline {
    agent any

    environment {
        PYTHONUNBUFFERED = '1'
        UV_PROJECT_ENVIRONMENT = '.venv'
        IMAGE_NAME = 'mlflow-test'
        IMAGE_TAG = "${BUILD_NUMBER}"
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

        stage('Build Docker Image') {
            when {
                expression {
                    fileExists('Dockerfile')
                }
            }

            steps {
                sh '''
                    echo "Building Docker image..."

                    docker build \
                        -t ${IMAGE_NAME}:${IMAGE_TAG} \
                        -t ${IMAGE_NAME}:latest \
                        .
                '''
            }
        }

        stage('Deploy Website') {
            steps {
                sh '''
                    echo "Deploying index.html..."

                    cp index.html /var/www/html/index.html

                    echo "Website deployed successfully."
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

