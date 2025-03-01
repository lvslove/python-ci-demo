pipeline {
    agent any

    environment {
        CONTAINER_NAME = 'python-tests-container'
        ALLURE_RESULTS_DIR = 'target/allure-results'
        JOB_NAME = 'test'
    }

    stages {
        stage('Notify GitHub: Build Started') {
            steps {
                script {
                    // Уведомляем GitHub, что сборка началась
                    // context: произвольная строка, которая будет видна в GitHub как контекст статуса
                    // description: краткое описание, которое отобразится на GitHub
                    githubNotify context: 'jenkins/build',
                                 status: 'PENDING',
                                 description: 'Build is in progress'
                }
            }
        }

        stage('Determine Changes') {
            steps {
                sh 'ls -a'
                sh 'pwd'
                script {
                    def changes = sh(returnStdout: true, script: 'git diff-tree --no-commit-id --name-only -r HEAD').trim()
                    echo "Измененные файлы:\n${changes}"
                    // при желании здесь можно выставлять переменные окружения, если нужно
                    // env.UI_CHANGED = changes.contains('frontend/').toString()
                    // env.BACKEND_CHANGED = changes.contains('backend/').toString()
                }
            }
        }

        stage('Build Docker Container') {
            steps {
                sh '''
                echo "Создаем контейнер для тестов..."
                docker run -d --rm --name ${CONTAINER_NAME} \
                           -v /var/lib/docker/volumes/jenkins-data/_data/workspace/${JOB_NAME}:/app \
                           -w /app python:3.9 tail -f /dev/null
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                echo "Проверяем файлы внутри контейнера..."
                docker exec ${CONTAINER_NAME} ls -la /app

                echo "Устанавливаем зависимости..."
                docker exec ${CONTAINER_NAME} pip install --no-cache-dir -r /app/requirements.txt
                '''
            }
        }

        stage('Run Flake8 Linting') {
            steps {
                sh '''
                echo "Запускаем линтер..."
                mkdir -p ${ALLURE_RESULTS_DIR}
                docker exec ${CONTAINER_NAME} pytest --flake8 . --alluredir=${ALLURE_RESULTS_DIR}
                '''
            }
        }
    }

    post {
        success {
            script {
                // Если сборка прошла успешно, уведомляем GitHub о статусе SUCCESS
                githubNotify context: 'jenkins/build',
                             status: 'SUCCESS',
                             description: 'Build succeeded'
            }
        }
        failure {
            script {
                // Если сборка упала, уведомляем GitHub о статусе FAILURE
                githubNotify context: 'jenkins/build',
                             status: 'FAILURE',
                             description: 'Build failed'
            }
        }
        always {
            script {
                // Проверяем, есть ли результаты Allure
                def resultsExist = sh(returnStatus: true, script: '''
                    [ -d ${ALLURE_RESULTS_DIR} ] && [ "$(ls -A ${ALLURE_RESULTS_DIR})" ]
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
            docker stop ${CONTAINER_NAME} || true
            docker rm ${CONTAINER_NAME} || true
            rm -rf allure.zip ${ALLURE_RESULTS_DIR}
            '''
        }
    }
}
