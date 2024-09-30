## Version considerations
Python: 3.10 required

# Application-tracker notes

You'll need to setup your own local database for the application_tracker in MariaDB.
To debug your Flask application you'll need to run this command on the commandline prior to starting the application:
> set FLASK_DEBUG=1


## .env file settings
Values are required in your .env file to be manually created in the root folder. Make sure to setup the correct values in your .env file. You'll also need an .env file matching the environment you're working in (eg. .env.development) in the frontend folder for npm to access. (Rename existing example.env to .env).

## Errors while setting up
You need to install these pip packages: 

    pymysql
    cryptography

You may need to install Connector C for MariaDB if you get this error:
> Could not find InstallationDir of MariaDB Connector/C. Please make sure MariaDB Connector/C is installed or specify the InstallationDir of MariaDB Connector/C by setting the environment variable MARIADB_CC_INSTALL_DIR.

Download it from:
https://downloads.mariadb.com/Connectors/c/connector-c-3.1.9/

You may also need Microsoft Visual C++ installed if you get this error:
> error: Microsoft Visual C++ 14.0 or greater is required. 

Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/

## Setup your database through Alembic

The following values are used from your .env file:
* APP_ACCESS_DB_HOSTNAME = hostname
* APP_ACCESS_DB_USERNAME = user name
* APP_ACCESS_DB_PASSWORD = password
* APP_ACCESS_DB_PORT = port# (defauilt mySQL port#: 3306)
* APP_ACCESS_DB_DATABASE = database name

You will also need these in the .env file:
* EXPORT_PATH= Path to "export.csv" file to create
* APP_ERROR_LOG = Path to "errorLog.txt" to create
* SECRET_KEY = See step below about creating a secret key
* FLASK_ENV = development, test, or production

# Generate secret key from the command line
```
.\venv\Scripts\python -c "import os; print(os.urandom(24).hex())"
```

If you've not yet created the database use Alembic to do so with the following commands:
```
./venv/Scripts/activate.bat
alembic init alembic
```

You'll then run the upgrade command to apply the latest SQL updates:
```
alembic upgrade head
```

## Activate your Python environment ##
```
./venv/Scripts/activate
```

## Startup commands for Flask

```
cd \backend
/venv/Scripts/activate
pip install -r requirements.txt
venv/Scripts/python.exe app.py
```

## Startup commands for Vue.js
```
cd /frontend
npm install
npm run serve
```