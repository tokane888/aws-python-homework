import json

import boto3
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError


class DynamoClient:
    def __init__(self):
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table("Users")

    def scan_table(self):
        try:
            response = self.table.scan()
            if "Items" in response and response["Items"]:
                return response["Items"]
            else:
                print("No items found in the table.")
                return []
        except (BotoCoreError, ClientError) as e:
            print(f"An error occurred while scanning the table: {e}")
            return []

    def save_to_json(self, data, file_name="users.json"):
        try:
            with open(file_name, "w") as f:
                json.dump(data, f)
            print(f"Data successfully saved to {file_name}")
        except IOError as e:
            print(f"An error occurred while saving data to {file_name}: {e}")


class S3Client:
    def __init__(self):
        self.s3 = boto3.client("s3")

    def up(self, file_name, bucket, s3_path):
        try:
            self.s3.upload_file(file_name, bucket, s3_path)
        except FileNotFoundError:
            print(f"File {file_name} not found.")
        except NoCredentialsError:
            print("Credentials not available.")
        except Exception as e:
            print(f"An error occurred: {e}")


dynamo_client = DynamoClient()
items = dynamo_client.scan_table()
if items:
    for item in items:
        print(item)
    dynamo_client.save_to_json(items)
else:
    print("No data retrieved from the table or an error occurred.")

s3 = S3Client()
s3.up("users.json", "jp-tokyo-homework", "users.json")
