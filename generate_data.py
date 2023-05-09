import psycopg2
import json
import time
import random

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="postgres",
    user="airflow",
    password="airflow"
)

def rand_payload():
    payload = {}
    if random.randint(0, 10) > 5:
        payload = {
            "value": f"{random.randint(0, 1000)}",
            "score": round(random.random(), 2),
            "ocr_score": round(random.random(), 2),
            "bounding_box": [round(random.random(), 2) for i in range(4)],
        }
    return payload

while True:
    # Generate a new payload
    choices = [
        rand_payload(),
        [rand_payload() for i in range(0, 9)],
    ]
    payload = {"business_id": random.randint(0, 9)}
    fields = ["total", "line_items"]
    for f in fields:
        payload[f] = choices[random.randint(0, 9) % len(fields)]

    # Convert the payload to a string and insert it into the `documents` table
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO documents (ml_response) VALUES (%s)",
        (json.dumps(payload),)
    )
    conn.commit()
    cur.close()

    print(f"Added new row with payload: {payload}")
    time.sleep(5)
