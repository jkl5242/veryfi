from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import psycopg2
import json

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 5, 8),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def extract_total():
    conn = psycopg2.connect(
        host="postgres",
        port="5432",
        database="airflow",
        user="airflow",
        password="airflow"
    )
    cur = conn.cursor()
    cur.execute("""
    SELECT document_id, ml_response 
    FROM documents
    WHERE document_id not in (
        SELECT document_id from parsed_total
    )
    """)
    rows = cur.fetchall()
    for row in rows:
        document_id = row[0]
        ml_response = json.loads(row[1])
        business_id = ml_response['business_id']
        ml_total = ml_response['total']
        if type(ml_total) is dict:
            ml_total = [ml_total]
        for total in ml_total:
            value = int(total.get('value')) if total.get('value') else None
            score = total.get('score')
            ocr_score = total.get('ocr_score')
            bounding_box = total.get('bounding_box')
            query = cur.mogrify("""
            INSERT INTO parsed_total (document_id, business_id, value, score, ocr_score, bounding_box) VALUES (%s, %s, %s, %s, %s, %s)
            """, (document_id, business_id, value, score, ocr_score, bounding_box))
            cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()

with DAG('veryfi_extract_total', 
         default_args=default_args,
         schedule_interval=timedelta(seconds=5)) as dag:

    extract_and_load = PythonOperator(
        task_id='extract_and_load',
        python_callable=extract_total
    )
    
    extract_and_load
