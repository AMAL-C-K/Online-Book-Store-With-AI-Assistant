# Online Book Store & AI Assistant

A comprehensive Django e-commerce platform for browsing, searching, and purchasing books, complete with full cart and order management, Cash on Delivery checkout, and an integrated AI Assistant service.


# Features

* User Authentication: Registration, login, logout, and session-backed user access control.  

* Book & Catalog Management:

  - View catalog with built-in pagination.
  - Genre-wise book filtering and dedicated category views.  
  - Single book detail views with short description previews.  
  - Search engine querying across titles, authors, and genres.  
  - Multi-attribute sorting (A-Z, Price: Low to High, Price: High to Low).

* Shopping Cart System: 

  - Real-time item management
  - quantity updates, removal, and live total calculation.  

* Order & Checkout System:

  - Order creation, summary tracking
  - Cash on Delivery (COD) payment processing.  

* AI Assistant Integration:

  -Native AI recommendation engine and conversational assistant built with modular views and services (ai_assistant).


# Tech Stack

  - Backend: Python 3.12+, Django  
  - Frontend: HTML5, CSS3, javascript  
  - Database: PostgreSQL 


# Quickstart Guide

# Clone the Repository

  - git clone <repository-url>
  - cd Ecommerce_project

# Set Up Virtual Environment

  - python -m venv venv
 
 # On Windows:

  - venv\Scripts\activate

  # On macOS/Linux:
  
  - source venv/bin/activate

# Install Dependencies

  - pip install -r requirements.txt

# Configure PostgreSQL

   Ensure PostgreSQL is installed and running on your system, create a target database, and set your environment variables or update DATABASES in Ecommerce_project/settings.py[cite: 1]:

  - DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.postgresql',
         'NAME': 'your_db_name',
         'USER': 'your_db_user',
         'PASSWORD': 'your_db_password',
         'HOST': 'localhost',
         'PORT': '5432',
      }
}
# Database Migrations

  - python manage.py makemigrations
  - python manage.py migrate

# Create Admin Superuser (Optional)

  - python manage.py createsuperuser

# Run Server

  - python manage.py runserver

Access the app at [http://127.0.0.1:8000/](http://127.0.0.1:8000/). 