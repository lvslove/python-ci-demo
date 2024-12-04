pipeline {
    agent any
    stages {
        stage('Setup Environment') {
            steps {
                // Установка Python и pip
                sh '''
                apt-get update
                apt-get install -y python3 python3-pip python3-venv
                '''
                // Проверка версий Python и pip
                sh 'python3 --version'
                sh 'pip3 --version'
            }
        }
        stage('Create Virtual Environment') {
            steps {
                // Создание виртуального окружения
                sh '''
                python3 -m venv venv
                source venv/bin/activate
                '''
            }
        }
        stage('Install Dependencies') {
            steps {
                // Установка зависимостей в виртуальном окружении
                sh '''
                source venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }
        stage('Run Backend Tests') {
            steps {
                // Запуск backend-тестов в виртуальном окружении
                sh '''
                source venv/bin/activate
                pytest backend --alluredir=target/allure-results
                '''
            }
        }
        stage('Run UI Tests') {
            steps {
                // Запуск UI-тестов в виртуальном окружении
                sh '''
                source venv/bin/activate
                pytest frontend --alluredir=target/allure-results
                '''
            }
        }
        stage('Setup Allure CLI') {
            steps {
                // Установка Allure CLI
                sh '''
                curl -o allure.zip -L https://github.com/allure-framework/allure2/releases/latest/download/allure-commandline.zip
                unzip -o allure.zip -d allure
                export PATH=$PATH:$PWD/allure/bin
                '''
                // Проверка установки Allure CLI
                sh 'allure --version'
            }
        }
    }
    post {
        always {
            steps {
                echo 'Generating Allure report...'
                // Генерация Allure отчета независимо от результата этапов
                allure([
                    includeProperties: false,
                    jdk: '',
                    properties: [],
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: 'target/allure-results']]
                ])
            }
        }
        cleanup {
            steps {
                echo 'Cleaning up workspace...'
                // Удаление временных файлов или папок, если требуется
                sh 'rm -rf venv allure.zip'
            }
        }
    }
}
