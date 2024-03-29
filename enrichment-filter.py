from datetime import datetime

def calculate_booking_duration(start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    duration = (end_date - start_date).days
    return duration

def lambda_handler(event, context):
    for record in event['Records']:
        message = record['body']
        start_date = message['startDate']
        end_date = message['endDate']

        duration = calculate_booking_duration(start_date, end_date)

        if duration > 1:
            process_message(message)
        else:
            print(f"Ignoring message with booking duration less than or equal to 1 day: {message}")

def process_message(message):
    print(f"Processing message: {message}")
