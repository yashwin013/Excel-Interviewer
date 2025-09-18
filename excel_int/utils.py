from gtts import gTTS
import io

def text_to_speech(text):
    """
    Converts a string of text into an in-memory audio file.
    """
    try:
        # Create a gTTS object
        tts = gTTS(text=text, lang='en', slow=False)
        
        # Create an in-memory binary stream
        audio_fp = io.BytesIO()
        
        # Write the audio data to the in-memory file
        tts.write_to_fp(audio_fp)
        
        # Reset the stream's position to the beginning
        audio_fp.seek(0)
        
        return audio_fp
    except Exception as e:
        print(f"Error in text_to_speech: {e}")
        return None