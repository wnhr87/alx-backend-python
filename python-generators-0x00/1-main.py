#!/usr/bin/env python3
from itertools import islice
import time

stream_users = __import__('0-stream_users').stream_users

# iterate over the generator function and print only the first 6 rows

start_time = time.time()
for user in islice(stream_users(), 6):
    print(user)

end_time = time.time()

time_elapsed = start_time - end_time
print(f"Execution Time: {time_elapsed:.4f} seconds")
