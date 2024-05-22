from flask import Flask, render_template, request, jsonify, send_from_directory
import random
from time import sleep
from threading import Thread, Event
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'

# Variáveis globais
loteap = 0
loteai = 0
lotebp = 0
lotebi = 0
lotec = 0
peso_minimo = float(100)
L = ['A', 'B']
limite = 0
running = False
alert_event = Event()
grafico_counter = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/iniciar', methods=['POST'])
def iniciar():
    global running, limite
    limite = int(request.form['limite'])
    running = True
    alert_event.clear()
    Thread(target=simulacao).start()
    return jsonify({"status": "Simulação iniciada."})

@app.route('/parar', methods=['POST'])
def parar():
    global running
    running = False
    return jsonify({"status": "Simulação parada."})

@app.route('/balanca', methods=['POST'])
def balanca():
    global peso_minimo
    peso_minimo = float(request.form['peso_minimo'])
    return jsonify({"status": "Peso mínimo atualizado."})

@app.route('/alerta', methods=['GET'])
def alerta():
    if alert_event.is_set():
        alert_event.clear()
        return jsonify({"alert": True, "message": f"UM DOS LOTES ATINGIU O SEU LIMITE DE {limite} CARGAS."})
    return jsonify({"alert": False})

@app.route('/resposta', methods=['POST'])
def resposta():
    global running, loteap, loteai, lotebp, lotebi, lotec
    resposta = request.form['resposta']
    if resposta == 'C':
        running = True
        Thread(target=simulacao).start()
        return jsonify({"status": "Continuando a simulação."})
    elif resposta == 'S':
        running = False
        return jsonify({"status": "Sistema encerrado."})
    elif resposta == 'B':
        return jsonify({"status": "Configurar balança.", "configurar_balanca": True})
    else:
        return jsonify({"status": "Opção inválida. Tente novamente."})

def criar_grafico():
    global loteap, loteai, lotebp, lotebi, lotec, grafico_counter
    plt.figure()
    labels = ['Lote A2', 'Lote A1', 'Lote B2', 'Lote B1', 'Lote C']
    valores = [loteap, loteai, lotebp, lotebi, lotec]
    plt.bar(labels, valores, color=['blue', 'green', 'red', 'purple', 'orange'])
    plt.xlabel('Lotes')
    plt.ylabel('Quantidade')
    plt.title('Quantidade de produtos por lote')
    grafico_counter += 1
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], f'grafico{grafico_counter}.png')
    plt.savefig(filepath)
    plt.close()

def simulacao():
    global loteap, loteai, lotebp, lotebi, lotec, running, alert_event
    while running:
        if any(lote >= limite for lote in [loteap, loteai, lotebp, lotebi, lotec]):
            alert_event.set()
            running = False
            return
        
        letra = random.choice(L)
        numero = random.randrange(10, 99)
        etiqueta = letra + str(numero)
        tipo = '2' if numero % 2 == 0 else '1'
        lote = letra
        
        print(f"\nLote da etiqueta: {etiqueta}")
        progresso()
        peso = random.randrange(99, 15000)  # Simulando a balança
        
        print(f"A carga está a caminho do lote {lote}{tipo}")
        progresso()
        
        if peso > peso_minimo:
            if lote == 'A' and tipo == '2':
                loteap += 1
            elif lote == 'A' and tipo == '1':
                loteai += 1
            elif lote == 'B' and tipo == '2':
                lotebp += 1
            elif lote == 'B' and tipo == '1':
                lotebi += 1
            print(f"Produto de etiqueta {etiqueta} chegou ao lote {lote}{tipo}")
        else:
            lotec += 1
            print(f"Produto enviado ao lote C para verificação")
        
        criar_grafico()

        if any(lote >= limite for lote in [loteap, loteai, lotebp, lotebi, lotec]):
            alert_event.set()
            running = False

def progresso():
    for _ in range(100):
        sleep(0.01)

@app.route('/images/<filename>')
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/images')
def images():
    global grafico_counter
    if grafico_counter == 0:
        return jsonify({"latest_grafico": None})
    filename = f'grafico{grafico_counter}.png'
    return jsonify({"latest_grafico": filename})

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
