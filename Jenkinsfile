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
                . venv/bin/activate
                '''
            }
        }
        stage('Install Dependencies') {
            steps {
                sh '''
                #!/bin/bash
                . venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }
        stage('Run Backend Tests') {
            steps {
                sh '''
                #!/bin/bash
                . venv/bin/activate
                pytest backend --alluredir=target/allure-results
                '''
            }
        }
        stage('Run UI Tests') {
            steps {
                sh '''
                #!/bin/bash
                . venv/bin/activate
                pytest frontend --alluredir=target/allure-results
                '''
            }
        }
    }
    post {
        always {
            echo 'Generating Allure report...'
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
            sh '''
            #!/bin/bash
            rm -rf venv allure.zip
            '''
        }
    }
}
