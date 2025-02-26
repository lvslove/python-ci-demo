pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'python:3.9'
        CONTAINER_NAME = 'python-tests-container'
        ALLURE_RESULTS_DIR = 'target/allure-results'
    }

    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/lvslove/python-ci-demo.git'
            }
        }

        stage('Build Docker Container') {
            steps {
                sh '''
                echo "Создаем контейнер для тестов..."
                docker run -d --name $CONTAINER_NAME -v $(pwd):/app -w /app $DOCKER_IMAGE tail -f /dev/null
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                echo "Устанавливаем зависимости..."
                docker exec $CONTAINER_NAME pip install --no-cache-dir -r requirements.txt
                '''
            }
        }

        stage('Run Flake8 Linting') {
            steps {
                sh '''
                echo "Запускаем линтер..."
                docker exec $CONTAINER_NAME pytest --flake8 . --alluredir=$ALLURE_RESULTS_DIR
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                echo "Запускаем тесты..."
                docker exec $CONTAINER_NAME pytest --alluredir=$ALLURE_RESULTS_DIR
                '''
            }
        }
    }

    post {
        always {
            script {
                def resultsExist = sh(returnStatus: true, script: '''
                [ -d $ALLURE_RESULTS_DIR ] && [ "$(ls -A $ALLURE_RESULTS_DIR)" ]
                ''') == 0

                if (resultsExist) {
                    echo 'Allure results found. Generating report...'
                    allure([
                        includeProperties: false,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: 'target/allure-results']]
                    ])
                } else {
                    echo 'No Allure results found. Tests might not have run.'
                }
            }
        }
        cleanup {
            echo 'Cleaning up...'
            sh '''
            echo "Останавливаем и удаляем контейнер..."
            docker stop $CONTAINER_NAME || true
            docker rm $CONTAINER_NAME || true
            rm -rf venv allure.zip $ALLURE_RESULTS_DIR
            '''
        }
    }
}
