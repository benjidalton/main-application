import os
import simplejson as json
import mysql.connector
import utility as util

from flask import jsonify

APP_ACCESS_DB_HOST = os.getenv("APP_ACCESS_DB_HOSTNAME")
APP_ACCESS_DB_USERNAME = os.getenv("APP_ACCESS_DB_USERNAME")
APP_ACCESS_DB_PASSWORD = os.getenv("APP_ACCESS_DB_PASSWORD")
APP_ACCESS_DB_DATABASE = os.getenv("APP_ACCESS_DB_DATABASE")
APP_ACCESS_DB_PORT = int(os.getenv("APP_ACCESS_DB_PORT"))

PARAM_QUERY_FAILED = "parameterized query failed {}"
CONNECTION_CLOSED = "MySQL connection is closed"

import logging
logger = logging.getLogger('app')

def executeAddSQL(insert_tuple, INSERT_SQL):
    id = 0
    try:  
        with mysql.connector.connect(
            host = APP_ACCESS_DB_HOST,
            user = APP_ACCESS_DB_USERNAME,
            password = APP_ACCESS_DB_PASSWORD,
            database = APP_ACCESS_DB_DATABASE,
            port = APP_ACCESS_DB_PORT
        ) as connection:
            with connection.cursor(prepared=True) as cursor:
                print('SQL_UTILITY ', INSERT_SQL, insert_tuple)
                cursor.execute(INSERT_SQL, insert_tuple)
                id = cursor.lastrowid
                connection.commit()
                cursor.close() 
            
            return jsonify({'success': True, 'id': id}), 200
    
    except mysql.connector.Error as error:
        print(PARAM_QUERY_FAILED.format(error))
        logger.debug("ERROR executeAddSQL() %s", INSERT_SQL)
        logger.debug("Tuple %s", insert_tuple)
        logger.debug("Exception ", exc_info=True)
        return jsonify({'success': False, 'message': error.msg}), 500
    
    finally:
        if connection.is_connected():
            connection.cursor().close()
            connection.close()
            print(CONNECTION_CLOSED)
            print()
    
def executeSelectSql(tuple,sql):
    items = ()

    try:
        with mysql.connector.connect(
            host = APP_ACCESS_DB_HOST,
            user = APP_ACCESS_DB_USERNAME,
            password = APP_ACCESS_DB_PASSWORD,
            database = APP_ACCESS_DB_DATABASE,
            port = APP_ACCESS_DB_PORT

        ) as connection:
            with connection.cursor(buffered=True) as cursor:
                cursor.execute(sql, tuple)
                rows = cursor.fetchall()
                items = [dict((cursor.description[i][0], value) \
                    for i, value in enumerate(row)) for row in rows]

        return json.dumps({'status':'success','items':items}, default =str)  

    except mysql.connector.Error as error:
        logger.debug("ERROR executeSelectSql() %s", sql)
        logger.debug("Tuple %s", tuple)
        logger.debug("Exception ", exc_info=True)
        return json.dumps({'status':'fail','items':items}, default =str) 
    
    finally:
        if connection.is_connected():
            connection.cursor().close()
            connection.close()
            print(CONNECTION_CLOSED)
            print()


# Delete
def execute_delete_sql(update_delete_tuple, sql):
    try:
        with mysql.connector.connect(
            host = APP_ACCESS_DB_HOST,
            user = APP_ACCESS_DB_USERNAME,
            password = APP_ACCESS_DB_PASSWORD,
            database = APP_ACCESS_DB_DATABASE,
            port = APP_ACCESS_DB_PORT,
        ) as connection:
                       
            with connection.cursor(prepared=True) as cursor:
                cursor.execute(sql, update_delete_tuple)
                connection.commit()
                cursor.close()

        return jsonify({'success': True}), 200        
                
    except mysql.connector.Error as error:
        print(PARAM_QUERY_FAILED.format(error))
        logger.debug("ERROR executeUpdateDeleteSql() %s", sql)
        logger.debug("Tuple %s", update_delete_tuple)
        logger.debug("Exception ", exc_info=True)
        
        return jsonify({'success': False, 'message': error.msg}), 500
   
    finally:
        if connection.is_connected():
            connection.cursor().close()
            connection.close()
            print(CONNECTION_CLOSED)
            print()

# Update, or Insert if missing
def execute_update_insert_sql(tuple, update_sql, insert_sql):
    result_success = False

    try:
        with mysql.connector.connect(
            host = APP_ACCESS_DB_HOST,
            user = APP_ACCESS_DB_USERNAME,
            password = APP_ACCESS_DB_PASSWORD,
            database = APP_ACCESS_DB_DATABASE,
            port = APP_ACCESS_DB_PORT,
        ) as connection:
              
            with connection.cursor(prepared=True) as cursor:
                cursor.execute(update_sql, tuple)
                logger.debug("SQL: %s --result rows: %s", update_sql, cursor.rowcount)

                if (cursor.rowcount == 0):
                    cursor.execute(insert_sql, tuple)
                    logger.debug("SQL: %s --result rows: %s", insert_sql, cursor.rowcount)

                if (cursor.rowcount != 1):
                    logger.error("ERROR executeUpdateInsertSql() %s", insert_sql)
                else:
                    result_success = True
                
                connection.commit()
                cursor.close()
        
        numericResponse = 200
        if (result_success != True):
            numericResponse = 500

        return jsonify({'success': result_success}), numericResponse
                
    except mysql.connector.Error as error:
        print(PARAM_QUERY_FAILED.format(error))
        logger.debug("ERROR executeUpdateInsertSql()")
        logger.debug("Tuple %s", tuple)
        logger.debug("Exception ", exc_info=True)
        
        return jsonify({'success': False, 'message': error.msg}), 500
   
    finally:
        if connection.is_connected():
            connection.cursor().close()
            connection.close()
            print(CONNECTION_CLOSED)
            print()
       
