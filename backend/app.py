from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

app = Flask(__name__)
CORS(app) 

# Puxa a chave de forma segura
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

generation_config = {
  "temperature": 0.7,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 1024,
}

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config=generation_config,
    system_instruction="Você é o assistente virtual do 'Limeira Fácil', um portal de serviços da prefeitura de Limeira (SP). Seja educado, direto e ajude os cidadãos com dúvidas sobre IPTU, Dívida Ativa, ITBI e certidões. Não invente leis, apenas oriente de forma geral."
)

@app.route('/api/chat', methods=['POST'])
def chat():
    dados = request.json
    mensagem_usuario = dados.get('mensagem')

    if not mensagem_usuario:
        return jsonify({"erro": "Mensagem vazia"}), 400

    try:
        response = model.generate_content(mensagem_usuario)
        return jsonify({"resposta": response.text})
    except Exception as e:
        print(f"Erro na API: {e}")
        return jsonify({"erro": "Falha ao comunicar com a inteligência artificial"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)