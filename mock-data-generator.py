import json
import uuid
import string
import boto3
import random

sqs = boto3.client('sqs')

def generate_booking_data():
    message = {
        "bookingId":str(uuid.uuid4()),
        "userId":''.join(random.choices(string.ascii_uppercase + string.digits, k = 10)),
        "propertyId":''.join(random.choices(string.ascii_uppercase + string.digits, k = 10)),
        "location":random.choice(["Florida, USA","Hyd, Ind","BLR, Ind"]),
        "startDate":random.choice(["2024-03-12","2024-03-13","2024-03-14"]),
        "endDate":random.choice(["2024-03-13","2024-03-14","2024-03-15"]),
        "price":'$ ' +  str(random.randint(100,999))
    }

def lambda_handler(event,context):
    for i in range(5):
        booking_data = generate_booking_data
        response = sqs.send_message(
            QueueUrl = '',
            MessageBody = json.dumps(booking_data)
        )