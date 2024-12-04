pipeline {
    agent any
    stages {

        stage('Setup Environment') {
            steps {
                // Установка Python и pip
                sh '''
                apt-get update
                apt-get install -y python3 python3-pip
                '''
                // Проверка версий Python и pip
                sh 'python3 --version'
                sh 'pip3 --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }
        stage('Run Backend Tests') {
            steps {
                sh 'pytest backend --alluredir=allure-results'
            }
        }
        stage('Run UI Tests') {
            steps {
                sh 'pytest frontend --alluredir=allure-results'
            }
        }
        stage('Generate Allure Report') {
            steps {
                allure([
                    includeProperties: false,
                    jdk: '',
                    properties: [],
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: 'allure-results']]
                ])
            }
        }
    }
    post {
        always {
            echo 'Pipeline completed successfully!'
        }
    }
}
