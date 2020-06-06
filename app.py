import os
from flask import Flask,request, jsonify

# from dummy import returnDummyResults
from extractor import test

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

def compute(text=None):
    return test.main(model='./extractor/model', text=text)

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        req_data = request.get_json()
        text = req_data['text'] # text input from PHP server
        print(text) # for PHP part debug purposes

        # data = returnDummyResults.main(text=text)
        data = compute(text=text) 
        response = jsonify(data)
        response.status_code = 200
        return response # Returns the HTTP response
    else:
        return "<h1>Send a POST-request with data.</h1> <br/> <a href='https://github.com/torcoste/leadersofdigital2020-rosatom-ner'>See code on GitHub</a>"

if __name__ == '__main__':
    app.run()