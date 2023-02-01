from flask import Flask






def WSGIPROCESS(QUE_OUT,QUE_IN):
    app = Flask(__name__)

    @app.route('/<number>')
    def send_number(number):
        QUE_OUT.put(number)
        print(number)
        return {"result": "True"}

    
    app.run(port=32784)