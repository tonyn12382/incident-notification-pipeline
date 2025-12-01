pipeline {
    agent any
    stages {
        stage('Install dependencies') {
            steps {
                sh 'python3 -m pip install -r requirements.txt'
            }
        }
        stage('Run tests') {
            steps {
                sh 'pytest test_calc.py'
            }
        }
        stage('Notify') {
            steps {
                sh 'python3 notify.py'
            }
        }
    }
}

