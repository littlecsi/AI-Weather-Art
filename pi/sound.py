from os.path import join, dirname

import pyaudio
import wave

# Set chunk size of 1024 samples per data frame
chunk = 1024

def play():
    """
    Plays the response provided from the Watson Assistant.
    """
    filename = join(dirname(__file__), '../sample', 'response.wav')

    # Open the sound file
    wf = wave.open(filename, 'rb')

    # Create an interface to PortAudio
    p = pyaudio.PyAudio()

    # Open a .Stream object to write the WAV file to
    # 'output = True' indicates that the sound will be played rather than recorded
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    
    # Read data in chunks
    data = wf.readframes(chunk)

    # Play the sound by writing the audio data to the stream
    while True:
        if data != '':
            stream.write(data)
            data = wf.readframes(chunk)
        if data == b'':
            break
    
    # Close and terminate the stream
    stream.close()
    p.terminate()

    return None

def record():
    """
    Records voice from the user.
    """
    sample_format = pyaudio.paInt16 # 16 bits per sample
    channels = 1
    fs = 44100  # Record at 44100 samples per second
    seconds = 4
    filename = join(dirname(__file__), '../sample', 'recording.wav')

    p = pyaudio.PyAudio()   # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)
    
    frames = [] # Initialise array to store frames

    # Store data in chunks for 5 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    return None

def main():
    play()

    return None

if __name__ == '__main__':
    main()