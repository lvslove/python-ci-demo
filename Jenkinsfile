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
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        tage('Run flake') {
            steps {
                sh 'flacke8 .'
            }
        }
        stage('Run Backend Tests') {
            when {
                expression { env.BACKEND_CHANGED == 'true' }
            }
            steps {
                sh 'pytest backend --alluredir=allure-results'
            }
        }
        stage('Run UI Tests') {
            when {
                expression { env.UI_CHANGED == 'true' }
            }
            steps {
                sh 'pytest frontend --alluredir=allure-results'
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
