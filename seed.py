#!/usr/bin/env python3
import csv
import uuid
import mysql.connector
from mysql.connector import errorcode

# MySQL server credentials
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "14>=hII$$"
DB_NAME = "ALX_prodev"
TABLE_NAME = "user_data"
CSV_FILE = "user_data.csv"


def connect_db():
    """
    Connects to MySQL server (no database selected).
    """
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )


def create_database(connection):
    """
    Creates the ALX_prodev database if it does not exist.
    """
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`")
    cursor.close()


def connect_to_prodev():
    """
    Connects to the ALX_prodev database.
    """
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


def create_table(connection):
    """
    Creates the user_data table if it does not exist.
    Fields:
      - user_id   VARCHAR(36), primary key, indexed
      - name      VARCHAR(255), NOT NULL
      - email     VARCHAR(255), NOT NULL
      - age       DECIMAL(5,2), NOT NULL
    """
    ddl = f"""
    CREATE TABLE IF NOT EXISTS `{TABLE_NAME}` (
        user_id VARCHAR(36) NOT NULL,
        name    VARCHAR(255) NOT NULL,
        email   VARCHAR(255) NOT NULL,
        age     DECIMAL(5,2)  NOT NULL,
        PRIMARY KEY (user_id)
    ) ENGINE=InnoDB;
    """
    cursor = connection.cursor()
    cursor.execute(ddl)
    cursor.close()


def insert_data(connection, record):
    """
    Inserts a single record into user_data.
    Uses INSERT IGNORE to skip duplicates based on primary key.
    `record` should be a tuple: (user_id, name, email, age)
    """
    sql = f"""
    INSERT IGNORE INTO `{TABLE_NAME}`
      (user_id, name, email, age)
    VALUES
      (%s, %s, %s, %s)
    """
    cursor = connection.cursor()
    cursor.execute(sql, record)
    connection.commit()
    cursor.close()


def seed_from_csv(connection, csv_path):
    """
    Reads user_data.csv and inserts each row into the database.
    Expects CSV with headers: user_id,name,email,age
    If user_id is blank in CSV, generates a new UUID4.
    """
    with open(csv_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            uid = row.get("user_id") or str(uuid.uuid4())
            name = row["name"].strip()
            email = row["email"].strip()
            age  = row["age"].strip()
            insert_data(connection, (uid, name, email, age))


def main():
    # 1. Connect to MySQL server and create database
    try:
        conn = connect_db()
        create_database(conn)
    except mysql.connector.Error as err:
        print("Error connecting or creating database:", err)
        return
    finally:
        conn.close()

    # 2. Connect to ALX_prodev and create table
    try:
        conn = connect_to_prodev()
        create_table(conn)
    except mysql.connector.Error as err:
        print("Error connecting to ALX_prodev or creating table:", err)
        return

    # 3. Seed the table from CSV
    try:
        seed_from_csv(conn, CSV_FILE)
        print("Seeding completed successfully.")
    except Exception as e:
        print("Error while seeding data:", e)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
