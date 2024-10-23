from flask import Flask, session, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = 's3cr3t'  # Necesario para usar sesiones

@app.before_request
def make_session_permanent():
    session.permanent = True
    if 'products' not in session:
        session['products'] = []

@app.route('/')
def index():
    return render_template('index.html', products=session['products'])

@app.route('/add', methods=['POST'])
def add_product():
    if request.method == 'POST':
        product = {
            'id': len(session['products']) + 1,
            'nombre': request.form['nombre'],
            'cantidad': int(request.form['cantidad']),
            'precio': float(request.form['precio']),
            'fecha_vencimiento': request.form['fecha_vencimiento'],
            'categoria': request.form['categoria']
        }
        session['products'].append(product)
        return redirect(url_for('index'))

@app.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = next((p for p in session['products'] if p['id'] == product_id), None)
    if request.method == 'POST':
        product['nombre'] = request.form['nombre']
        product['cantidad'] = int(request.form['cantidad'])
        product['precio'] = float(request.form['precio'])
        product['fecha_vencimiento'] = request.form['fecha_vencimiento']
        product['categoria'] = request.form['categoria']
        return redirect(url_for('index'))
    return render_template('edit.html', product=product)

@app.route('/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    session['products'] = [p for p in session['products'] if p['id'] != product_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
