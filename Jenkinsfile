// Autor: Rodrigo Callisaya Cameo - Pipeline del inventario de juegos Nintendo Switch
pipeline {
    agent any

    environment {
        // Credenciales guardadas en Jenkins (tipo "Secret text")
        TF_VAR_aws_access_key = credentials('aws-access-key-id')
        TF_VAR_aws_secret_key = credentials('aws-secret-access-key')
        TF_VAR_aws_region     = 'sa-east-1'
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Test') {
            steps {
                dir('app') {
                    sh '''
                        python3 -m venv .venv
                        . .venv/bin/activate
                        pip install -r requirements.txt
                        pytest tests/ -v
                    '''
                }
            }
        }

        stage('Terraform Plan') {
            steps {
                dir('terraform') {
                    sh 'terraform init -input=false'
                    sh 'terraform validate'
                    sh 'terraform plan -input=false -out=tfplan'
                }
            }
        }

        stage('Aprobación') {
            steps {
                input message: '¿Aplicar la infraestructura en AWS?'
            }
        }

        stage('Terraform Apply') {
            steps {
                dir('terraform') {
                    sh 'terraform apply -input=false tfplan'
                }
            }
        }

        stage('Ansible Deploy') {
            steps {
                dir('ansible') {
                    sh 'ansible-playbook -i inventory playbook.yml'
                }
            }
        }
    }

    post {
        success { echo 'Despliegue completado correctamente.' }
        failure { echo 'El pipeline falló, revise los logs.' }
    }
}
