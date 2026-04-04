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
                bat 'docker build -t oop-simulator .'
            }
        }

        stage('Stop Old Container') {
            steps {
                bat 'docker stop oop-container || true'
                bat 'docker rm oop-container || true'
            }
        }

        stage('Run Container') {
            steps {
                bat 'docker run -d -p 5002:5000 --name oop-container oop-simulator'
            }
        }
    }
}