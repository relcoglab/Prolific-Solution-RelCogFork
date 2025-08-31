


from firebase_admin import credentials, firestore, initialize_app
import config

# Initialize Firebase
firebase_credentials = config.FIREBASE_CREDENTIALS
cred = credentials.Certificate(firebase_credentials)
initialize_app(cred)
db = firestore.client()

# List of surveys and participants
surveys = [
    # "https://qualtricsxmhxsm8yb3m.qualtrics.com/jfe/form/SV_4OQou7COBK2WPs2",
    # "https://qualtricsxmhxsm8yb3m.qualtrics.com/jfe/form/SV_6KETqTdatNVMQPc"
    "https://qualtricsxmhxsm8yb3m.pdx1.qualtrics.com/jfe/form/SV_eEFjLFIsG5SEGoe"
    # Add other survey URLs here
]
participants = [
    "PROLIFIC_PID12345",
    "PROLIFIC_PID67890",
    "PROLIFIC_PID35642"
    # Add other Prolific IDs here
]

# Creating dictionaries
survey_dict = {url.split('/')[-1]: {'url': url, 'count': 0} for url in surveys}
participant_dict = {pid: [] for pid in participants}

# Populate the Firestore document
management_data_ref = db.collection('MoralCompositionTestRun').document('ManagementData')
management_data_ref.set({
    'surveys': survey_dict,
    'participants': participant_dict
})

print("Database initialized!")
