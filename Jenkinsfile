pipeline {
  agent any

  environment {
    REGISTRY = "ghcr.io"
    IMAGE    = "ghcr.io/<你的GitHub用户名>/hello-jenkins"
  }

  triggers {
    // 兜底：每5分钟轮询一次（Webhook 失效也能触发）
    pollSCM('H/5 * * * *')
  }

  options {
    timestamps()
    ansiColor('xterm')
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Unit Test (pytest)') {
      steps {
        sh """
          docker run --rm -v "\$PWD":/src -w /src python:3.11-slim \
            bash -lc 'pip install -r requirements.txt && pytest -q'
        """
      }
    }

    stage('Build Image') {
      steps {
        script {
          docker.build("${env.IMAGE}:${env.BUILD_NUMBER}")
        }
      }
    }

    stage('Push Image to GHCR') {
      steps {
        script {
          docker.withRegistry("https://${env.REGISTRY}", "ghcr") {
            sh "docker push ${env.IMAGE}:${env.BUILD_NUMBER}"
            sh "docker tag ${env.IMAGE}:${env.BUILD_NUMBER} ${env.IMAGE}:latest"
            sh "docker push ${env.IMAGE}:latest"
          }
        }
      }
    }

    stage('Deploy (local container)') {
      steps {
        sh """
          docker rm -f hello-jenkins 2>/dev/null || true
          docker run -d --name hello-jenkins -p 8000:5000 ${env.IMAGE}:latest
        """
      }
    }

    stage('Smoke Check') {
      steps {
        sh 'sleep 2 && curl -fsS http://localhost:8000/ | grep -q "Hello"'
      }
    }
  }

  post {
    always  { echo "Build URL: ${env.BUILD_URL}" }
    failure { echo "Build failed. Check console output." }
  }
}
