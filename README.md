
# Spy Cat Agency Management System

This project is a RESTful API designed for managing spy cats, their missions, and targets. Built with Django and Django REST Framework, it provides all necessary endpoints to handle CRUD operations for cats and missions.

---

## Features

- **Spy Cats Management**:
  - Add, view, update, and delete spy cats.
  - Validate cat breeds using [TheCatAPI](https://thecatapi.com/).

- **Mission and Target Management**:
  - Create missions with associated targets.
  - Assign missions to cats.
  - Mark targets and missions as completed.
  - Update and view notes for targets.

- **Robust Validation**:
  - Missions can only have between 1 and 3 targets.
  - Prevent updates to completed targets or missions with assigned cats.

---

## Installation

Follow these steps to set up the application locally:

### 1. Clone the repository

```bash
git clone https://github.com/Chelakhovl/the-Spy-Cat-Agency.git
```

### 2. Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root with the following content:

```
DEBUG=True
SECRET_KEY=<your_django_secret_key>
DATABASE_URL=postgres://<user>:<password>@<host>:<port>/<database>
THE_CAT_API_URL=https://api.thecatapi.com/v1/breeds/search
```

### 5. Set up the database

```bash
python manage.py migrate
```

### 6. Run the server

```bash
python manage.py runserver
```

---

## API Endpoints

### Spy Cats
| Endpoint            | Method  | Description                 |
|---------------------|---------|-----------------------------|
| `/api/cats/`        | GET     | List all spy cats.          |
| `/api/cats/<id>/`   | GET     | Retrieve a single spy cat.  |
| `/api/cats/`        | POST    | Create a new spy cat.       |
| `/api/cats/<id>/`   | PATCH   | Update a spy cat's salary.  |
| `/api/cats/<id>/`   | DELETE  | Delete a spy cat.           |

### Missions
| Endpoint                  | Method  | Description                        |
|---------------------------|---------|------------------------------------|
| `/api/missions/`          | GET     | List all missions.                 |
| `/api/missions/<id>/`     | GET     | Retrieve a single mission.         |
| `/api/missions/`          | POST    | Create a new mission with targets. |
| `/api/missions/<id>/`     | PATCH   | Update mission details or targets. |
| `/api/missions/<id>/`     | DELETE  | Delete a mission.                  |
| `/api/missions/<id>/complete_target/` | PATCH | Mark a target as completed.      |

---

## Examples

### Create a Spy Cat
**Request**:
```json
POST /api/cats/
{
  "name": "Agent Whiskers",
  "years_of_experience": 3,
  "breed": "Maine Coon",
  "salary": "5000.00"
}
```

**Response**:
```json
{
  "id": 1,
  "name": "Agent Whiskers",
  "years_of_experience": 3,
  "breed": "Maine Coon",
  "salary": "5000.00"
}
```

### Create a Mission with Targets
**Request**:
```json
POST /api/missions/
{
  "cat": 1,
  "status": false,
  "targets": [
    {"title": "Target Alpha", "country": "USA", "notes": "Observation 1"},
    {"title": "Target Beta", "country": "UK", "notes": "Observation 2"}
  ]
}
```

**Response**:
```json
{
  "id": 1,
  "cat": 1,
  "status": false,
  "targets": [
    {"id": 1, "title": "Target Alpha", "country": "USA", "notes": "Observation 1", "is_completed": false},
    {"id": 2, "title": "Target Beta", "country": "UK", "notes": "Observation 2", "is_completed": false}
  ]
}
```

---

## Running Tests

Run the following command to execute the test suite:

```bash
python manage.py test
```
---

## Future Improvements

- **Authentication**: Implement user authentication and authorization.
- **UI Integration**: Add a frontend interface for better usability.
- **Advanced Analytics**: Provide reports on mission performance and spy cat efficiency.

## Postman Collection
https://spy-cat.postman.co/workspace/Spy-cat-Workspace~655a0ad5-4471-457e-b3ee-6d29991ab1ca/collection/33495085-020f6154-397e-4f0a-bc0d-e3d592058538?action=share&creator=33495085
