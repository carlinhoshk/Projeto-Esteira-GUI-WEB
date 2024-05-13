from flask import Flask, render_template

ligado = True

app = Flask(__name__)














@app.route('/')
def index():
    return render_template('index.html')

@app.route('/iniciar')
def iniciar():
    global ligado
    ## necessidade de criar funcao para iniciar uma animacao que mostre um gif ou animao de esteira para o usuario 
    ligado = True
    return "Simulação iniciada."

@app.route('/parar')
def parar():
    global ligado
    ligado = False
    return "Simulação parada."