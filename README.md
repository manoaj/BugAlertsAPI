# BugAlertsAPI


## Overview

This project is a part of the BugAlerts UI project. The backend of the system is developed using Python FastAPI, and it serves as the intermediary communication layer between the frontend user interface, the backendand database. Several Application Programming Interfaces (APIs) have been implemented to enable seamless interaction between these components. These APIs facilitate the exchange of data and requests, ensuring efficient data flow and functionality across the entire system.


## Prerequisites

Before you begin, ensure you have the following installed on your system:

- PostgreSQL (version 15)
- Python 3.x
- Homebrew (for macOS users)


## Installation

### Install PostgreSQL

For macOS using Homebrew:
```
brew install postgresql@15
```
Start PostgreSQL and make sure PostgreSQL is running.

### Add PostgreSQL to Path
```
export PATH=$PATH:/path/to/your/postgresql/bin
```

### Clone the Project

```
git clone https://github.com/your-username/BugAlertsAPI.git
cd BugAlertsAPI
```

### Add Credentials
In the file /code/Cred.py, add your intranet username and password:
```
# /code/Cred.py

username = "your_username"   # Add your SSO username
password = "your_password"   # Add your SSO password
```

### Install Python Packages
```
pip3 install -r requirements.txt 
pip3 install psycopg2
```


## Usage
Navigate to the parent directory (/code) and run the application using the following command:
```
python3 -m uvicorn main:app --reload
```
The application should now be accessible at http://localhost:8000.


## Troubleshooting
If you encounter any issues during the installation or setup process, please check the following:

- Ensure PostgreSQL is running.
- Confirm that the correct version of Python is installed.
- Double-check that the required Python packages are installed.
- Verify that your intranet username and password are correctly set in /code/Cred.py.
If you still face problems, please open an issue on GitHub.
