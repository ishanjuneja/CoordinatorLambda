import boto3
import json
import urllib.parse

s3_client = boto3.client('s3')
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    # Get the S3 bucket name and object key from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    try:
        # Download the file from S3
        response = s3_client.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read().decode('utf-8')
        json_data = json.loads(content)
        
        # Iterate over the images array
        images = json_data.get('images', [])
        for image in json.dumps(images):
            # Trigger the second Lambda function for each object in images
            print(image['image_url'])
            lambda_client.invoke(
                FunctionName='test',
                InvocationType='Event',  # 'Event' for async, 'RequestResponse' for sync
                Payload=json.dumps(image)
            )
        
        return {
            'statusCode': 200,
            'body': json.dumps(f'Triggered second Lambda function for {len(images)} images')
        }
    
    except Exception as e:
        print(f"Error processing S3 event: {str(e)}")
        raise e