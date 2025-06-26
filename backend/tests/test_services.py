import psycopg2
import pymongo
import redis
import requests
import boto3
from botocore.exceptions import EndpointConnectionError


# PostgreSQL
def test_postgres_connection():
    try:
        conn = psycopg2.connect(
            dbname="trainiq",
            user="postgres",
            password="postgres",
            host="host.docker.internal",
            port="5432",
        )
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        assert cur.fetchone()[0] == 1
        conn.close()
    except Exception as e:
        # Affiche un message propre sans tenter de décoder quoi que ce soit
        raise AssertionError(
            f"Échec de connexion à PostgreSQL : {type(e).__name__} – {str(e).encode(errors='ignore')}"
        )


# MongoDB
def test_mongo_connection():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["trainiq_test"]
    result = db.test_collection.insert_one({"ping": "pong"})
    doc = db.test_collection.find_one({"_id": result.inserted_id})
    assert doc["ping"] == "pong"


# Redis
def test_redis_connection():
    r = redis.Redis(host="localhost", port=6379, db=0)
    r.set("test_key", "hello")
    value = r.get("test_key")
    assert value.decode() == "hello"


# NGINX
def test_nginx_running():
    response = requests.get("http://localhost")
    assert response.status_code == 200


# MinIO
def test_minio_connection():
    try:
        s3 = boto3.client(
            "s3",
            endpoint_url="http://localhost:9000",
            aws_access_key_id="minio",
            aws_secret_access_key="minio123",
            region_name="us-east-1",
        )
        buckets = s3.list_buckets()
        assert isinstance(buckets.get("Buckets"), list)
    except EndpointConnectionError:
        assert False, "Could not connect to MinIO"
