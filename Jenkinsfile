pipeline {
  agent {
    docker {
      image 'jenkins-agent:latest'
      args '-u root -v /var/run/docker.sock:/var/run/docker.sock --network jenkins-net'
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

docker rm -f "${CONTAINER_NAME}" >/dev/null 2>&1 || true

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
      sh 'docker image prune -f'
      sh 'docker rmi ${IMAGE_NAME}:${BUILD_NUMBER} || true'
    }
  }
}
