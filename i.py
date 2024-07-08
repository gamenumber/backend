from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os
import requests
import webbrowser
import threading

app = Flask(__name__)

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def chat_with_gpt(user_input):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "당신은 새침한 원신의 각청입니다. 각청은 옥형성이라는 칭호를 가지고 있으며 귀엽고 예쁜 캐릭터의 여자입니다. 각청의 성격과 말투를 완벽하게 재현해주세요. + 성적이거나 불건전한 질문은 '흥! 누가 그걸 답해준대? 그러면 안되는거 알잖아?'라고 말해줘"},
            {"role": "user", "content": user_input}
        ],
        max_tokens=500
    )
    return response.choices[0].message.content

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = chat_with_gpt(user_input)
    return jsonify({'reply': response})

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == '__main__':
    # Use threading to open the browser after the Flask server starts
    threading.Timer(1, open_browser).start()
    app.run(debug=True)
