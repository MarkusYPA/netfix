# Understanding Django and This Project

#### *"You should learn PHP, understand what is hell, then come back here."* - _gipi_


This document provides a high-level overview of the Django framework and the structure of this project. It's designed to be a quick and easy-to-understand guide for anyone new to Django.

## What is Django?

Django is a high-level Python web framework that enables rapid development of secure and maintainable websites. It follows the "Don't Repeat Yourself" (DRY) principle, which means it's designed to help you write less code and avoid redundancy.

### Server-Side Rendering

Django is a **server-side rendering** framework. This means that when you visit a page in your browser, the server has already assembled the HTML, CSS, and data for that page. The browser then simply displays the pre-built page. This is in contrast to client-side rendering, where the browser receives a minimal HTML file and then uses JavaScript to fetch data and build the page.

## Project Structure

This project is organized into a series of **apps**, each with a specific responsibility. This modular approach makes the project easier to manage and scale.

- **`netfix/`**: This is the main project directory. It contains the global configuration for the entire project, including settings, URL routing, and the entry point for the web server.
- **`main/`**: This app handles the core, static pages of the site, such as the homepage and the main layout.
- **`services/`**: This app is responsible for everything related to services, including creating, listing, and requesting them.
- **`users/`**: This app manages user authentication, registration, and profiles.

## How Data Flows Through the Application

Understanding how data moves through a Django application is key to understanding how it works. Here's a simplified overview of the process:

1.  **The Request:** A user in their browser clicks a link or types a URL. This sends a request to the Django server.

2.  **URL Routing (`urls.py`):** Django looks at the requested URL and checks the `urls.py` files to see which **view** should handle it. Each app has its own `urls.py` file to keep the routing organized.

3.  **The View (`views.py`):** The view is a Python function that takes the user's request and figures out what to do with it. It might need to fetch data from the database, process form submissions, or perform other logic.

4.  **The Model (`models.py`):** If the view needs to interact with the database, it uses the **models**. A model is a Python class that defines the structure of a piece of data, like a user or a service. Django's Object-Relational Mapper (ORM) allows you to interact with the database using Python code instead of writing raw SQL.

5.  **The Template (`templates/`):** Once the view has the data it needs, it passes it to a **template**. A template is an HTML file with special syntax that allows you to insert data and logic. This is where the final HTML for the page is generated.

6.  **The Response:** The view renders the template with the data, creating a complete HTML page. This page is then sent back to the user's browser to be displayed.

This entire process happens on the server, which is why Django is a server-side framework. By the time the page reaches the user's browser, it's a fully-formed HTML document.

## Case Example: Adding Data to the Database (Creating a New Service)

Let's walk through how a new service is added to the database, using the `services` app as an example.

1.  **User Interaction (Browser):** A company user navigates to the "Create Service" page (e.g., `/services/create/`). They fill out a form with details like service name, description, price, and field.

2.  **Form Submission (HTTP POST Request):** When the user clicks "Submit", their browser sends an HTTP POST request to the Django server, containing the form data.

3.  **URL Routing (`services/urls.py`):** Django receives the POST request for `/services/create/`. It consults `services/urls.py` and routes this request to the `create` function in `services/views.py`.

4.  **View Processing (`services/views.py` - `create` function):**
    *   The `create` view receives the POST request.
    *   It instantiates a Django `Form` (e.g., `CreateNewService`) with the submitted data (`request.POST`).
    *   It validates the form data (e.g., checks if all required fields are present, if data types are correct).
    *   If the form is valid, the view extracts the cleaned data (e.g., `form.cleaned_data['name']`, `form.cleaned_data['description']`).
    *   Crucially, it then interacts with the database using the `Service` model:
        ```python
        Service.objects.create(
            company=company,
            name=name,
            description=description,
            price_hour=price_hour,
            field=field
        )
        ```
        Here, `Service` is a Django model defined in `services/models.py`. `Service.objects` is Django's **Object-Relational Mapper (ORM)** manager. The `create()` method is an ORM method that takes Python keyword arguments corresponding to the model's fields.

5.  **Database Interaction (Django ORM & SQLite3):**
    *   When `Service.objects.create()` is called, the Django ORM translates this Python command into an appropriate SQL `INSERT` statement.
    *   Since this project uses `db.sqlite3` (a file-based database), the ORM executes this SQL statement against the SQLite3 database file.
    *   The new service record is then permanently saved in the `db.sqlite3` file.

6.  **Redirection/Response:** After successfully saving the data, the `create` view typically redirects the user to another page (e.g., `/services/`) to show the updated list of services, or renders a success message.

This process demonstrates how Django's ORM allows developers to work with database records as if they were regular Python objects, abstracting away the complexities of SQL and database-specific interactions (like those with SQLite3).