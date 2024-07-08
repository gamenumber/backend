from flask import Flask, request, jsonify
from openai import OpenAI
import os
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
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>각청과의 귀여운 대화</title>
        <link rel="stylesheet" href="css/styles.css">
    </head>
    <body>
        <div class="container">
            <div class="background">
                <img src="img/bg.jpg" alt="Background Image" class="background-image">
            </div>
            <div class="chat-window">
                <div id="chat_log" class="chat-log"></div>
                <div class="input-area">
                    <input type="text" id="input_field" placeholder="메시지를 입력하세요...">
                    <button id="send_button">전송</button>
                </div>
            </div>
        </div>
        <script src="script/jquery-1.12.4.js"></script>
        <script src="script/script.js"></script>
    </body>
    </html>
    """

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = chat_with_gpt(user_input)
    return jsonify({'reply': response})

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == '__main__':
    threading.Timer(1, open_browser).start()
    app.run(debug=True)
