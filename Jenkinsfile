pipeline {
    agent {
        kubernetes {
            yaml '''
                apiVersion: v1
                kind: Pod
                spec:
                    containers:
                    - name: python-container
                      image: python:3.10-alpine
            '''
        }

    }
    stages {
        stage('Install Dependencies') {
            steps {
                sh 'python3.10 -m pip install -r requirements.txt'
            }
        }

        stage('Build') {
            steps {
                sh 'python -m py_compile custom_parser.py resize.py'
                stash(name: 'parser-source', includes: 'custom_parser.py')
                stash(name: 'resize-source', includes: 'resize.py')
                stash(name: 'compiled-results', includes: './*.pyc')
            }
        }


    }
}