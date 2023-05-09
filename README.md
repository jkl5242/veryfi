# Veryfi Takehome Project

# How to run
docker compose up

Once everything is running, go to localhost:8080 and log in as airflow/airflow and start the DAG. After that, it will begin scheduling. (Part 2)

# Information
**Database**
1. username: airflow
2. password: airflow
3. database: airflow
4. port: 5432
5. host: localhost
6. You should be able to connect with DBeaver/Dbvisualizer or any other tool through with host as localhost. Two tables will be created on docker compose up startup based on init.sql - documents & parsed_total (Part 2 & 3)

**Docker**
1. Dockerfile.generate-data will be running and uploading data every second to 'documents' table (Part 1)
2. Dockerfile.analytics-api will serve as the API server that will return data Part(4)
3. docker-compose.yaml will have have airflow, generate-data, analytics-api, and pg-admin dashboard (use pg-admin dashboard if needed) running

**Dags**
1. There is one DAG that will be scheduled in 5 second batches - it will be inserting data to the parsed_total table which has schema 
CREATE TABLE parsed_total (
    id SERIAL PRIMARY KEY,
    document_id INT,
    business_id INT,
    value NUMERIC,
    score NUMERIC,
    ocr_score NUMERIC,
    bounding_box NUMERIC[]
)

**API Server** 
I created two APIs to test the sum of values:
1. /api/business/<int:business_id>
2. /api/score/<float:score>
I could have created more but the logic would be the same.

1. curl --location 'http://0.0.0.0:5001/api/business/1'
2. curl --location 'http://0.0.0.0:5001/api/score/0.03'

**Part 5**
To scale up the current setup for processing half a million documents a day or half a million database writes a day, we can consider the following strategies:
1. Horizontal scaling: We can horizontally scale the system by adding more processing nodes to distribute the load. We can use multiple instances of the data generating service, and use a load balancer to distribute incoming requests among them.
2. Stream processing: Instead of batches, we can use stream processing to process the documents in real-time. For example, we can use Apache Kafka to ingest the documents and process them as they arrive.
3. Caching: We can use caching like Redis to store frequently accessed data in memory, reducing the load on the database and improving performance for analytics
4. Data warehousing: For analytics of different fields, we can use a data warehousing solution like Amazon Redshift since it is optimized for large datasets
5. Partitioning/Sharding: We can partition the data by business_id or other relevant criteria. We can also try to create materialized views based on most frequently accessed time stamps

# Tradeoffs
I chose Postgres because for the data generator, I wanted to way to join documents and parsed_total together in order to keep track of already processed documents. Also, since the schema and data are already defined, it makes more sense to use Postgres. Lastly, Postgres also has the option to store json in a column so in general, it fit the use case better.
