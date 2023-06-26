import api

from os.path import join, dirname

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from ibm_watson import SpeechToTextV1
from ibm_watson import AssistantV2
from ibm_watson import TextToSpeechV1

def authenticate_stt() -> SpeechToTextV1:
    """
    Constructs a new client for the Speech to Text service.

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
    Constructs a new client for the Assistant service.

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
    Constructs a new client for the Text to Speech service.

    :return: A `TextToSpeechV1` with access to Watson TTS service.
    :rtype: TextToSpeechV1
    """
    authenticator = IAMAuthenticator(api.tts_key)
    text_to_speech = TextToSpeechV1(
        authenticator=authenticator
    )

    text_to_speech.set_service_url(api.tts_url)

    return text_to_speech

def get_transcript(stt:SpeechToTextV1) -> str:
    """
    Sends audio and returns transcription results for a recognition request.

    :param str filename: filename of the audio file.
    :param stt SpeechToTextV1: Watson STT service client.
    :return: A `str` of user's voice transcript.
    :rtype: str
    """
    if not isinstance(stt, SpeechToTextV1):
        raise Exception(
            'stt is not a derived class of SpeechToTextV1'
        )
    
    # requesting watson stt service
    with open(join(dirname(__file__), '../sample', 'recording.wav'), 'rb') as audio_file:
        speech_recognition_results = stt.recognize(
            audio=audio_file,
            content_type='audio/wav',
            # word_alternatives_threshold=0.9,
            model='en-GB_Multimedia',
            low_latency=True
        ).get_result()

    # extracting transcript from results
    if len(speech_recognition_results['results']) != 0:
        transcript = speech_recognition_results['results'][0]['alternatives'][0]['transcript']
    else:
        return ''

    return transcript

def create_session(assistant:AssistantV2) -> str:
    """
    Creates a session for communicating with Watson Assistant.

    :param AssistantV2 assistant: Watson Assistant service client.
    :return: When successfully created, the session id is returned as `str`.
    :rtype: str
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

def message(assistant:AssistantV2, msg:str, environment_id:str=api.environment_id, session_id:str=api.session_id) -> str:
    """
    Send user input to an assistant and receive a response, 
    with conversation state (including context data) stored by Watson Assistant 
    for the duration of the session.

    :param AssistantV2 assistant: Watson Assistant service client.
    :param str environment_id: `str` form of Watson Assistant environment_id.
    :param str session_id: `str` form of Watson Assistant session_id.
    :param str msg: `str` form of message that user asks to Watson Assistant.
    :return: response of type `str` from Watson Assistant.
    :rtype: str
    """
    if not isinstance(assistant, AssistantV2):
        raise Exception(
            'assistant is not a derived class of AssistantV2'
        )
    if not isinstance(environment_id, str):
        raise Exception(
            'environment_id is not a derived class of str'
        )
    if not isinstance(session_id, str):
        raise Exception(
            'session_id is not a derived class of str'
        )
    if not isinstance(msg, str):
        raise Exception(
            'msg is not a derived class of str'
        )

    response = assistant.message(
        assistant_id=api.environment_id,
        session_id=api.session_id,
        input={
            'message_type': 'text',
            'text': msg
        }
    ).get_result()

    response = response['output']['generic'][0]['text']

    return response

def synthesise(tts:TextToSpeechV1, msg:str):
    """
    Synthesizes text to audio that is spoken in the specified voice. 
    The service bases its understanding of the language for the input text on the specified voice.
    Use a voice that matches the language of the input text.

    :param TextToSpeechV1 tts: Watson TTS service client.
    :param 
    """
    if not isinstance(tts, TextToSpeechV1):
        raise Exception(
            'tts is not a derived class of TextToSpeechV1'
        )
    if not isinstance(msg, str):
        raise Exception(
            'msg is not a derived class of str'
        )

    with open(join(dirname(__file__), '../sample', 'response.wav'), 'wb') as audio_file:
        audio_file.write(
            tts.synthesize(
                msg,
                # voice='en-US_MichaelV3Voice',
                accept='audio/wav'
            ).get_result().content)

    return None