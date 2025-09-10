Movie Review & Rating API

A Django REST Framework API for browsing movies by genre, submitting reviews with automatic sentiment analysis, rating movies (1-5 stars), and viewing aggregated ratings. Features secure JWT authentication, sentiment-based review filtering, and admin-managed movie/genre CRUD operations.

Features:

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