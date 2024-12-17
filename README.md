## <div align="center">

[![Pytest Testing Suite](https://github.com/diverso-lab/uvlhub/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/diverso-lab/uvlhub/actions/workflows/tests.yml)
[![Commits Syntax Checker](https://github.com/diverso-lab/uvlhub/actions/workflows/commits.yml/badge.svg?branch=main)](https://github.com/diverso-lab/uvlhub/actions/workflows/commits.yml)

</div>

<div align="center">
  <img src="https://www.uvlhub.io/static/img/logos/logo-light.svg" alt="Logo">
</div>

## Introduction

Chicharrones-hub is a fork of the UVLHub project by DiversoLab, developed as part of the Evolution and Configuration Management (Evolución y Gestión de la Configuración - EGC) course in the Software Engineering degree program at the University of Seville.

This project serves as a repository for feature models in the UVL format, integrated with Zenodo and Flamapy. It includes various enhancements introduced by students, providing practical experience in a continuous integration and deployment environment. Participants applied best practices such as automating tests and checks with GitHub Actions while collaborating efficiently across multiple teams.

# About Chicharrones-hub

Chicharrones-hub is an organization composed of two subgroups: **chicharrones-hub-1** and **chicharrones-hub-2**.

# Chicharrones-hub-1

### Members:

| Name                       |
|----------------------------|
| Francisco Avilés Carrera |
| Lorenzo Torralba Lanzas   |
| Andrés Pizzano Cerrillos |
| Diego José Pérez Vargas |
| Francisco Pérez Manzano  |
| Alexis Molins López      |

### Work items completed:

| Work Item                  | Difficulty |
|----------------------------|------------|
| Advanced filtering         | High       |
| Download in different formats | Medium  |
| Bot integration            | High       |
| Upload from GitHub / Zip   | Medium     |
| Sign up validation         | Low        |
| View user profile          | Low        |

# Chicharrones-hub-2

### Members:

| Name                            |
|---------------------------------|
| [Ignacio Blanquero Blanco](https://github.com/ignblabla)        |
| [Adrián Cabello Martín](https://github.com/Adrcabmar)         |
| [María de la Salud Carrera Talaverón](https://github.com/maryycarrera) |
| [Antonio Montero López](https://github.com/antonio-mz)         |
| [Natalia Olmo Villegas](https://github.com/nataliaaolmo)          |
| [David Vargas Jorba](https://github.com/vDavidd)             |

### Work items completed:

| Work Item                  | Difficulty |
|----------------------------|------------|
| AI Integration             | High       |
| Download all datasets      | Medium     |
| Rate datasets              | Medium     |
| Register developer         | Low        |
| Anonymize dataset          | Low        |
| Search query               | High       |

## Project Deployment

The project is deployed and accessible at: [https://chicharrones-hub.onrender.com/](https://chicharrones-hub.onrender.com/)

## Project Wiki

You can access the project wiki at: [https://github.com/EGC-chicharrones/chicharrones-hub-1/wiki](https://github.com/EGC-chicharrones/chicharrones-hub-1/wiki)

# Getting started with Chicharrones-hub

Follow this guide to set up the project:

## 1. Clone the repository
Clone Chicharrones-hub repository by executing:

```bash
git@github.com:EGC-chicharrones/chicharrones-hub-1.git
```

in the directory of your choice. Remember to create an SSH key first.

## 2. Configure the environment
### Linux
- Install mariadb:

```bash
sudo apt install mariadb-server -y
```

- Start mariadb:

```bash
sudo systemctl start mariadb
```

- Configure MariaDB:

```bash
sudo mysql_secure_installation
```

Accept every step.

### Configure databases and users

- Configure database:

```bash
sudo mysql -u root -p
```

Use `uvlhubdb_root_password` as root password. Then execute:

```bash
CREATE DATABASE uvlhubdb;
CREATE DATABASE uvlhubdb_test;
CREATE USER 'uvlhubdb_user'@'localhost' IDENTIFIED BY 'uvlhubdb_password';
GRANT ALL PRIVILEGES ON uvlhubdb.* TO 'uvlhubdb_user'@'localhost';
GRANT ALL PRIVILEGES ON uvlhubdb_test.* TO 'uvlhubdb_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Configure app environment

- Copy environment variables:

```bash
cp .env.local.example .env
```

- Ignore webhook module:

```bash
echo "webhook" > .moduleignore
```

### Install dependencies

#### Create and activate a virtual environment

- Install virtualenv:

```bash
sudo apt install python3.12-venv
```

- In the root directory of the project you just cloned, create the virtual environment:

```bash
python3.12 -m venv venv
```

`venv` is the name of the virtual environment.

- Activate your new virtual environment:

```bash
source venv/bin/activate
```

#### Install Python dependencies

- Upgrade pip:

```bash
pip install --upgrade pip
```

- Install dependencies:

```bash
pip install -r requirements.txt
```

- Install the app in editable mode:

```bash
pip install -e ./
```

- Check that Rosemary has been installed correctly:

```bash
rosemary
```

### Run app

- Apply migrations:

```bash
flask db upgrade
```

- Populate database:

```bash
rosemary db:seed
```

- Run development Flask server:

```bash
flask run --host=0.0.0.0 --reload --debug
```

## Official documentation

You can consult the official documentation of the project at [docs.uvlhub.io](https://docs.uvlhub.io/)

