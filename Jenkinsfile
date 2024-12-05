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

            sh '''
            #!/bin/bash
            allure generate target/allure-results --clean -o target/allure-report
            '''
            echo 'Allure report generated at target/allure-report'
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
