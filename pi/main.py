import sys

import keyboard

sys.path.append('watson')

import watson
import sound

def main():
    # Initialise watson clients
    stt = watson.authenticate_stt()
    kairos = watson.authenticate_assistant()
    tts = watson.authenticate_tts()

    session_id = watson.create_session(kairos)

    # Wait for button to be pressed
    while 1:
        if keyboard.is_pressed('space'):
            # Record user's request
            sound.record()

            # Get transcript
            transcript = watson.get_transcript(stt)

            # Get response
            response = watson.message(kairos, transcript)

            # Change to wav file
            watson.synthesise(tts, response)

            # Play response
            sound.play()

    return None

if __name__ == '__main__':
    main()