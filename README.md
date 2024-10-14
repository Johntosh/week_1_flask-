# Superheroes API

The **Superheroes API** is a RESTful service built using Flask, SQLAlchemy, and Flask-Migrate. The API allows you to manage superheroes, their superpowers, and the associations between them. It provides endpoints to create, retrieve, update, and manage superheroes and their powers, alongside relational data between heroes and their powers.

## Table of Contents

- [Superheroes API](#superheroes-api)
  - [Table of Contents](#table-of-contents)
  - [Project Overview](#project-overview)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Installation and Setup](#installation-and-setup)
  - [Database Migrations](#database-migrations)
  - [Seeding the Database](#seeding-the-database)
  - [Running the Application](#running-the-application)
  - [API Endpoints](#api-endpoints)
    - [GET /](#get)
    - [GET /heroes](#get-heroes)
    - [GET `/heroes/:id`](#get-heroesid)
    - [GET /powers](#get-powers)
    - [GET/PATCH /powers/:id](#getpatch-powersid)
    - [POST /hero\_powers](#post-hero_powers)
  - [License](#license)

---

## Project Overview

This API is designed to manage superheroes, their powers, and the relationships between them. The API supports CRUD operations for both superheroes and powers, and it enables linking heroes to specific powers with an associated strength level. The project uses Flask for the web framework and SQLAlchemy as the ORM to manage the database.

---

## Features

- CRUD operations for heroes and powers
- Linking heroes to powers with strength levels (e.g., Strong, Weak, Average)
- Database migration using Flask-Migrate and Alembic
- Automatic serialization of models using SQLAlchemy-Serializer
- Error handling and validation for input data

---

## Prerequisites

Before you begin, make sure you have the following installed:

- Python 3.10 or higher
- SQLite (for local development)

---

## Installation and Setup

Follow these steps to set up the project on your local machine:

1. **Clone the repository**:

   ```bash
   git clone git@github.com:Johntosh/week_1_flask-.git
   cd week_1_flask
   ```

2. **Create a virtual environment**:

   ```bash
   pipenv shell
   ```

3. **Install dependencies using Pipenv**:
   If you're using `pipenv`, install the dependencies:

   ```bash
   pipenv install --dev
   ```
    The `dev` flag is used to ensure development dependencies are also installed

---

## Database Migrations

To set up the database, you need to run the migrations from the `server` directory:

1. **Change into the server directory**:

   ```bash
   cd server
   ```

2. **Initialize the database and run migrations**:

   ```bash
   flask db upgrade
   ```

This will create the necessary tables in the SQLite database (`app.db`), such as `heroes`, `powers`, and `heroes_powers`.

---

## Seeding the Database

Once the database is set up, you can seed it with initial data using the `seed.py` script:

1. **Run the seed script**:

   ```bash
   python seed.py
   ```

This script populates the database with some initial superhero and power records, allowing you to interact with the API right away.

---

## Running the Application

To run the Flask development server, use the following command from the `server` directory:

```bash
python app.py
```

By default, the server will start at `http://127.0.0.1:5555/`. You can test the API endpoints using Postman, cURL, or a similar tool.

---

## API Endpoints

Here is a detailed description of each endpoint provided by the API:

### GET /

**Description**:  
This is the root endpoint of the API. It simply returns a message indicating that the API is live.

- **URL**: `/`
- **Method**: `GET`
- **Response**:

  ```json
  "Superheroes API"
  ```

### GET /heroes

**Description**:  
Retrieve a list of all superheroes in the database. Each hero's basic information, such as their name and super_name, is included in the response.

- **URL**: `/heroes`
- **Method**: `GET`
- **Response**:
  Returns a list of heroes:

  ```json
  [
    {
      "id": 1,
      "name": "Kamala Khan",
      "super_name": "Ms. Marvel"
    },
    ...
  ]
  ```

### GET /heroes/:id

**Description**:  
Retrieve a single superhero by their `id`. If the hero does not exist, the endpoint will return a `404` error.

- **URL**: `/heroes/:id`
- **Method**: `GET`
- **Response**:
  Returns the hero's details:

  ```json
  {
    "id": 1,
    "name": "Kamala Khan",
    "super_name": "Ms. Marvel"
  }
  ```

### GET /powers

**Description**:  
Retrieve a list of all superpowers. Each power has a name and description. This endpoint helps you see the available powers to assign to heroes.

- **URL**: `/powers`
- **Method**: `GET`
- **Response**:
  Returns a list of powers:

  ```json
  [
    {
      "id": 1,
      "name": "super strength",
      "description": "gives the wielder super-human strengths"
    },
    ...
  ]
  ```

### GET/PATCH /powers/:id

**Description**:  
This endpoint has two operations:

- **GET**: Retrieve a specific power by its `id`.
- **PATCH**: Update an existing power by sending a partial update to its description or name.

- **URL**: `/powers/:id`
- **Method**: `GET`, `PATCH`
- **Response (GET)**:

  ```json
  {
    "id": 1,
    "name": "super strength",
    "description": "gives the wielder super-human strengths"
  }
  ```

- **Response (PATCH)**:
  After successfully updating a power:

  ```json
  {
    "id": 1,
    "name": "super strength",
    "description": "new description for the power"
  }
  ```

### POST /hero_powers

**Description**:  
Create a new relationship between a hero and a power, with an associated strength level. You must provide the hero's ID, power's ID, and the strength.

- **URL**: `/hero_powers`
- **Method**: `POST`
- **Request Body**:

  ```json
  {
    "hero_id": 1,
    "power_id": 2,
    "strength": "Strong"
  }
  ```

- **Response**:
  Returns the newly created hero-power relationship:

  ```json
  {
    "id": 1,
    "hero_id": 1,
    "power_id": 2,
    "strength": "Strong"
  }
  ```

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
