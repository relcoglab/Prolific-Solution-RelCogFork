import sys
import os

print("Python path:", sys.path)
print("Contents of /var/task/:", os.listdir('/var/task/'))
# print("Contents of /var/task/python/:", os.listdir('/var/task/python/'))

try:
    import firebase_admin
    print("✅ firebase_admin imported successfully")
except Exception as e:
    print("❌ firebase_admin failed:", str(e))

try:
    from firebase_admin import credentials
    print("✅ credentials imported successfully")
except Exception as e:
    print("❌ credentials failed:", str(e))

try:
    from firebase_admin import firestore
    print("✅ firestore imported successfully")
except Exception as e:
    print("❌ firestore failed:", str(e))
    print("Exception type:", type(e))

try:
    import google.cloud.firestore
    print("✅ google.cloud.firestore imported directly")
except Exception as e:
    print("❌ google.cloud.firestore failed:", str(e))
    print("Exception type:", type(e))

import json
import random
from firebase_admin import credentials, firestore, initialize_app, get_app
import config

def lambda_handler(event, context):
    try:
        # Attempt to get the default Firebase app, initialize if not found
        app = get_app()
    except ValueError:
        # Initialize Firebase if app does not exist
        firebase_credentials = config.FIREBASE_CREDENTIALS
        cred = credentials.Certificate(firebase_credentials)
        app = initialize_app(cred)

    db = firestore.client(app=app)  # Ensure to pass the app instance to the client

    try:
        # Extract Prolific ID from the API Gateway query string parameters
        prolific_id = event['queryStringParameters']['PROLIFIC_PID']

        # Reference to the Firestore management document
        management_ref = db.collection('MoralCompositionTestRun').document('ManagementData')
        management_data = management_ref.get().to_dict()

        # Get participant and survey data
        participants_dict = management_data.get('participants', {})
        survey_dict = management_data.get('surveys', {})

        # Get the surveys this participant has already taken
        taken_surveys = participants_dict.get(prolific_id, [])

        # Filter for surveys not taken by this participant and not full
        available_surveys = {k: v for k, v in survey_dict.items() if k not in taken_surveys and v['count'] < 10}

        if not available_surveys:
            return {
                'statusCode': 200,
                'body': json.dumps('All surveys are completed or no available surveys. Please contact AOI for more information.')
            }

        # Randomly select a new survey
        survey_id, survey_data = random.choice(list(available_surveys.items()))

        # Increment the survey count and update or add the participant's survey list
        survey_data['count'] += 1
        if prolific_id not in participants_dict:
            participants_dict[prolific_id] = [survey_id]
        else:
            participants_dict[prolific_id].append(survey_id)

        # Write updates back to Firestore
        management_ref.set({
            'participants': participants_dict,
            'surveys': survey_dict
        })

        # Return the survey URL for redirection
        return {
            'statusCode': 302,
            'headers': {
                'Location': survey_data['url']
            },
            'body': json.dumps({'message': 'Redirecting to survey...'})
        }
    except Exception as e:
        print("Error: ", str(e))  # Log the error to CloudWatch
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal Server Error', 'error': str(e)})
        }
