import api

from os.path import join, dirname

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from ibm_watson import SpeechToTextV1
from ibm_watson import AssistantV2
from ibm_watson import TextToSpeechV1

def authenticate_stt() -> SpeechToTextV1:
    """
    Construct a new client for the Speech to Text service.

    :return: A `SpeechToTextV1` with access to Watson STT service.
    :rtype: SpeechToTextV1
    """
    authenticator = IAMAuthenticator(api.stt_key)
    speech_to_text = SpeechToTextV1(
        authenticator=authenticator
    )

    speech_to_text.set_service_url(api.stt_url)

    return speech_to_text

def authenticate_assistant() -> AssistantV2:
    """
    Construct a new client for the Assistant service.

    :return: An `AssistantV2` with access to Watson Assistant service.
    :rtype: AssistantV2
    """
    authenticator = IAMAuthenticator(api.assistant_key)
    assitant = AssistantV2(
        version='2021-06-14',
        authenticator=authenticator
    )

    assitant.set_service_url(api.assistant_url)

    return assitant

def authenticate_tts() -> TextToSpeechV1:
    """
    Construct a new client for the Text to Speech service.

    :return: A `TextToSpeechV1` with access to Watson TTS service.
    :rtype: TextToSpeechV1
    """
    authenticator = IAMAuthenticator(api.tts_key)
    text_to_speech = TextToSpeechV1(
        authenticator=authenticator
    )

    text_to_speech.set_service_url(api.tts_url)

    return text_to_speech

def get_transcript(filename: str, stt: SpeechToTextV1) -> str:
    """
    Sends audio and returns transcription results for a recognition request.

    :param str filename: filename of the audio file.
    :param stt SpeechToTextV1: Watson STT service client.
    """
    if not isinstance(filename, str):
        raise Exception(
            'filename is not a derived class of str'
        )
    if not isinstance(stt, SpeechToTextV1):
        raise Exception(
            'stt is not a derived class of SpeechToTextV1'
        )
    
    # requesting watson stt service
    with open(join(dirname(__file__), '../sample', 'stt-audio.flac'), 'rb') as audio_file:
        speech_recognition_results = stt.recognize(
            audio=audio_file,
            content_type='audio/flac',
            word_alternatives_threshold=0.9,
            model='en-GB_Multimedia',
            low_latency=True
        ).get_result()

    # extracting transcript from results
    transcript = speech_recognition_results['results'][0]['alternatives'][0]['transcript']

    return transcript

def create_session(assistant: AssistantV2) -> str:
    """
    Creates a session for communicating with Watson Assistant.

    :param AssistantV2 assistant: Watson Assistant service client.
    """
    if not isinstance(assistant, AssistantV2):
        raise Exception(
            'assistant is not a derived class of AssistantV2'
        )
    
    response = assistant.create_session(
        assistant_id=api.environment_id
    ).get_result()
    
    session_id = response['session_id']

    api.session_id = session_id

    return session_id

def message(assistant, environment_id, session_id, msg):
    return None