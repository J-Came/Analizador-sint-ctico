from flask import Flask, render_template, request
import re

app = Flask(__name__)

palabras_reservadas = {"for": "Palabra reservada"}

def analizar_lexico(codigo):
    tokens = []
    lineas = codigo.splitlines()

    for num_linea, linea in enumerate(lineas, start=1):
        for match in re.finditer(r'\b\w+\b', linea):
            token = match.group(0)
            if token.lower() in palabras_reservadas:
                tipo = "Palabra reservada"
            else:
                tipo = "Identificador"
            tokens.append({
                'tipo': tipo,
                'valor': token,
                'linea': num_linea,
                'columna': match.start() + 1
            })
    return tokens

def analizar_sintactico(tokens):
    estructuras = []
    
    for token in tokens:
        if token['valor'].lower() == 'for':
            estructuras.append({
                'linea': token['linea'],
                'tipo_estructura': 'For',
                'estructura_correcta': 'X',
                'estructura_incorrecta': ''
            })
        else:
            estructuras.append({
                'linea': token['linea'],
                'tipo_estructura': token['valor'],
                'estructura_correcta': '',
                'estructura_incorrecta': 'X'
            })
    return estructuras

@app.route('/', methods=['GET', 'POST'])
def index():
    tokens = []
    estructuras = []

    if request.method == 'POST':
        codigo = request.form['codigo']
        
        tokens = analizar_lexico(codigo)
        estructuras = analizar_sintactico(tokens)

    return render_template('index.html', tokens=tokens, estructuras=estructuras)

if __name__ == '__main__':
    app.run(debug=True)