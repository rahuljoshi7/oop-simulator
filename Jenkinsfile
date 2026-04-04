pipeline {
    agent any

    stages {

        stage('Clone Code') {
            steps {
                git branch: 'main', url: 'https://github.com/rahuljoshi7/oop-simulator.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t oop-simulator .'
            }
        }

        stage('Stop Old Container') {
            steps {
                sh 'docker stop oop-container || true'
                sh 'docker rm oop-container || true'
            }
        }

        stage('Run Container') {
            steps {
                sh 'docker run -d -p 5002:5000 --name oop-container oop-simulator'
            }
        }
    }
}
