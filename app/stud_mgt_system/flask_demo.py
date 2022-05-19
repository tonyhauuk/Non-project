from flask import Flask

app = Flask(__name__)

@app.route('/mytest')
def showString():
    return 'Hello World !!! '

if __name__ == '__main__':
    app.run(host = 'localhost', port = 8082)