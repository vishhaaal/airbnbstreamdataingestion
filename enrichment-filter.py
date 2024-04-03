from datetime import datetime
import json
import boto3 

sqs = boto3.client('sqs')

def calculate_booking_duration(start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    duration = (end_date - start_date).days
    return duration

def enrich_message(message):
    booking_id = message['bookingId']
    user_id = message['userId']
    property_id = message['propertyId']
    location = message['location']
    start_date = datetime.strptime(message['startDate'], '%Y-%m-%d')
    end_date = datetime.strptime(message['endDate'], '%Y-%m-%d')
    price = message['price']

    duration = calculate_booking_duration(message['startDate'],message['endDate'])

    enriched_message = {
        "bookingId": booking_id,
        "userId": user_id,
        "propertyId": property_id,
        "location": location,
        "startDate": str(start_date),
        "endDate": str(end_date),
        "price": price,
        "duration": duration
    }

    return enriched_message

def lambda_handler(event, context):
    print(event)
    filtered_messages = []
    for record in event['Records']:
        message_body = json.loads(record['body'])
        message = json.loads(message_body['Message'])

        enriched_message = enrich_message(message_body)
        if enriched_message['duration'] > 1:
            filtered_messages.append(enriched_message)
    
    return {
        'statusCode': 200,
        'body': json.dumps(filtered_messages)
    }
  