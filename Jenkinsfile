pipeline {
    agent any

    environment {
        ALLURE_RESULTS_DIR = 'target/allure-results'
        JOB_NAME = 'test'
    }

    stages {

        stage('Determine Changes') {
            steps {
                script {
                    def changes = sh(returnStdout: true, script: 'git diff-tree --no-commit-id --name-only -r HEAD').trim()
                    env.CONTAINER_NAME = "python-tests-container-${env.BUILD_NUMBER}"
                    sh'echo $CONTAINER_NAME'
                    
                }
            }
        }

        stage('Build Docker Container') {
            steps {
                sh '''
                echo "Создаем контейнер для тестов..."
                docker run -d --rm --name $CONTAINER_NAME -v  /var/lib/docker/volumes/jenkins-data-new/_data/workspace/$JOB_NAME:/app -w /app python:3.9 tail -f /dev/null

                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                echo $BUILD_NUMBER
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
            rm -rf allure.zip $ALLURE_RESULTS_DIR
            '''
        }
    }
}