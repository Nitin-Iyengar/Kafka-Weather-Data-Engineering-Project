from kafka import KafkaConsumer
from time import sleep
from json import dumps,loads
import json
from google.cloud import storage
from google.oauth2 import service_account
import time
import uuid
import datetime
import pytz

consumer = KafkaConsumer(
    'weather_data',
     bootstrap_servers=['34.121.184.86:9092'],
    value_deserializer=lambda x: loads(x.decode('utf-8')))

# Load your service account credentials
SERVICE_ACCOUNT_KEY_FILE = "D:/Kafka_Project/kafka_user.json"
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_KEY_FILE,
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

# Initialize a client to interact with Google Cloud Storage
storage_client = storage.Client(credentials=credentials)


def upload_to_gcs(bucket_name, folder_name, file_name, data):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(f"{folder_name}/{file_name}")
    blob.upload_from_string(data, content_type='application/json')
    print(f'File {file_name} uploaded to {bucket_name} bucket')

ist = pytz.timezone('Asia/Kolkata')

for message in consumer:
    received_data = message.value
    ist_now = datetime.datetime.now(ist)  # Get current time in IST
    timestamp = int(ist_now.timestamp())  # Convert to Unix timestamp
    unique_id = uuid.uuid4().hex  # Generate a unique ID
    bucket_name = 'kafka_files_storage'
    folder_name = 'weather_data'
    file_name = f"weather_data_{timestamp}_{unique_id}.json"

    # Convert the JSON data to string for upload
    data_string = json.dumps(received_data)

    # Upload received JSON data to GCS
    upload_to_gcs(bucket_name, folder_name, file_name, data_string)