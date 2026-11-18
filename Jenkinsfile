pipeline {
    agent any

    environment {
        APP_ENV = 'production'
        APP_PORT = '8000'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code from Git repository...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Setting up Python virtual environment and installing dependencies...'
                sh '''
                    python3 -m venv venv || virtualenv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo 'Running pytest automated unit test suite...'
                sh '''
                    . venv/bin/activate
                    pytest -v --junitxml=test-results.xml tests/
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'test-results.xml'
                }
            }
        }

        stage('Package Artifact') {
            steps {
                echo 'Packaging application artifact into tarball...'
                sh '''
                    mkdir -p dist
                    tar --exclude='.git' --exclude='venv' --exclude='__pycache__' --exclude='.pytest_cache' \
                        -czvf dist/app-artifact.tar.gz app/ requirements.txt tests/ repo_link.txt
                    ls -lh dist/
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded! Archiving build artifact...'
            archiveArtifacts artifacts: 'dist/app-artifact.tar.gz', fingerprint: true
        }
        failure {
            echo 'Pipeline failed! Please check console log for errors.'
        }
    }
}
