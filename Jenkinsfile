pipeline {
    agent any

    parameters {
        string(name: 'EXECUTOR', defaultValue: 'selenoid',
               description: 'Хост Selenoid, например selenoid или localhost')
        string(name: 'APP_URL', defaultValue: 'http://prestashop',
               description: 'Адрес тестируемого приложения PrestaShop')
        choice(name: 'BROWSER', choices: ['chrome', 'firefox'],
               description: 'Браузер в Selenoid')
        string(name: 'BROWSER_VERSION', defaultValue: '120.0',
               description: 'Версия браузера в Selenoid')
        string(name: 'THREADS', defaultValue: '1',
               description: 'Количество параллельных потоков pytest-xdist')
    }

    stages {
        stage('Окружение') {
            steps {
                sh '''
                    docker version --format 'Docker {{.Server.Version}}'
                    docker network inspect selenoid --format 'network {{.Name}}'
                '''
            }
        }

        stage('Сборка образа тестов') {
            steps {
                sh "docker build --tag prestashop-tests:${BUILD_NUMBER} ."
            }
        }

        stage('Прогон тестов') {
            steps {
                // The tests image declares ENTRYPOINT ["pytest", "--headless"],
                // so the options below are passed straight to pytest.
                sh """
                    set +e
                    container="prestashop-tests-${BUILD_NUMBER}"
                    docker rm -f "\$container" > /dev/null 2>&1
                    docker run --name "\$container" --network selenoid \
                        "prestashop-tests:${BUILD_NUMBER}" \
                        --url "${params.APP_URL}" \
                        --executor "${params.EXECUTOR}" \
                        --browser "${params.BROWSER}" \
                        --browser_version "${params.BROWSER_VERSION}" \
                        -n "${params.THREADS}"
                    status=\$?
                    docker cp "\$container:/tests/allure-results" allure-results
                    docker cp "\$container:/tests/automation.log" automation.log || true
                    docker rm -f "\$container" > /dev/null
                    exit \$status
                """
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'automation.log', allowEmptyArchive: true
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
        }
        cleanup {
            sh "docker image rm -f prestashop-tests:${BUILD_NUMBER} || true"
        }
    }
}
