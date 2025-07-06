#!/usr/bin/env python3

import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode
import csv
import uuid

load_dotenv()

def read_csv(file_path):
    """ Generator function to read csv file row by row """
    with open(file_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row

def connect_db():
    """ connect to mysql server."""
    config={
            'user': os.environ["DB_USER"],
            'password': os.environ["DB_PASSWORD"],
            'host':os.environ["DB_HOST"]
        }
    try:
        cnx = mysql.connector.connect(**config)
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return None

def create_database(connection):
    """ creates the database """
    cursor = connection.cursor()
    db_name = os.environ["DB_NAME"]
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} DEFAULT CHARACTER SET 'utf8mb4'")
        print(f"DATABASE {db_name} CREATED or already exists")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)
    finally:
        cursor.close()

def connect_to_prodev():
    """ connects tje ALX_prodev database in MYSQL """
    config={
            'user': os.environ["DB_USER"],
            'password': os.environ["DB_PASSWORD"],
            'host':os.environ["DB_HOST"],
            'database': os.environ["DB_NAME"]
        }
    try:
        cnx = mysql.connector.connect(**config)
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return None

def create_table(connection):
    """ creates a table user_data if it does not exists with the required fields."""
    cursor = connection.cursor()
    try:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(3,0) NOT NULL,
            INDEX idx_user_id (user_id)
        )
        """
        cursor.execute(create_table_query)
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    finally:
        cursor.close()

def insert_data(connection, data):
    """ inserts data in the database if it does not exists"""
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM user_data")
    count = cursor.fetchone()[0]
    if count > 0:
        print(f"Data already exists in table ({count} rows). Skipping insertion.")
        cursor.close()
        return
    try:
        insert_query = "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)"
        for row in read_csv(data):
            user_id = str(uuid.uuid4())
            cursor.execute(insert_query,
                            (user_id, row['name'], row['email'], row['age'])
                            )
        connection.commit()
        print("Data inserted successfully")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
        connection.rollback()
    except Exception as e:
        print(f"Unexpected error: {e}")
        connection.rollback()
    finally:
        cursor.close()
