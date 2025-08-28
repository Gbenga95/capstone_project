Movie Review & Rating API
A Django REST Framework API for browsing movies by genre, submitting reviews with automatic sentiment analysis (using TextBlob), rating movies (1-5 stars), and viewing aggregated ratings. Supports JWT authentication and filtering reviews by sentiment.
Features

User registration and JWT-based authentication
CRUD operations for movies and genres (admin only)
Submit and filter reviews by sentiment (Positive, Negative, Neutral)
Rate movies and view average ratings
Browse movies by genre

Tech Stack

Backend: Django, Django REST Framework
Database: PostgreSQL
Authentication: JWT (djangorestframework-simplejwt)
Sentiment Analysis: TextBlob
Environment: Python 3.10+, virtualenv

Setup Instructions

Clone the Repository:
git clone https://github.com/Gbenga95/capstone_project.git
cd movie_api


Set Up Virtual Environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:
pip install -r requirements.txt
python -m textblob.download_corpora


Configure Environment Variables:Create a .env file in the project root:
SECRET_KEY=your-secure-secret-key
DEBUG=True
DB_NAME=movie_api_db
DB_USER=your_postgres_user
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432


Set Up PostgreSQL:

Install PostgreSQL and create a database named movie_api_db.
Or use Docker:docker run -d --name postgres -e POSTGRES_DB=movie_api_db -e POSTGRES_USER=your_postgres_user -e POSTGRES_PASSWORD=your_postgres_password -p 5432:5432 postgres:13




Apply Migrations:
python manage.py migrate


Create Superuser:
python manage.py createsuperuser


Run the Server:
python manage.py runserver

Access the admin panel at http://localhost:8000/admin/.


Current Progress

Project setup with Django, DRF, JWT, and PostgreSQL.
Models defined for Movie, Genre, Review, Rating, and MovieGenre.
Serializers implemented with TextBlob for sentiment analysis.

Next Steps

Implement API endpoints (views and URLs).
Add filtering and permissions.
Write tests and deploy to a hosting platform.

## Current Progress
- Project setup with Django, DRF, JWT, and PostgreSQL.
- Models defined for `Movie`, `Genre`, `Review`, `Rating`, and `MovieGenre`.
- Serializers implemented with TextBlob for sentiment analysis.
- Viewsets created for all API endpoints with permissions and filtering.

License
MIT License