pipeline {
    agent any

    stages {

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t oop-simulator .'
            }
        }

        stage('Stop Old Container') {
            steps {
                bat 'docker stop oop-container || exit 0'
                bat 'docker rm oop-container || exit 0'
            }
        }

        stage('Run Container') {
            steps {
                bat 'docker run -d -p 5002:5000 --name oop-container oop-simulator'
            }
        }
    }
}