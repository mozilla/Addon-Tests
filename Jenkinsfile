@Library('fxtest@1.6') _

/** Desired capabilities */
def capabilities = [
  browserName: 'Firefox',
  version: '47.0',
  platform: 'Windows 10'
]

pipeline {
  agent any
  options {
    ansiColor('xterm')
    timestamps()
    timeout(time: 1, unit: 'HOURS')
  }
  environment {
    /* See https://issues.jenkins-ci.org/browse/JENKINS-43872 - credentials
       variable should be usable inside the same environment block */
    VARIABLES = credentials('AMO_VARIABLES')
    PULSE = credentials('PULSE')
    SAUCELABS_API_KEY = credentials('SAUCELABS_API_KEY')
  }
  stages {
    stage('Lint') {
      steps {
        sh 'tox -e flake8'
      }
    }
    stage('Test') {
      environment {
        PYTEST_ADDOPTS =
          "--tb=short " +
          "--color=yes " +
          "--driver=SauceLabs " +
          "--variables=capabilities.json " +
          "--variables=${VARIABLES}"
      }
      steps {
        writeCapabilities(capabilities)
        sh 'tox -e py27'
      }
      post {
        always {
          archiveArtifacts 'results/*'
          junit 'results/*.xml'
          submitToActiveData('results/py27_raw.txt')
          submitToTreeherder('addon-tests', 'e2e', 'End-to-end integration tests', 'results/*', 'results/py27_tbpl.txt')
          publishHTML(target: [
            allowMissing: false,
            alwaysLinkToLastBuild: true,
            keepAll: true,
            reportDir: 'results',
            reportFiles: 'py27.html',
            reportName: 'HTML Report'])
        }
      }
    }
  }
  post {
    failure {
      mail(
        body: "${BUILD_URL}",
        from: "firefox-test-engineering@mozilla.com",
        replyTo: "firefox-test-engineering@mozilla.com",
        subject: "Build failed in Jenkins: ${JOB_NAME} #${BUILD_NUMBER}",
        to: "fte-ci@mozilla.com")
    }
    changed {
      ircNotification()
    }
  }
}
