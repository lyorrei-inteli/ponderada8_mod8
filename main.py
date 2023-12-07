from googletrans import Translator, LANGUAGES
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
import os
import sys

def convert_audio_to_wav(audio_path):
    file_extension = audio_path.split('.')[-1].lower()
    if file_extension == 'wav':
        return audio_path
    
    supported_formats = ['mp3', 'm4a', 'flac', 'wav']
    if file_extension not in supported_formats:
        raise ValueError(f"Formato de arquivo não suportado: {file_extension}")

    audio = AudioSegment.from_file(audio_path, format=file_extension)
    audio = audio.set_frame_rate(16000).set_channels(1)
    converted_audio_path = audio_path.replace(f".{file_extension}", '.wav')
    audio.export(converted_audio_path, format='wav')
    return converted_audio_path

def audio_to_text(audio_path):
    converted_audio_path = convert_audio_to_wav(audio_path)  # Converte o arquivo para WAV se necessário
    recognizer = sr.Recognizer()
    with sr.AudioFile(converted_audio_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language='pt-BR')
        return text

def translate_text(text, dest_language='en'):
    translator = Translator()
    translated = translator.translate(text, dest=dest_language)
    return translated.text

def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    audio_file = 'translated_audio.mp3'
    tts.save(audio_file)
    os.system(f"open {audio_file}")  # 'start' para Windows, use 'open' para MacOS ou 'xdg-open' para Linux

def main(audio_path):
    # Convertendo áudio para texto
    text = audio_to_text(audio_path)
    print(f"Texto Original: {text}")

    # Traduzindo o texto
    translated_text = translate_text(text)
    print(f"Texto Traduzido: {translated_text}")

    # Convertendo texto traduzido para áudio
    text_to_speech(translated_text)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("É necessário passar o caminho do arquivo de áudio como argumento")

    audio_file_path = sys.argv[1]

    if not os.path.exists(audio_file_path):
        raise ValueError(f"Arquivo não encontrado: {audio_file_path}")

    main(audio_file_path)