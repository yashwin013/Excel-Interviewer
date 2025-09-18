# utils.py

from gtts import gTTS
import io

def text_to_speech(text):
    """
    Converts a string of text into an in-memory audio file.
    """
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        return audio_fp
    except Exception as e:
        print(f"Error in text_to_speech: {e}")
        return None
    

