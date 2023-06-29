import sys

import keyboard

sys.path.append('watson')

import watson
import sound
import bbc

def main():
    # Initialise variables
    news = []
    weather = []

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
            print('transcript:', transcript)

            # Get response according to the user's request:
            if 'weather' in transcript:
                response = watson.message(kairos, transcript)

                weather = response.split(',')
                if 'tomorrow' in transcript:
                    response = "Tomorrow's weather is " + weather[4] + ", temperature is " + weather[5] + " degrees celsius, with " + weather[6] + "% chance of rain and the wind speed is " + weather[7] + " miles per hour."
                else:
                    response = "Today's weather is " + weather[0] + ", temperature is " + weather[1] + " degrees celsius, with " + weather[2] + "% chance of rain and the wind speed is " + weather[7] + " miles per hour."                
            elif 'news' in transcript:
                news = bbc.get_top3_news()
                response = "Today's top 3 most watched news are as follows: " + news[0] + ', ' + news[1] + ' and ' + news[2] 
            else:
                response = 'Could you repeat that please?'

            # Change to wav file
            watson.synthesise(tts, response)

            # Play response 
            sound.play()

    return None

if __name__ == '__main__':
    main()