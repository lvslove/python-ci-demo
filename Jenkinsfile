pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'python:3.9'
        CONTAINER_NAME = 'python-tests-container'
        ALLURE_RESULTS_DIR = 'target/allure-results'
    }

    stages {
        stage('Cleanup Workspace') {
            steps {
                script {
                    echo "Очистка рабочей директории перед билдом..."
                    sh 'chmod -R 777 /var/jenkins_home/workspace/test'
                    deleteDir()
                }
            }
        }

        stage('Checkout Repository') {
            steps {
                checkout scm
            }
        }

        stage('Determine Changes') {
            steps {
                sh 'ls -a'
                sh'pwd'
                script {
                    def changes = sh(returnStdout: true, script: 'git diff-tree --no-commit-id --name-only -r HEAD').trim()
                    env.UI_CHANGED = changes.contains('frontend/').toString()
                    env.BACKEND_CHANGED = changes.contains('backend/').toString()
                }
            }
        }

        stage('Build Docker Container') {
            steps {
                sh '''
                echo "Создаем контейнер для тестов..."
                docker run -d --rm --name python-tests-container -v  /var/lib/docker/volumes/jenkins-data/_data/workspace/test:/app -w /app python:3.9 tail -f /dev/null

                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                echo "Проверяем файлы внутри контейнера..."
                docker exec $CONTAINER_NAME ls -la /app
                
                echo "Устанавливаем зависимости..."
                docker exec $CONTAINER_NAME pip install --no-cache-dir -r /app/requirements.txt
                '''
            }
        }

        stage('Run Flake8 Linting') {
            steps {
                sh '''
                echo "Запускаем линтер..."
                mkdir -p $ALLURE_RESULTS_DIR
                docker exec $CONTAINER_NAME pytest --flake8 . --alluredir=$ALLURE_RESULTS_DIR
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
                docker exec $CONTAINER_NAME pytest backend --alluredir=$ALLURE_RESULTS_DIR
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
                docker exec $CONTAINER_NAME pytest frontend --alluredir=$ALLURE_RESULTS_DIR
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
            rm -rf allure.zip $ALLURE_RESULTS_DIR
            '''
        }
    }
}
