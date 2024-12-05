pipeline {
    agent any
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
        environment {
            VENV_PATH = 'venv/bin'
        }
        stage('Create Virtual Environment') {
            steps {
                sh '''
                #!/bin/bash
                python3 -m venv venv
                '''
            }
        }
        stage('Install Dependencies') {
            steps {
                sh '''
                #!/bin/bash
                $VENV_PATH/pip install -r requirements.txt
                '''
            }
        }
        stage('Run flake') {
            steps {
                sh 'flacke8 .'
            }
        }
        stage('Run Backend Tests') {
            when {
                expression { env.BACKEND_CHANGED == 'true' }
            }
            steps {
                sh '''
                #!/bin/bash
                $VENV_PATH/pytest backend --alluredir=target/allure-results
                '''
            }
        }
        stage('Run UI Tests') {
            when {
                expression { env.UI_CHANGED == 'true' }
            }
            steps {
                sh '''
                #!/bin/bash
                $VENV_PATH/pytest frontend --alluredir=target/allure-results
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
