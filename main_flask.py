




 # Variaveis 
 
loteap = 0
loteai = 0
lotebp = 0
lotebi = 0
lotec = 0
## adotando padrao de snake_case
peso_minimo = float(100)

L = ['A', 'B']

limite = int(0)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/iniciar')
def iniciar():
    global running
    running = True
    return "Simulação iniciada."

@app.route('/parar')
def parar():
    global running
    running = False
    return "Simulação parada."