from flask import Flask, render_template, request, send_file
from gtts import gTTS
import os

app = Flask(__name__)

# Pasta para salvar o áudio gerado
AUDIO_FOLDER = "static/audio"
os.makedirs(AUDIO_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_audio', methods=['POST'])
def generate_audio():
    text = request.form['text']
    voice = request.form['voice']

    # Definir o idioma e a voz
    language = 'pt'
    if voice == 'female':
        tts = gTTS(text=text, lang=language, slow=False)
    else:  # voz masculina
        tts = gTTS(text=text, lang=language, slow=False)

    # Nome do arquivo de áudio
    audio_filename = 'output.mp3'
    audio_path = os.path.join(AUDIO_FOLDER, audio_filename)

    # Salvar o áudio gerado
    tts.save(audio_path)

    # Retornar o áudio gerado como resposta
    return send_file(audio_path, as_attachment=True, download_name='audio.mp3')

if __name__ == '__main__':
    app.run(debug=True)