from model import ChatbotLLM
from flask import Flask, request, jsonify, render_template, send_from_directory

chatbot = ChatbotLLM()

app = Flask(__name__)

def process_response(response):
    rows = response.split('\n')
    open_list = False
    result = []

    for row in rows:
        if row.startswith('-'):
            if not open_list:
                result.append('<ul class="list">')
                open_list = True

            item = row[2:]
            result.append(f'<li>{item}</li>')

        else:
            if open_list:
                result.append('</ul>')
                open_list = False

            result.append(row)

    if open_list:
        result.append('</ul>')

    return ' '.join(result)

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/chatbot', methods=['POST'])
def model():
    user_message = request.json['user_message']
    response = chatbot.make_query(user_message)

    return jsonify({'response': response})


@app.route('/')
def result():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)