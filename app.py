from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pass
    else:
        return "Send a POST-request with data"

if __name__ == '__main__':
    app.run()