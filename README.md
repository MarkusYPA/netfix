# Netfix Project

## Project Description

Netfix is a web application built with Django that connects users (customers) with service providers (companies). Customers can request various services, while companies can offer services based on their field of work. The platform supports user registration, login, profile management, service browsing, and service requests.

## How to Run the Project with Docker

Follow these steps to get the Netfix project up and running using Docker.

### Prerequisites

-   Docker Desktop (or Docker Engine) installed and running on your system.

### Setup Instructions

1.  **Clone the repository (if you haven't already):**

    ```bash
    git clone <repository_url>
    cd netfix
    ```

2.  **Build and run the Docker containers:**

    This command will build the Docker image, create the necessary containers, and start the Django development server.

    ```bash
    docker-compose up --build
    ```

    The first time you run this, it might take a few minutes to download base images and install dependencies.

3.  **Apply database migrations:**

    Once the containers are running, open a new terminal and execute the migrations. This will set up the necessary database tables and populate them with initial mock data.

    ```bash
    docker-compose exec web python manage.py migrate
    ```

4.  **Create a superuser (for admin access):**

    You'll need a superuser account to access the Django admin panel and manage data. Run this command in a new terminal:

    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```
    Follow the prompts to create your username, email, and password.

### Accessing the Application

-   **Homepage:** Open your web browser and go to `http://localhost:8000/`
-   **Admin Panel:** Access the Django administration interface at `http://localhost:8000/admin/` using the superuser credentials you created.

### Stopping the Application

To stop the Docker containers, press `Ctrl+C` in the terminal where `docker-compose up` is running. To remove the containers and associated volumes (including the database data), run:

```bash
docker-compose down -v
```

### Running the Project with a Docker Script

For a quicker setup without creating a superuser, you can use the provided `run_docker.sh` script.

1.  **Make the script executable:**

    ```bash
    chmod +x run_docker.sh
    ```

2.  **Run the script:**

    ```bash
    ./run_docker.sh
    ```

    This script will build and start the Docker containers, apply migrations, and wait for the web service to be ready.

### Accessing the Application (Script Method)

-   **Homepage:** Open your web browser and go to `http://localhost:8000/`

### Stopping the Application (Script Method)

To stop the Docker containers, run:

```bash
docker-compose down -v
```

## How to Run the Project (Python Only)

Follow these steps to get the Netfix project up and running using only Python.

### Prerequisites

-   Python 3.x

### Setup Instructions

1.  **Clone the repository (if you haven't already):**

    ```bash
    git clone <repository_url>
    cd netfix
    ```

2.  **Create and activate a virtual environment:**

    It's highly recommended to use a virtual environment to manage project dependencies.

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**

    Install all the required Python packages using pip.

    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply database migrations:**

    This will set up the necessary database tables and populate them with initial mock data.

    ```bash
    python3 manage.py migrate
    ```

5.  **Create a superuser (for admin access):**

    You'll need a superuser account to access the Django admin panel and manage data.

    ```bash
    python3 manage.py createsuperuser
    ```
    Follow the prompts to create your username, email, and password.

6.  **Run the development server:**

    ```bash
    python3 manage.py runserver
    ```

    The server will typically start at `http://127.0.0.1:8000/`

### Accessing the Application

-   **Homepage:** Open your web browser and go to `http://127.0.0.1:8000/`
-   **Admin Panel:** Access the Django administration interface at `http://127.0.0.1:8000/admin/` using the superuser credentials you created.

### Mock Data Credentials

After running `python3 manage.py migrate`, the database will be populated with some mock user data. You can use these credentials to test the application:

**Customers:**
-   **Username:** `customer1` / `customer2`
-   **Email:** `customer1@example.com` / `customer2@example.com`
-   **Password:** `password123`

**Companies:**
-   **Username:** `company1` / `company2` / `allinone`
-   **Email:** `company1@example.com` / `company2@example.com` / `allinone@example.com`
-   **Password:** `password123`