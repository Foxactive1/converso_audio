from flask import Flask, request, jsonify
import pyttsx3
import os

app = Flask(__name__)

# Definindo o limite de caracteres, por exemplo, 1000 caracteres
CHAR_LIMIT = 1000

# Função para dividir o texto em partes menores
def split_text(text, limit=CHAR_LIMIT):
    return [text[i:i+limit] for i in range(0, len(text), limit)]

@app.route('/generate_audio', methods=['POST'])
def generate_audio():
    text = request.form['text']
    
    # Verifica se o texto ultrapassa o limite
    if len(text) > CHAR_LIMIT:
        return jsonify({"error": f"Texto muito longo. O limite é {CHAR_LIMIT} caracteres."}), 400
    
    # Dividir o texto em partes menores, se necessário
    texts = split_text(text)
    
    # Gerar áudio para cada parte
    audio_files = []
    engine = pyttsx3.init()
    
    # Criar pasta para armazenar os áudios gerados
    output_dir = 'static/audio_output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for i, part in enumerate(texts):
        filename = os.path.join(output_dir, f'output_part_{i+1}.mp3')
        engine.save_to_file(part, filename)
        audio_files.append(f'/static/audio_output/output_part_{i+1}.mp3')
    
    engine.runAndWait()
    
    # Retornar os arquivos gerados
    return jsonify({"message": "Áudios gerados com sucesso!", "audio_files": audio_files}), 200

if __name__ == "__main__":
    app.run(debug=True)