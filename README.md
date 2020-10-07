<h1 align="center">
  <a href="https://github.com/WesGtoX/medicar">
    <img src=".github/logo.png" alt="Medicar" title="Medicar" width="300px">
  </a>
  <br />
  <img alt="Medicar CI" src="https://github.com/WesGtoX/medicar/workflows/Medicar%20CI/badge.svg" />
</h1>

<p align="center">
  <a href="#about-the-project">About</a>&nbsp;&nbsp;|&nbsp;&nbsp;
  <a href="#technology">Technology</a>&nbsp;&nbsp;|&nbsp;&nbsp;
  <a href="#layout">Layout</a>&nbsp;&nbsp;|&nbsp;&nbsp;
  <a href="#getting-started">Getting Started</a>&nbsp;&nbsp;|&nbsp;&nbsp;
  <a href="#usage">Usage</a>&nbsp;&nbsp;|&nbsp;&nbsp;
  <a href="#license">License</a>
</p>

<p align="center">
  <img alt="GitHub top language" src="https://img.shields.io/github/languages/top/wesgtox/medicar?style=plastic" />
  <img alt="GitHub language count" src="https://img.shields.io/github/languages/count/wesgtox/medicar?style=plastic" />
  <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/wesgtox/medicar?style=plastic" />
  <img alt="GitHub issues" src="https://img.shields.io/github/issues/wesgtox/medicar?style=plastic" />
  <img alt="License" src="https://img.shields.io/github/license/wesgtox/medicar?style=plastic" />
</p>


# Medicar

Platform for registering and managing medical appointments and schedules.


## About the Project

### Medicar Back-end

- Administrative system for managing:
  - Medical specialties
  - Doctors
  - Medical agenda
  - Medical appointment

- API Restfull for:
  - Creation:
    - Medical appointment

  - Listing:
    - Medical specialties
    - Doctors
    - Medical agenda
    - Medical appointment

  - Details:
    - Medical specialties
    - Doctors
    - Medical agenda

  - Removal:
    - Medical appointment

### Medicar Front-end

- Application login and logout
- List of authenticated user's medical appointments
- Make an appointment for a doctor
- Unmark a doctor's appointment
- Routes:

  | Routes       | Description         |
  | ------------ | ------------------- |
  | `/login`     | Login page          |
  | ` /register` | Register a user     |
  | `/home`      | Home page           |
  | `/create`    | Make an appointment |


## Technology 

This project was developed with the following technologies:

- [Python](https://www.python.org/)
- [Django Framework](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)


## Layout

You can view the project layout in the format through this [LINK](https://www.figma.com/file/HAx6cnob0U2Za7LYZN1cVK/Desafio-Full-Stack-Intmed?node-id=0%3A1).  
Remembering that you will need to have an account at [Figma](http://figma.com/).  

## Getting Started

### Prerequisites

- [Python](https://www.python.org/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)


### Install and Run the API

1. Clone the repository:
```bash
git clone https://github.com/WesGtoX/medicar.git
```
2. Set a `SECRET_KEY` in `.env`:
```bash
cp backend/.env.sample backend/.env
```
3. Build
```bash
make build
```
4. Run:
```bash
make run
```
4. Run tests:
```bash
make test
```


## Usage

### Endpoints

### Auth Token

| Method | Endpoint           | Description          |
| :----: | ------------------ | -------------------- |
| `POST` | `/api-token-auth/` | User authentication. |

#### Especialidades

| Method | Endpoint              | Description                              |
| :----: | --------------------- | ---------------------------------------- |
| `GET`  | `/especialidades/`    | List all registered specialties.         |
| `GET`  | `/especialidades/:id` | Show the detail of a specific specialty. |

#### Médicos

| Method | Endpoint       | Description                           |
| :----: | -------------- | ------------------------------------- |
| `GET`  | `/medicos/`    | List all registered doctors.          |
| `GET`  | `/medicos/:id` | Show the detail of a specific doctor. |

#### Agendas
| Method | Endpoint       | Description                           |
| :----: | -------------- | ------------------------------------- |
| `GET`  | `/agendas/`    | List all registered agendas.          |
| `GET`  | `/agendas/:id` | Show the detail of a specific agenda. |

#### Consultas
|  Method  | Endpoint         | Description                              |
| :------: | ---------------- | ---------------------------------------- |
|  `POST`  | `/consultas/`    | Register a medical appointment.          |
|  `GET`   | `/consultas/`    | List all registered medical appointment. |
| `DELETE` | `/consultas/:id` | Remove a specific medical appointment.   |

_For more examples, please refer to the [Documentation](https://github.com/WesGtoX/medicar/wiki)_


## License

Distributed under the MIT License. See [LICENSE](LICENSE.md) for more information.

---

Made with ♥ by [Wesley Mendes](https://wesleymendes.com.br/) :wave:
