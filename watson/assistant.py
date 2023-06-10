# ============================== Watson ==============================

import api

import json
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Authentication
authenticator = IAMAuthenticator(api.assistant_key)
assistant = AssistantV2(
    version='2021-06-14',
    authenticator = authenticator
)

assistant.set_service_url(api.assistant_url)

# # Create Assistant
# response = assistant.create_assistant(
#     language="EN",
#     name="Kairos-prototype",
#     description="KAIROS alpha test"
# ).get_result()

# # Listing Assistants
# response = assistant.list_assistants(page_limit=1)
# print(json.dumps(response, indent=2))

# Create Session
response = assistant.create_session(
    assistant_id=api.environment_id
).get_result()
api.session_id = response["session_id"]
print("api.session_id :", api.session_id)

response = assistant.message(
    assistant_id=api.environment_id,
    session_id=api.session_id,
    input={
        'message_type': 'text',
        'text': 'Hello'
    }
).get_result()

print(json.dumps(response, indent=2))