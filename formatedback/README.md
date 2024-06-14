# CarListing_Backend

This is a Django application for managing and searching car listings. The project is structured to provide a comprehensive set of features for handling car information, including detailed car specifications, user management, and search functionalities. This is only a small part of the project, which can be expanded, supplemented, improved, you can use it as you like, customize it and much more.

Just practicing with Django.

## Features

- **Car Listings**: Add, update, delete, and view car listings with detailed specifications.
- **User Management**: Custom user model with JWT authentication.
- **Search Functionality**: Advanced search capabilities to filter cars by various criteria.
- **Admin Interface**: Custom admin interface for managing cars and related information.

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/kinworkit/yourrepository.git
    cd yourrepository
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations:**
    ```bash
    python manage.py migrate
    ```

5. **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

## Usage

### Admin Panel

Access the Django admin panel to manage car listings and user accounts at `http://127.0.0.1:8000/admin/`.

### API Endpoints

The application provides several API endpoints for interacting with the car listings and search functionality.

- **List all cars**: `GET /cars/`
- **Retrieve a specific car**: `GET /cars/<int:pk>/`
- **Search cars**: `GET /cars/search/`
- **List car marks**: `GET /marks/`
- **List car models**: `GET /models/`
- **List car years**: `GET /years/`
- **List transmission types**: `GET /kpps/`

### Example Requests

To search for cars based on criteria:
```http
GET /cars/search/?mark=Toyota&model=Camry&year=2020&city=NewYork
