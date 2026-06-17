pipeline {
  agent {
    docker {
      image 'python:3.11-slim'  // use whatever base your app needs
      args '--network jenkins-net'  // so it can reach your app container
    }
  }
  environment {
    IMAGE_NAME = "jenkins-test-app"
    CONTAINER_NAME = "jenkins-test-container-${env.BUILD_NUMBER}"
  }
  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }
    stage('Build Docker image') {
      steps {
        sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .'
      }
    }
    stage('Run container') {
      steps {
        sh '''#!/bin/bash
set -e

docker network create jenkins-net || true
docker network connect jenkins-net jenkins || true

docker run -d \
    --name "${CONTAINER_NAME}" \
    --network jenkins-net \
    "${IMAGE_NAME}:${BUILD_NUMBER}"
'''
      }
    }
    stage('Test health API') {
      steps {
        sh '''#!/bin/bash
set -e

for i in $(seq 1 20); do
  if curl -sSf "http://${CONTAINER_NAME}:8000/health/" | grep -q '"status": *"ok"'; then
    echo "Health check passed"
    exit 0
  fi
  echo "Waiting for app readiness ($i/20)..."
  sleep 2
done

echo "ERROR: Health endpoint did not respond with expected payload"
docker logs "${CONTAINER_NAME}"
exit 1
'''
      }
    }
  }
  post {
    always {
      sh 'docker rm -f "${CONTAINER_NAME}" || true'
    }
  }
}