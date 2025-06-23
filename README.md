# lateshow-lenah-mbae

This is a Flask-based RESTful API that models episodes, guests, and their appearances on a fictional talk show, inspired by *The Late Show*. The project includes models with proper relationships, validations, and routes to manage and view data related to show guests and episodes.

## Features

- View all episodes and individual episode details with guest appearances.
- View all guests.
- Add new guest appearances to specific episodes.
- Validates rating input and handles errors gracefully.
- Database seeded using a CSV file.
- Proper serialization rules to avoid circular references.

## Technologies Used

- Python 
- Flask
- SQLAlchemy
- Flask-Migrate
- SQLite (development database)
- Postman (for API testing)