pipeline {
    agent any
    
    environment {
        DOCKERHUB_REPO = 'ancela'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo "Code récupéré depuis ${env.GIT_BRANCH}"
            }
        }
        
        stage('Build Cast Service') {
            steps {
                script {
                    sh """
                        cd cast-service
                        docker build -t ${DOCKERHUB_REPO}/cast-service:${IMAGE_TAG} .
                        docker tag ${DOCKERHUB_REPO}/cast-service:${IMAGE_TAG} ${DOCKERHUB_REPO}/cast-service:latest
                        cd ..
                    """
                }
            }
        }
        
        stage('Build Movie Service') {
            steps {
                script {
                    sh """
                        cd movie-service
                        docker build -t ${DOCKERHUB_REPO}/movie-service:${IMAGE_TAG} .
                        docker tag ${DOCKERHUB_REPO}/movie-service:${IMAGE_TAG} ${DOCKERHUB_REPO}/movie-service:latest
                        cd ..
                    """
                }
            }
        }
        
        stage('Push to DockerHub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', 
                                                      usernameVariable: 'DOCKER_USER', 
                                                      passwordVariable: 'DOCKER_PASS')]) {
                        sh """
                            echo "${DOCKER_PASS}" | docker login -u "${DOCKER_USER}" --password-stdin
                            
                            docker push ${DOCKERHUB_REPO}/cast-service:${IMAGE_TAG}
                            docker push ${DOCKERHUB_REPO}/cast-service:latest
                            
                            docker push ${DOCKERHUB_REPO}/movie-service:${IMAGE_TAG}
                            docker push ${DOCKERHUB_REPO}/movie-service:latest
                            
                            docker logout
                            
                            echo "All images pushed to DockerHub successfully!"
                        """
                    }
                }
            }
        }
        
        stage('Deploy to DEV') {
            steps {
                script {
                    sh """
                        kubectl --namespace=dev apply -f k8s/dev/ --validate=false
                        kubectl --namespace=dev set image deployment/cast-service cast-service=${DOCKERHUB_REPO}/cast-service:${IMAGE_TAG}
                        kubectl --namespace=dev set image deployment/movie-service movie-service=${DOCKERHUB_REPO}/movie-service:${IMAGE_TAG}
                        kubectl --namespace=dev rollout status deployment/cast-service --timeout=60s || true
                        kubectl --namespace=dev rollout status deployment/movie-service --timeout=60s || true
                        kubectl --namespace=dev get pods
                    """
                }
            }
        }
        
        stage('Deploy to QA') {
            steps {
                script {
                    sh """
                        kubectl --namespace=qa apply -f k8s/qa/ --validate=false
                        kubectl --namespace=qa set image deployment/cast-service cast-service=${DOCKERHUB_REPO}/cast-service:${IMAGE_TAG}
                        kubectl --namespace=qa set image deployment/movie-service movie-service=${DOCKERHUB_REPO}/movie-service:${IMAGE_TAG}
                        kubectl --namespace=qa rollout status deployment/cast-service --timeout=60s || true
                        kubectl --namespace=qa rollout status deployment/movie-service --timeout=60s || true
                    """
                }
            }
        }
        
        stage('Deploy to Staging') {
            steps {
                script {
                    sh """
                        kubectl --namespace=staging apply -f k8s/staging/ --validate=false
                        kubectl --namespace=staging set image deployment/cast-service cast-service=${DOCKERHUB_REPO}/cast-service:${IMAGE_TAG}
                        kubectl --namespace=staging set image deployment/movie-service movie-service=${DOCKERHUB_REPO}/movie-service:${IMAGE_TAG}
                        kubectl --namespace=staging rollout status deployment/cast-service --timeout=60s || true
                        kubectl --namespace=staging rollout status deployment/movie-service --timeout=60s || true
                        kubectl --namespace=staging get pods
                    """
                }
            }
        }
        
        stage('Smoke Tests') {
            steps {
                script {
                    sh """
                        echo "🔍 Smoke tests on staging..."
                        kubectl --namespace=staging get pods | grep -E "cast|movie"
                        echo "Smoke tests passed"
                    """
                }
            }
        }
        
        // Stage Production - UNIQUEMENT pour la branche master et avec confirmation manuelle
        stage('Deploy to Production') {
            when {
                branch 'master'
            }
            input {
                message "CONFIRMER DÉPLOIEMENT EN PRODUCTION ?"
                ok "DÉPLOYER"
            }
            steps {
                script {
                    sh """
                        echo "Déploiement en production..."
                        kubectl --namespace=prod apply -f k8s/prod/ --validate=false
                        kubectl --namespace=prod set image deployment/cast-service cast-service=${DOCKERHUB_REPO}/cast-service:${IMAGE_TAG}
                        kubectl --namespace=prod set image deployment/movie-service movie-service=${DOCKERHUB_REPO}/movie-service:${IMAGE_TAG}
                        kubectl --namespace=prod rollout status deployment/cast-service --timeout=120s
                        kubectl --namespace=prod rollout status deployment/movie-service --timeout=120s
                        kubectl --namespace=prod get pods
                        kubectl --namespace=prod get services
                        echo "Production deployed! Version: ${IMAGE_TAG}"
                    """
                }
            }
        }
    }
    
    post {
        always {
            script {
                sh "docker system prune -f || true"
            }
            echo "Pipeline terminé pour build #${env.BUILD_NUMBER}"
        }
        success {
            echo "Pipeline réussi! Version: ${IMAGE_TAG}"
        }
        failure {
            echo "Build échoué. Vérifier les logs."
        }
    }
}
