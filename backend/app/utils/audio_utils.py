from gtts import gTTS
from moviepy import AudioFileClip
import re

def tts_save(text, out_audio_path, lang="fr"):
    clean_text = re.sub(r'[^\w\s\.,\!\?\-]', '', text)
    tts = gTTS(text=clean_text, lang=lang)
    tts.save(out_audio_path)
    return AudioFileClip(out_audio_path)

def split_text_for_screens(text, max_chars=120):
    sentences = text.replace('!', '.').replace('?', '.').split('.')
    segments = []
    current_segment = ""
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        if len(current_segment + sentence) < max_chars:
            current_segment += sentence + ". "
        else:
            if current_segment:
                segments.append(current_segment.strip())
            current_segment = sentence + ". "
    
    if current_segment:
        segments.append(current_segment.strip())
    
    return segments