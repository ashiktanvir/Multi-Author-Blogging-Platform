Multi-Author Blogging Platform
A full-featured Django web application where visitors can read published posts, registered readers can interact via comments and likes, and promoted authors can manage their own blog content with view analytics.

***

I have given a SPACE by mistake at the begining of my Poject Directory Name
***

Prerequisites
    1. Python: 3.9 or higher
    2. Database: PostgreSQL server running locally or remotely
    3. Environment: Virtual environment (venv)

Setup & Installation
1. Clone the Repository & Environment Setup:
   
    Navigate to your project root directory and set up the virtual environment:
    # Create virtual environment
        python3 -m venv myenv

        # Activate virtual environment (macOS/Linux)
        source myenv/bin/activate

        # Activate virtual environment (Windows)
        # myenv\Scripts\activate
        
3. Install Dependencies:
   
    Create a requirements.txt file with the necessary dependencies:
    Django>=4.2.0,<5.0.0
    psycopg2-binary>=2.9.0
    Pillow>=10.0.0
    python-dotenv>=1.0.0

  Install all required packages into your active virtual environment:
    pip install -r requirements.txt
  
  Environment Configuration (.env)
  Create a .env file in the root project folder alongside manage.py to securely store database credentials and secret key configurations:

    SECRET_KEY=django-insecure-your-super-secret-key-here
    DEBUG=True
    ALLOWED_HOSTS=127.0.0.1,localhost
    DB_NAME=multi_author_blogging
    DB_USER=postgres
    DB_PASSWORD=your_postgres_password
    DB_HOST=localhost
    DB_PORT=5432

 Database Configuration & Migrations:
 
        1. PostgreSQL Database Setup
        Ensure PostgreSQL is active and create the database specified in your .env file:

        CREATE DATABASE multi_author_blogging;

        2. Static Folder Creation
        Create an empty static directory in the project root to prevent static file setting warnings:
        
        mkdir static

        3. Run Migrations
        Execute the migration scripts to build the database tables:

        python manage.py makemigrations
        python manage.py migrate

3. Superuser Creation & Admin Setup
    1. Create Administrative Account
    Create a superuser account to manage users, categories, tags, and content via the Django Admin panel:

    python manage.py createsuperuser

4. Access the application endpoints in your web browser:

Using Django Admin Panel, Create some entries to the the Model Table to explore the features.

Public Homepage: [http://127.0.0.1:8000/]
Author Dashboard: [http://127.0.0.1:8000/dashboard/]
Admin Panel: [http://127.0.0.1:8000/admin/]

Key Feature Map
---------------

Endpoint	    Access Level	        Description
/	            Public	                Paginated published posts, search, and category/tag

/register/	    Public	                User registration 

/login/	        Public	                Secure authentication login page.

/dashboard/	    Approved Authors/Admin	Manage, edit, draft, and delete author-owned posts.
