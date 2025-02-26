pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'python:3.9'
        CONTAINER_NAME = 'python-tests-container'
        ALLURE_RESULTS_DIR = 'target/allure-results'
        VENV_PATH = '/app/venv/bin'
    }

    stages {
        stage('Determine Changes') {
            steps {
                script {
                    def changes = sh(returnStdout: true, script: 'git diff-tree --no-commit-id --name-only -r HEAD').trim()
                    env.UI_CHANGED = changes.contains('frontend/')
                    env.BACKEND_CHANGED = changes.contains('backend/')
                }
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

        stage('Create Virtual Environment') {
            steps {
                sh '''
                echo "Создаем виртуальное окружение..."
                docker exec $CONTAINER_NAME python3 -m venv /app/venv
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                echo "Устанавливаем зависимости..."
                docker exec $CONTAINER_NAME $VENV_PATH/pip install --no-cache-dir -r requirements.txt
                '''
            }
        }

        stage('Run Flake8 Linting') {
            steps {
                sh '''
                echo "Запускаем линтер..."
                docker exec $CONTAINER_NAME $VENV_PATH/pytest --flake8 . --alluredir=$ALLURE_RESULTS_DIR
                '''
            }
        }

        stage('Run Backend Tests') {
            when {
                expression { env.BACKEND_CHANGED == 'true' }
            }
            steps {
                sh '''
                echo "Запускаем backend-тесты..."
                docker exec $CONTAINER_NAME $VENV_PATH/pytest backend --alluredir=$ALLURE_RESULTS_DIR
                '''
            }
        }

        stage('Run UI Tests') {
            when {
                expression { env.UI_CHANGED == 'true' }
            }
            steps {
                sh '''
                echo "Запускаем UI-тесты..."
                docker exec $CONTAINER_NAME $VENV_PATH/pytest frontend --alluredir=$ALLURE_RESULTS_DIR
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
