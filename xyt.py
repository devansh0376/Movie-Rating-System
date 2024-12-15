watchmate/                    # Root directory of the project
│
├── watchmate/                # Main project directory (contains settings.py, urls.py, etc.)
│   ├── __init__.py           # Initialization file for the project module
│   ├── settings.py           # Django settings configuration file
│   ├── urls.py               # URL routing configuration
│   ├── wsgi.py               # WSGI application file for deployment
│
├── watchlist_app/            # Application directory for watchlist app
│   ├── __init__.py           # Initialization file for the app
│   ├── admin.py              # Admin configurations for the app
│   ├── apps.py               # App configuration
│   ├── models.py             # Model definitions (database schema)
│   ├── tests.py              # Unit tests for the app
│   ├── views.py              # Views for handling requests
│   ├── migrations/           # Database migration files
│   └── api/                  # Contains API-specific files for the app
│       ├── __init__.py
│       ├── urls.py           # API URL routing file
│       ├── views.py          # API views for the watchlist app
│       └── serializers.py    # Serializer files for API data formatting
│
├── user_app/                 # Application directory for user authentication (if applicable)
│   ├── __init__.py
│   ├── api/                  # Contains API-specific files for user authentication
│       ├── __init__.py
│       ├── urls.py           # API URL routing file for user-related endpoints
│       ├── views.py          # API views for user authentication
│
└── db.sqlite3                # SQLite database file (for local development)


----------------------------------------------------------------

Project Report for "Watchmate"

    1. Project Title:
    Watchmate: A Django-based Watchlist Management System

    2. Project Aim:
    The main aim of the Watchmate project is to develop a web-based application that allows users to maintain a personalized watchlist of their favorite movies, TV shows, or other media. The project focuses on providing a simple and user-friendly interface for adding, viewing, updating, and deleting media items in a watchlist. Additionally, it integrates a RESTful API for seamless communication between the frontend and backend, making the application more flexible and scalable.

    3. Project Description:
    Watchmate is a web application built using Django, aimed at managing a watchlist for media such as movies and TV shows. Users can log in, view their watchlist, and add new items to it. The project is built using Django REST Framework (DRF) for handling the backend, allowing for the development of an API that users can interact with via HTTP requests. This makes it possible to add or manage entries in the watchlist through a web interface or API calls.

    The application has a simple and intuitive interface, and users are provided with an option to view all their watchlisted items or filter them based on certain criteria. The watchlist can be easily customized by adding or deleting entries based on user preferences.

    4. How the Project Works:
    User Authentication:

    Users can register and log in to access their personalized watchlist. The user authentication is handled using Django’s built-in authentication system, with token-based authentication for API requests.
    Watchlist Management:

    Users can add movies, TV shows, or any media content to their watchlist.
    Each entry in the watchlist has details such as the title, genre, release year, and a description.
    The user can edit or delete entries from their watchlist.
    API Endpoints:

    The project exposes API endpoints to interact with the watchlist. For instance:
    GET /watch/ - Fetch all the media in the watchlist.
    POST /watch/ - Add a new media item to the watchlist.
    PUT /watch/{id}/ - Update an existing media item.
    DELETE /watch/{id}/ - Delete a media item from the watchlist.
    Throttling and Security:

    The project implements throttling using Django Rest Framework's built-in throttling classes. There are custom throttle rates for different types of requests (e.g., review_create, review_list).
    Token-based authentication ensures secure access to the API and protects user data.
    5. Technology Used:
    Backend:

    Django: A high-level Python web framework that simplifies backend development by providing powerful tools and a structured approach to building applications.
    Django REST Framework (DRF): A toolkit for building Web APIs. It simplifies the process of serializing data and handling HTTP requests to manage the watchlist items.
    SQLite: Used as the database for storing user and watchlist data. It is lightweight and ideal for development and testing.
    Frontend:

    The frontend is a simple Django-based web interface that interacts with the backend using API calls. (Though not provided in the files, it can be extended with HTML, CSS, and JavaScript to provide a better user experience).
    Security and Authentication:

    Token Authentication: Using Django Rest Framework's token-based authentication for secure login and access to API endpoints.
    Permissions: The API endpoints are secured using permission classes like IsAuthenticated, which ensures that only logged-in users can access their data.
    Other Tools:

    Django Filters: Used for filtering the data based on user input, making it easier to display relevant watchlist items.
    6. Features of the Project:
    User Registration and Authentication:

    Secure login and registration system for users.
    Token-based authentication for API access.
    Watchlist Management:

    Users can add, update, and delete items in their watchlist.
    Each item has key attributes like title, genre, and description.
    API-Driven Interaction:

    The project exposes RESTful API endpoints to interact with the watchlist data, enabling remote access and scalability.
    Custom throttle rates are implemented to limit API usage for security and performance.
    Security:

    Token authentication ensures that only authenticated users can manage their watchlist.
    Scalability:

    The API is designed to scale easily, allowing new features or integrations (such as connecting with third-party movie databases).
    7. Future Scope:
    The current project can be extended with the following features:

    Frontend Development: A more dynamic frontend can be developed using JavaScript frameworks like React or Angular to consume the API and provide a better user experience.

    Third-Party Integrations:

    Integration with third-party movie databases like IMDB or TMDB to fetch additional information about movies and TV shows.
    Rating and Review System:

    Users can rate and review movies/shows they have added to their watchlist.
    Search Functionality:

    Add search filters to allow users to search their watchlist based on different criteria like genre, title, or release date.

    8. Conclusion:
    The Watchmate project serves as a basic yet functional platform for managing a personal watchlist of media content. By utilizing Django and Django REST Framework, the application provides a solid foundation for handling CRUD operations on watchlist items. The token authentication system ensures the security of user data, while the throttling mechanism helps in controlling the rate of API requests to maintain performance.

    This project serves as an excellent starting point for anyone looking to develop a media management platform with Django, and it can be expanded further based on additional user requirements or new features.

9. References:
Django Documentation
Django REST Framework Documentation
SQLite Documentation



----------------------------------------------------------------
Watchmate: Django-based Watchlist Management System
Developed a web-based application for managing a personalized watchlist of movies and TV shows using Django and Django REST Framework. The project includes secure user authentication, CRUD operations for managing watchlist items, and API endpoints for seamless interaction. Implemented token-based authentication and throttling for security and performance optimization. The system is designed for scalability, with future integration possibilities for third-party movie databases and enhanced frontend features.



----------------------------------------------------------------
+-------------------+
|      User         |
+-------------------+
| id (PK)           |
| username          |
| email             |
| password          |
| first_name        |
| last_name         |
| is_active         |
+-------------------+
         |
         |  One-to-Many
         |
+-------------------+
|    Watchlist      |
+-------------------+
| id (PK)           |
| user_id (FK)      |
| title             |
| description       |
| created_at        |
| updated_at        |
+-------------------+
         |
         |  One-to-Many
         |
+-------------------+
| WatchlistItem     |
+-------------------+
| id (PK)           |
| watchlist_id (FK) |
| name              |
| year              |
| genre             |
| description       |
| rating            |
| created_at        |
| updated_at        |
+-------------------+

Explanation of Relationships:
User to Watchlist: A User can have multiple Watchlist items, establishing a one-to-many relationship.
Watchlist to WatchlistItem: A Watchlist can contain multiple WatchlistItem entries, creating another one-to-many relationship.
In this schema:

User table holds the user's personal information and authentication data.
Watchlist stores the lists of items (like movies or TV shows) that a user creates.
WatchlistItem contains details of the individual items in each watchlist.