#!/usr/bin/env python3
import csv
from decimal import Decimal
from contextlib import closing
from seed import connect_to_prodev

def stream_users():
    """ fetch rows one by one from the user_data table """
    with closing(connect_to_prodev()) as cnx:
        cur = cnx.cursor(dictionary=True)
        cur.execute("SELECT * FROM user_data")
        while True:
            user = cur.fetchone()
            if user is None:
                break
            if isinstance(user["age"], Decimal):
                user["age"] = int(user["age"])
            yield user

