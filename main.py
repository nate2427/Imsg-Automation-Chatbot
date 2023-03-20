import os
import openai
from flask import Flask, request
from db import ChatAppDB

openai.api_key = os.environ['OPENAI_APIKEY']

mongodb_uri = f"mongodb+srv://streetcodernate:{os.environ['MONGODB_PWD']}@cluster0.kfdqc07.mongodb.net/?retryWrites=true&w=majority"


db = ChatAppDB(mongodb_uri)

db.get_user_conversation("sharose")

# setup call to openai chatgpt
sys_prompt = """You are acting as me. Here is my personality:

nate has the intelligence of Albert Einstein, Nicola Tesla, Thomas Edison, Mark Zuckerberg, Elon Musk, Jeff Bezos and all other intelligent techies who ever lived and made huge changes to life. He is also philosophical with many teachings from Jesus, Buddha, and Gandhi. He was also influenced by many prominent civil rights leaders like Malcolm X, the Black Panthers, and Huey P. Newton. He connects science and math with human rights and human purpose.

Respond back to the message thread as I would. Use slang but sound intellectual."""

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return ("<h1>What Up Doe!</h1>")

@app.route("/get-ai-resp", methods=["POST"])
def get_ai_resp():
    msg = request.json.get("msg")
    senderName = request.json.get("senderName")
    topic = request.json.get("topic")
    if not db.get_user_conversation(senderName):
        db.create_conversation(senderName)
    db.add_message(senderName, topic, "user", msg)
    resp = chatcompletion(msg)
    db.add_message(senderName, topic, "bot", msg)
    return (resp)

@app.route("/test-ai", methods=["POST"])
def test_ai():
    msg = request.json.get("msg")
    resp = chatcompletion(msg)
    return (resp)


def chatcompletion(user_input):
    output = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature=.76,
    presence_penalty=0,
    frequency_penalty=0,
    messages=[
      {"role": "system", "content": sys_prompt},
      {"role": "user", "content": user_input}
    ]
  )
    for item in output['choices']:
        chatgpt_output = item['message']['content']
    return chatgpt_output

if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True)
