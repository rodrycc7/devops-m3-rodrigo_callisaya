# Autor: Rodrigo Callisaya Cameo
variable "aws_region" {
  description = "Región de AWS donde se desplegará la infraestructura"
  type        = string
  default     = "sa-east-1"
}

variable "aws_access_key" {
  description = "AWS Access Key ID (o usar variable de entorno AWS_ACCESS_KEY_ID)"
  type        = string
  sensitive   = true
  default     = null
}

variable "aws_secret_key" {
  description = "AWS Secret Access Key (o usar variable de entorno AWS_SECRET_ACCESS_KEY)"
  type        = string
  sensitive   = true
  default     = null
}

variable "project_name" {
  description = "Prefijo para nombrar los recursos"
  type        = string
  default     = "switch-inventory"
}

variable "instance_type" {
  description = "Tipo de instancia EC2"
  type        = string
  default     = "t3.micro"
}

variable "app_port" {
  description = "Puerto en el que escucha la aplicación"
  type        = number
  default     = 8080
}

variable "allowed_ssh_cidr" {
  description = "CIDR autorizado para SSH (restringir a tu IP, ej. 190.1.2.3/32)"
  type        = string
  default     = "0.0.0.0/0"
}

variable "public_key_path" {
  description = "Ruta a la llave pública SSH que se registrará en AWS"
  type        = string
  default     = "~/.ssh/id_rsa.pub"
}

variable "private_key_path" {
  description = "Ruta a la llave privada SSH (se escribe en el inventario de Ansible)"
  type        = string
  default     = "~/.ssh/id_rsa"
}
