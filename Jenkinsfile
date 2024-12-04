pipeline {
    agent any
    stages {
        stage('Setup Environment') {
            steps {
                sh '''
                apt-get update
                apt-get install -y python3 python3-pip python3-venv
                '''
                sh 'python3 --version'
                sh 'pip3 --version'
            }
        }
        stage('Create Virtual Environment') {
            steps {
                sh '''
                #!/bin/bash
                python3 -m venv venv
                source venv/bin/activate
                '''
            }
        }
        stage('Install Dependencies') {
            steps {
                sh '''
                #!/bin/bash
                source venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }
        stage('Run Backend Tests') {
            steps {
                sh '''
                #!/bin/bash
                source venv/bin/activate
                pytest backend --alluredir=target/allure-results
                '''
            }
        }
        stage('Run UI Tests') {
            steps {
                sh '''
                #!/bin/bash
                source venv/bin/activate
                pytest frontend --alluredir=target/allure-results
                '''
            }
        }
        stage('Setup Allure CLI') {
            steps {
                sh '''
                #!/bin/bash
                curl -o allure.zip -L https://github.com/allure-framework/allure2/releases/latest/download/allure-commandline.zip
                unzip -o allure.zip -d allure
                export PATH=$PATH:$PWD/allure/bin
                '''
                sh '''
                #!/bin/bash
                allure --version
                '''
            }
        }
    }
    post {
        always {
            echo 'Generating Allure report...'
            // Генерация Allure отчета
            allure([
                includeProperties: false,
                jdk: '',
                properties: [],
                reportBuildPolicy: 'ALWAYS',
                results: [[path: 'target/allure-results']]
            ])
        }
        cleanup {
            echo 'Cleaning up workspace...'
            // Удаление временных файлов или папок
            sh '''
            #!/bin/bash
            rm -rf venv allure.zip
            '''
        }
    }
}
