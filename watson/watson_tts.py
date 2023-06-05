
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

auth = IAMAuthenticator(tts_key)
text_to_speech = TextToSpeechV1(authenticator=auth)
text_to_speech.set_service_url(tts_url)



with open((dirname(__file__), '../sample', 'audio-file2.mp3'), 'wb') as audio_file: 
    text_results = text_to_speech.synthesise(audio = audio_file, accept ="audio/mp3", voice = "en_US_AllisonVoice").get_result()
    audio_file.write(text_results.content)
