#!/usr/bin/env python3
from contextlib import closing
from seed import connect_to_prodev

def stream_user_ages():
    """ yields user ages one by one"""
    with closing(connect_to_prodev()) as cnx:
        cur = cnx.cursor(dictionary=True)
        cur.execute("SELECT * FROM user_data")
        while True:
            user = cur.fetchone()
            if user is None:
                break
            age = user["age"]
            yield age

def average_ages():
    """ calculate average age without loading the entire dataset into memory"""
    total_ages = 0
    count = 1
    for age in stream_user_ages():
        total_ages += age
        count += 1
    return total_ages / count if count > 0 else 0 
print(average_ages())