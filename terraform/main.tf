# Autor: Rodrigo Callisaya Cameo - Infraestructura del inventario de juegos Nintendo Switch
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}

provider "aws" {
  region     = var.aws_region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

# VPC por defecto (simplifica el examen)
data "aws_vpc" "default" {
  default = true
}

# Última AMI de Ubuntu 22.04 LTS (Canonical)
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

resource "aws_key_pair" "deployer" {
  key_name   = "${var.project_name}-key"
  public_key = file(pathexpand(var.public_key_path))
}

resource "aws_security_group" "app" {
  name        = "${var.project_name}-sg"
  description = "Permite SSH y trafico a la aplicacion"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.allowed_ssh_cidr]
  }

  ingress {
    description = "Aplicacion"
    from_port   = var.app_port
    to_port     = var.app_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-sg"
  }
}

resource "aws_instance" "app" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  key_name               = aws_key_pair.deployer.key_name
  vpc_security_group_ids = [aws_security_group.app.id]

  tags = {
    Name = "${var.project_name}-server"
  }
}

# Genera automáticamente el inventario de Ansible con la IP creada
resource "local_file" "ansible_inventory" {
  filename        = "${path.module}/../ansible/inventory"
  file_permission = "0644"
  content         = <<-EOT
    [app]
    ${aws_instance.app.public_ip}

    [app:vars]
    ansible_user=ubuntu
    ansible_ssh_private_key_file=${pathexpand(var.private_key_path)}
    ansible_ssh_common_args='-o StrictHostKeyChecking=no'
    app_port=${var.app_port}
  EOT
}

output "public_ip" {
  description = "IP pública del servidor"
  value       = aws_instance.app.public_ip
}

output "app_url" {
  description = "URL de la aplicación"
  value       = "http://${aws_instance.app.public_ip}:${var.app_port}/health"
}
