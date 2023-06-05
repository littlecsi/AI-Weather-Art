import  os

from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from pydub import AudioSegment
from pydub.playback import play


auth = IAMAuthenticator(tts_key)
text_to_speech = TextToSpeechV1(authenticator=auth)
text_to_speech.set_service_url(tts_url)



with open(os.path.join(dirname(__file__), '../transcript', 'text.txt'), 'r') as text_file: 
    text = text_file.read()
    text_results = text_to_speech.synthesize(text, accept="audio/mp3", voice="en_US_AllisonVoice").get_result()
with open("audio-file2.mp3", "wb") as audio_file:
    audio_file.write(text_results.content)
# Load the audio file
audio = AudioSegment.from_file("audio-file2.mp3", format="mp3")
# Play the audio file
play(audio)
