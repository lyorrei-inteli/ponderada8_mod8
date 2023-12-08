# Tradutor de Áudio

## Objetivo
Este projeto consiste em uma aplicação capaz de integrar um tradutor de texto, uma aplicação de speech-to-text (reconhecimento de voz), e uma aplicação de text-to-speech (síntese de voz). Seu objetivo principal é receber um arquivo de áudio, converter o áudio em texto, traduzir o texto para outro idioma e, finalmente, converter o texto traduzido de volta para áudio.

## Como Funciona
A aplicação opera em linha de comando e aceita como argumento o caminho de um arquivo de áudio. Após processar o áudio, a aplicação o converte em texto, traduz o texto e sintetiza o texto traduzido em um novo arquivo de áudio.

## Requisitos
- Python
- Bibliotecas: `googletrans`, `speech_recognition`, `gtts`, `pydub`
- Acesso à internet para as APIs de tradução e reconhecimento de voz

## Instalação e Execução
1. Instale as dependências necessárias:
   ```
   pip install googletrans speech_recognition gtts pydub
   or
   pip install -r requirements.txt
   ```
2. Execute o script com o seguinte comando, substituindo `[caminho do arquivo de áudio]` pelo caminho do seu arquivo de áudio:
   ```
   python main.py [caminho do arquivo de áudio]
   ```

   ex:
   ```
   python main.py audio.m4a
   ```
### Considerações importantes
Caso o script não funcione, tente instalar o `ffmpeg` no seu sistema.

Se der erro na função `text_to_speech`, mude a última linha da função text_to_speech para `os.system(f"start {audio_file}")`. Isso será necessário caso você esteja utilizando Windows.

## Explicação do Código com Trechos Relevantes

### `convert_audio_to_wav(audio_path)`
- **Propósito**: Converte um arquivo de áudio para o formato WAV.
- **Trecho de Código**:
  ```python
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
  ```

### `audio_to_text(audio_path)`
- **Propósito**: Converte áudio em texto.
- **Trecho de Código**:
  ```python
  def audio_to_text(audio_path):
      converted_audio_path = convert_audio_to_wav(audio_path)  # Converte o arquivo para WAV se necessário
      recognizer = sr.Recognizer()
      with sr.AudioFile(converted_audio_path) as source:
          audio_data = recognizer.record(source)
          text = recognizer.recognize_google(audio_data, language='pt-BR')
          return text
  ```

### `translate_text(text, dest_language='en')`
- **Propósito**: Traduz o texto para outro idioma.
- **Trecho de Código**:
  ```python
  def translate_text(text, dest_language='en'):
      translator = Translator()
      translated = translator.translate(text, dest=dest_language)
      return translated.text
  ```

### `text_to_speech(text, lang='en')`
- **Propósito**: Converte texto em áudio (mude a última linha para `os.system(f"start {audio_file}")` se estiver usando Windows).
- **Trecho de Código**:
  ```python
  def text_to_speech(text, lang='en'):
      tts = gTTS(text=text, lang=lang)
      audio_file = 'translated_audio.mp3'
      tts.save(audio_file)
      os.system(f"open {audio_file}")  # 'start' para Windows, use 'open' para MacOS ou 'xdg-open' para Linux
  ```

### `main(audio_path)`
- **Propósito**: Coordena o fluxo do programa.
- **Trecho de Código**:
  ```python
  def main(audio_path):
      # Convertendo áudio para texto
      text = audio_to_text(audio_path)
      print(f"Texto Original: {text}")

      # Traduzindo o texto
      translated_text = translate_text(text)
      print(f"Texto Traduzido: {translated_text}")

      # Convertendo texto traduzido para áudio
      text_to_speech(translated_text)
  ```

## Demonstração
Uma demonstração do funcionamento da aplicação pode ser vista no vídeo disponível no repositório. Este vídeo mostra o processo completo, desde a entrada do arquivo de áudio até a reprodução do áudio traduzido.
https://youtu.be/0nDeQgvMsqQ
