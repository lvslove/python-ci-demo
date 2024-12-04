pipeline {
    agent {
        docker {
            image 'python:3.9'
        }
    }
    stages {
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
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
