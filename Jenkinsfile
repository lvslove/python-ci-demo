pipeline {
    agent {
        docker {
            image 'python:3.9'
        }
    }
    environment {
        PATH = "$PATH:/usr/local/bin"
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
        stage('Setup Dependencies') {
            when {
                expression { env.UI_CHANGED == 'true' }
            }
            steps {
                sh '''
                apt-get update && apt-get install -y wget unzip google-chrome-stable \
                    libnss3 libx11-xcb1 libxcomposite1 libxcursor1 libxdamage1 \
                    libxi6 libxtst6 libglib2.0-0 libxrandr2 libasound2 libpangocairo-1.0-0
                '''
            }
        }
        stage('Install Python Dependencies') {
            steps {
                sh '''
                python -m pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }
        stage('Run Backend Tests') {
            when {
                expression { env.BACKEND_CHANGED == 'true' }
            }
            steps {
                script {
                    try {
                        sh 'pytest backend --alluredir=allure-results'
                    } catch (Exception e) {
                        echo "Backend tests failed: ${e.message}"
                    }
                }
            }
        }
        stage('Run UI Tests') {
            when {
                expression { env.UI_CHANGED == 'true' }
            }
            steps {
                script {
                    try {
                        sh 'pytest frontend --alluredir=allure-results'
                    } catch (Exception e) {
                        echo "UI tests failed: ${e.message}"
                    }
                }
            }
        }
    }
    post {
        always {
            // Генерация Allure-отчета
            script {
                allure([
                    includeProperties: false,
                    jdk: '',
                    properties: [],
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: 'allure-results']]
                ])
            }
            // Очистка рабочей директории
            cleanWs()
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}
