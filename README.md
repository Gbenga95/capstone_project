Movie Review & Rating API

A Django REST Framework API for browsing movies by genre, submitting reviews with automatic sentiment analysis, rating movies (1-5 stars), and viewing aggregated ratings. Features secure JWT authentication, sentiment-based review filtering, and admin-managed movie/genre CRUD operations.
Features

User Authentication: Register and log in with JWT-based authentication.
Movie Management: Admins can create, update, and delete movies and genres.
Review System: Users can submit reviews with automatic sentiment analysis (Positive, Negative, Neutral) using TextBlob.
Rating System: Rate movies (1-5 stars) and view average ratings per movie.
Filtering & Browsing: Filter reviews by sentiment and browse movies by genre.
RESTful API: Built with Django REST Framework for scalability and ease of use.

Tech Stack

Backend: Django 5.2, Django REST Framework
Database: PostgreSQL
Authentication: Django REST Framework SimpleJWT
Sentiment Analysis: TextBlob
Environment: Python 3.13.3, virtualenv
Deployment: Pythonanywhere -- https://gbenga.pythonanywhere.com/

Prerequisites

Python 3.13.3
PostgreSQL 16
Git
pip and virtualenv


Setup Instructions

Clone the Repository:
git clone https://github.com/Gbenga95/capstone_project.git
cd capstone_project


Set Up Virtual Environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:
pip install -r requirements.txt
python -m textblob.download_corpora


Configure Environment Variables:

Create a .env file in the project root:DB_NAME=movie_api_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your_secure_django_key_here
DEBUG=True


Generate a secure SECRET_KEY:python -c "import secrets; print(secrets.token_urlsafe(50))"




Set Up PostgreSQL:

Install PostgreSQL (https://www.postgresql.org/download/windows/) or use Docker:docker run -d --name postgres -e POSTGRES_DB=movie_db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=your_postgres_password -p 5432:5432 postgres:16


Create the database movie_api_db in PostgreSQL.


Apply Migrations:
python manage.py migrate


Create Superuser (for admin access):
python manage.py createsuperuser


Run the Server:
python manage.py runserver


Access the API at http://127.0.0.1:8000/.
Admin panel: http://127.0.0.1:8000/admin/.



API Endpoints



Endpoint
Method
Description
Authentication



/api/auth/register/
POST
Register a new user
None


/api/auth/login/
POST
Login and get JWT tokens
None


/api/movies/
GET, POST
List or create movies
Admin (POST)


/api/movies/<id>/
GET, PUT, DELETE
Retrieve, update, or delete a movie
Admin (PUT, DELETE)


/api/reviews/
GET, POST
List or create reviews
Authenticated (POST)


/api/reviews/?sentiment=<value>
GET
Filter reviews by sentiment (Positive, Negative, Neutral)
None


/api/movies/<id>/average-rating/
GET
Get average rating for a movie
None


/api/genres/
GET, POST
List or create genres
Admin (POST)


Example Requests:

Register:curl -X POST http://127.0.0.1:8000/api/auth/register/ \
-H "Content-Type: application/json" \
-d '{"username": "newuser11", "email": "newuser11@example.com", "password": "testpass123"}'


Create Review (with JWT):curl -X POST http://127.0.0.1:8000/api/reviews/ \
-H "Content-Type: application/json" \
-H "Authorization: Bearer [access-token]" \
-d '{"movie": 1, "review_text": "Amazing film!"}'



Testing
Run the test suite:
python manage.py test api -v 2


Tests cover user authentication, movie/genre CRUD, review submission, sentiment analysis, and rating calculations.


License
This project is licensed under the MIT License.
Contact
For issues or questions, contact Gbenga95 or open an issue on GitHub.