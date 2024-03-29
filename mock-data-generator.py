import boto3
import json
import random
import string
import uuid
from datetime import datetime,timedelta

sqs = boto3.client('sqs')

def generate_booking_data():
    booking_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())
    property_id = str(uuid.uuid4())
    location = f"{random.choice(['New York', 'London', 'Paris'])}, {random.choice(['USA', 'UK', 'FRANCE'])}"
    start_date = (datetime.now() + timedelta(days=random.randint(1,30))).strftime('%Y-%m-%d')
    end_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d')
    price = '$' + str(round(random.uniform(50,5000), 2))

    return {
        "bookingId" : booking_id,
        "userId": user_id,
        "propertyId": property_id,
        "location": location,
        "startDate": start_date,
        "endDate": end_date,
        "price": price
    }

def publish_to_queue(data):
    response = sqs.send_message(
        QueueUrl = 'https://sqs.ap-south-1.amazonaws.com/423736870603/AirbnbBookingQueue',
        MessageBody = json.dumps(data)
    )
    print(f"Message publish to queue: {response['MessageId']}")

def lambda_handler(event,context):

    num_messages = 10
    for _ in range(num_messages):
        booking_data = generate_booking_data()
        publish_to_queue(booking_data)

    return {
        'statusCode': 200,
        'body': f'{num_messages} mock booking data messages published to AirbnbBookingQueue'
    }
