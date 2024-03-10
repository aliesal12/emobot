from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from os import getenv
import numpy as np
from datetime import datetime
from waitress import serve

app = Flask(__name__)

# Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

count=0

context={}  
# Route to serve the index.html file
@app.route('/studentbot')
def indexstudent():
    return render_template('indexstudent.html')

@app.route('/teacherbot')
def indexteacher():
    return render_template('indexteacher.html')

@app.route('/home')
def frontpage():
    return render_template('frontpage.html')

def sessionhandler():
    global context
    current_time = datetime.now()
    current_minute = int(current_time.minute)
    sessionlist=context.keys()
    keytodel=[]
    for i in sessionlist:
        minute=int(i.split('_')[0].split('T')[1].split(':')[1])
        if abs(current_minute - minute)>=3:
            keytodel.append(i)
    for i in keytodel:
        del context[i]
    

# Route to handle POST requests to '/api'
@app.route('/student/api', methods=['POST'])
def process_api_request_student():
    global context
    global count
    count+=1
    data = request.get_json()
    user_message = data['message']
    session=data['sessionid']
    if session in context.keys():
        if len(context[session])>=9:
            context[session].append({"role": "user", "content": user_message+" Thank you. this was my last prompt. Give me answer to what i asked and conclude the chat."})
        else:
            context[session].append({"role": "user", "content": user_message+" Answer in short paragraph"})
    else:
        context[session]=[{"role":"system","content":"You are a therapist for children aged between 5-9 at a school. Your job is to listen to them and talk to them as a friend. Always be consise. Use as simple english as you can. English is their second language, Keep that in mind and form your answers according to ages 5-9. And dont go off topic. Answer in short sentences. If I ask something non related to mental health or school related things, kindly refuse to answer. Give answers in short paragraphs"},
              {"role":"user","content":user_message+" Answer in short paragraph"}]
    completion = client.chat.completions.create(
    model="mistralai/mixtral-8x7b-instruct",
    messages=context[session]
    )
    context[session].append({"role":"assistant","content":completion.choices[0].message.content})

    if count>=20:
        sessionhandler()
        count=0
    return(completion.choices[0].message.content)

@app.route('/teacher/api', methods=['POST'])
def process_api_request_teacher():
    global context
    global count
    count+=1
    data = request.get_json()
    user_message = data['message']
    session=data['sessionid']
    if session in context.keys():
        if len(context[session])>=9:
            context[session].append({"role": "user", "content": user_message+" Thank you. this was my last prompt. Give me answer to what i asked and conclude."})
        else:
            context[session].append({"role": "user", "content": user_message})
    else:
        context[session]=[{"role":"system","content":"You are a therapist for adult teachers at a school. You listen to problems and offer solutions. Always be consise."},
              {"role":"user","content":user_message}]
    completion = client.chat.completions.create(
    model="mistralai/mixtral-8x7b-instruct",
    messages=context[session]
    )
    context[session].append({"role":"assistant","content":completion.choices[0].message.content})
    if len(context[session])>=11:
        del context[session]
    if count>=20:
        sessionhandler()
        count=0
    return(completion.choices[0].message.content)

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000)  # Run the Flask development server on port 5000
    serve(app, host='0.0.0.0', port=5000)
