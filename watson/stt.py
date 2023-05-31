# ============================== Watson ==============================

import api

from os.path import join, dirname
import json

from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Authentication
authenticator = IAMAuthenticator(api.stt_key)
speech_to_text = SpeechToTextV1(
    authenticator=authenticator
)

speech_to_text.set_service_url(api.stt_url)

# Requesting STT
with open(join(dirname(__file__), '../sample', 'audio-file2.flac'), 'rb') as audio_file:
    speech_recognition_results = speech_to_text.recognize(
        audio=audio_file,
        content_type='audio/flac',
        word_alternatives_threshold=0.9,
        # keywords=['colorado', 'tornado', 'tornadoes'],
        # keywords_threshold=0.5
    ).get_result()

# Getting Transcript
transcript = speech_recognition_results["results"][0]["alternatives"][0]["transcript"]
print(type(transcript))

# print(json.dumps(speech_recognition_results, indent=2))

# speech_model = speech_to_text.get_model('en-GB_BroadbandModel').get_result()
# print(json.dumps(speech_model, indent=2))