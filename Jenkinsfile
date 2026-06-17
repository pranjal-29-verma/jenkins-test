pipeline {
  agent any
  environment {
    IMAGE_NAME = "jenkins-test-app"
    CONTAINER_NAME = "jenkins-test-container-${env.BUILD_NUMBER}"
    HEALTH_URL = "http://localhost:8002/health/"
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

docker run -d --name "${CONTAINER_NAME}" -p 8002:8000 "${IMAGE_NAME}:${BUILD_NUMBER}"
'''
      }
    }
    stage('Test health API') {
      steps {
        sh '''#!/bin/bash
set -e

for i in $(seq 1 20); do
  if curl -sSf "${HEALTH_URL}" | grep -q '"status": *"ok"'; then
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
