FastAPI JWT Authentication Microservice

This FastAPI-based microservice provides JWT-based authentication for user registration, login, token verification, and refresh. The application uses two SQLite databases: one for the application endpoints and another for running tests.
Features

    JWT Authentication: Secure authentication with access and refresh tokens.
    Endpoints:
        /register: Register a new user.
        /login: Obtain access tokens.
        /token/refresh: Refresh an existing token.
        /token/verify: Verify the validity of a token.
        /logout: Log out the user.

Requirements

To run this project locally, you need to have the following installed:

    Docker
    Docker Compose

How to Run the Application
1. Clone the Repository

bash

git clone https://github.com/your-username/your-repository.git
cd your-repository

2. Build and Run the Docker Container

To build and run the application inside a Docker container, use:

bash

docker-compose up --build

The application will be available at http://0.0.0.0:8000/.
3. Access the API Documentation

You can view the auto-generated API documentation by FastAPI at:

    Swagger UI: http://0.0.0.0:8000/docs
    ReDoc: http://0.0.0.0:8000/redoc

These endpoints provide interactive API documentation where you can test the different endpoints.
4. Running Tests

This project uses a separate SQLite database for testing, isolated from the main database used by the application endpoints.

To run the tests, execute the following command:

bash

docker-compose exec app pytest

This will run the test suite inside the Docker container and display the results.

Alternatively, if you prefer to run the tests without entering the container:

bash

docker-compose run app pytest

5. Application Database Configuration

The application uses two SQLite databases:

    Main Database (app.db): This database is used for storing user data and handling requests to the application's endpoints.
    Test Database (test.db): This database is used exclusively during testing to isolate test data from production data.

The database connections are automatically managed by the application based on whether it's running tests or serving endpoints.
Environment Variables

The application relies on environment variables to configure certain parameters. These are defined in the .env file. Here are the important variables:

    SECRET_KEY: The key used for JWT encoding/decoding.
    ALGORITHM: The algorithm used for encoding the JWT (e.g., HS256).
    ACCESS_TOKEN_EXPIRE_MINUTES: Token expiration time in minutes.
    DATABASE_URL: The URL for the main SQLite database (e.g., sqlite:///./app.db).
    TEST_DATABASE_URL: The URL for the test SQLite database (e.g., sqlite:///./test.db).

Make sure to set up your .env file correctly before running the project.