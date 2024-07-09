from flask import Flask, request, jsonify
from openai import OpenAI
from deta import Deta
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 모든 출처에서의 요청을 허용

# OpenAI API 키 설정
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Deta 설정
deta_project_key = os.getenv("DETA_PROJECT_KEY")
deta = Deta(deta_project_key)

# Deta Base 인스턴스 생성
db = deta.Base("your_base_name")

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
    return "Hello, this is the Keqing chatbot backend."

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = chat_with_gpt(user_input)
    
    # Deta Base에 대화 저장 예시
    db.put({"user_input": user_input, "bot_response": response})
    
    return jsonify({'reply': response})

# Deta Base에서 데이터 조회 예시
@app.route('/get_chat', methods=['GET'])
def get_chat():
    key = request.args.get('key')
    item = db.get(key)
    return jsonify(item)

if __name__ == '__main__':
    app.run(debug=True)