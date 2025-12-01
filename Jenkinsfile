pipeline {
    agent {
        docker {
            image 'python:3.11'   // Official Python image from Docker Hub
        }
    }
    stages {
        stage('Install dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Run tests') {
            steps {
                sh 'pytest test_calc.py'
            }
        }
        stage('Notify') {
            steps {
                sh 'python notify.py'
            }
        }
    }
}
