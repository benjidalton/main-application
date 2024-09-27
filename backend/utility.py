import os

from dotenv import load_dotenv
from pathlib import Path
from os.path import exists

import pythoncom
# For Python threading, this has to be here
pythoncom.CoInitialize()

from pyad import aduser

import logging
logger = logging.getLogger('app')
# load_dotenv(os.path.join(os.path.dirname( __file__ ), '..', '.env'))

# The .env file
#
# Program reads the .env file and it will be overwritten depending on what the
# FLASK_ENV variable is set to.
# For example if FLASK_ENV = test it will be overwritten with what is in test.
# The .env file should be used as pairs.
# .env & .env.development
# .env & .env.test
# .env & .env.production  
    
flaskEnvironmentVariable = 'FLASK_ENV'
dotEnv = None
if os.environ.get(flaskEnvironmentVariable) is None:
    logger.debug("ERROR Environment variable is not set and must be one of [test, development, production]")
    raise OSError(flaskEnvironmentVariable + ' Environment variable is not set and must be one of [test, development, production]')
    
environment = os.environ[flaskEnvironmentVariable]
defaultSettings = Path(os.path.join(os.path.dirname( __file__ ), '..', '.env'));

if not exists(defaultSettings):
    logger.debug("ERROR Default Settings not found, missing .env")
    raise OSError('Default Settings not found')
dotEnv = load_dotenv(dotenv_path=defaultSettings)
if environment is not None:
    dotEnv = load_dotenv(dotenv_path=os.path.join(os.path.dirname( __file__ ), '..', '.env.' +environment), override=True)
else:
    logger.debug("ERROR Environment variable is not set and must be one of [test, development, production]")
    raise   OSError(flaskEnvironmentVariable + ' Environment variable is not set and must be one of [test, development, production]')

# Find the original data to check if it was modified
def findRecordById(list, id):
    try:
        for item in list:
            if item['id'] == id:
                return item
        
        return None  
    except Exception as e:
        logger.debug("Exception in findRecordById() ", exc_info=True)  
        return None    

# Test if a string is either None OR Empty OR Blank:
def isNotBlank (myString):
    if(myString == None):
        return False
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return True
    #myString is None OR myString is empty or blank
    return False  

# Verify that the user sigining in is in the IT dept,  all other users are not allowed
# to use this app
def verifyItUser(email):
    try:
        isValid = False
        
        result = email.split(".")
        fname_tmp = result[0] 
        fname = fname_tmp.capitalize()
        
        lntmp = result[1]
        lname_tmp1 = lntmp.split("@")
        lname_tmp2 = lname_tmp1[0]
        lname = lname_tmp2.capitalize()
        user_name = fname + " " + lname

        # For Python threading
        pythoncom.CoInitialize()

        # Use JXplorer to get this info CN,OU,OU,OU,DC
        user = aduser.ADUser.from_dn("CN=" + user_name + ",OU=Employees,OU=Users,OU=IT,OU=Knox-Main,DC=knox-main,DC=org")
        department = str(user.get_attribute('department', always_return_list=False)).strip().replace('None', '')
        if(department == "Information Technology"):
           isValid = True
        
        return isValid

    except Exception as e:
        logger.debug("Exception in verifyItUser() ", exc_info=True)  
        return isValid      