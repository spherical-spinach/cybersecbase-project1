# Project I for Cyber Security Base

This repository contains my [Project I for Cyber Security Base course](https://cybersecuritybase.mooc.fi/module-3.1)

# Installation

To set up the project, follow these steps:

1. Clone the repository:

```
git clone https://github.com/spherical-spinach/cybersecbase-project1.git
```

2. Create a virtual environment for dependency handling

```
# Navigate to the project directory:
cd cybersecbase-project1

# Create the virtual environment:
python3 -m venv example-env

# Activate the virtual environment on Windows:
example-env\Scripts\activate

# Activate the virtual environment on macOS/Linux:
source example-env/bin/activate

# Once you are done, you can exit the virtual environment by running
deactivate
```

3. Install dependencies by running this in the project folder:

```
pip install -r requirements.txt

```

4. Set up the database:

```
python3 manage.py migrate

```

5. Start the development server:

```
python3 manage.py runserver

# Application should now be running on http://127.0.0.1:8000/

# the users are bob:bob123 and alice:alice123

# Admin panel can be accessed from http://127.0.0.1:8000/admin/

# the admin user is admin:admin123

```
