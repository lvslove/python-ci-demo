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
                echo "Downloading Allure CLI..."
                curl -L -o allure.zip https://github.com/allure-framework/allure2/releases/latest/download/allure-commandline.zip
                
                # Проверяем, успешно ли скачан архив
                if [ $? -ne 0 ] || [ ! -f allure.zip ]; then
                    echo "Failed to download Allure CLI. Exiting."
                    exit 1
                fi

                echo "Unzipping Allure CLI..."
                unzip -o allure.zip -d allure
                
                # Проверяем успешность распаковки
                if [ $? -ne 0 ]; then
                    echo "Failed to unzip Allure CLI. Exiting."
                    exit 1
                fi

                export PATH=$PATH:$PWD/allure/bin
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
