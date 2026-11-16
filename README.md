# 🎮 Inventario de juegos de Nintendo Switch — Terraform + Ansible (AWS)

**Autor:** Rodrigo Callisaya Cameo ([@roddrycc7](https://github.com/roddrycc7))
**Curso:** DevOps — Módulo 3: Infraestructura como Código y CI/CD Avanzado (Educomser)
**Docente:** Lic. Rubén Gonzalo Soria Soria
**Examen:** Despliegue de aplicación con Terraform y Ansible

API REST en **Flask** para gestionar el inventario de una tienda de juegos de Nintendo Switch.
La infraestructura se define con **Terraform**
El servicio se despliega con **Ansible**
**Jenkinsfile** que automatiza el flujo completo.

## Estructura

```
project/
├── app/                 # API Flask + pruebas unitarias
│   ├── main.py
│   ├── requirements.txt
│   └── tests/test_basic.py
├── terraform/           # Infraestructura AWS
│   ├── main.tf
│   └── variables.tf
├── ansible/             # Configuración y despliegue
│   ├── inventory        # Lo genera Terraform con la IP real
│   └── playbook.yml
└── Jenkinsfile
```

## Requisitos

Python 3.10+, Terraform >= 1.5, Ansible >= 2.14, una llave SSH
(`ssh-keygen -t rsa -b 4096`) y credenciales de AWS.

## 1. Ejecutar y probar la aplicación en local

```bash
cd app
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest tests/ -v                      # pruebas unitarias
python main.py                        # http://localhost:8080

curl localhost:8080/health
curl localhost:8080/games
curl "localhost:8080/games?genre=Carreras"
curl -X POST localhost:8080/games -H "Content-Type: application/json" \
     -d '{"title":"Metroid Dread","genre":"Acción","price":49.99,"stock":6}'
curl -X PUT localhost:8080/games/1/stock -H "Content-Type: application/json" -d '{"stock":20}'
```

## 2. Terraform (variables de región y credenciales)

Opción A — archivo de variables:

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars   # editar con sus datos
terraform init
terraform validate
terraform plan
terraform apply
```

Opción B — variables de entorno:

```bash
export TF_VAR_aws_region="sa-east-1"
export TF_VAR_aws_access_key="AKIA..."
export TF_VAR_aws_secret_key="..."
terraform init && terraform apply -auto-approve
```

Al terminar, Terraform muestra `public_ip` y `app_url`, y genera `ansible/inventory`
con la IP del servidor.

## 3. Ansible

```bash
cd ../ansible
ansible all -i inventory -m ping
ansible-playbook -i inventory playbook.yml
```

Verificar el despliegue:

```bash
curl http://<public_ip>:8080/health
curl http://<public_ip>:8080/games
```

## 4. Destruir la infraestructura

```bash
cd terraform && terraform destroy
```

## Jenkins

Pipeline desde SCM apuntando a este repositorio, con las credenciales (tipo *Secret text*)
`aws-access-key-id` y `aws-secret-access-key`. Etapas: Test → Terraform Plan →
Aprobación → Terraform Apply → Ansible Deploy.
