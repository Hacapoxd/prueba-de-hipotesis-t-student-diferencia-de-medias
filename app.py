from flask import Flask, render_template, request, jsonify, send_from_directory
from scipy import stats 
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg') 
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/pg_calcular')
def pg_calcular():
    return render_template('calcular.html')

@app.route('/imagen_t')
def imagen_t():
    return render_template('imagen_t.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    # Obtener los datos del formulario
    data = request.get_json()
    sample1 = np.array(data['sample1'])
    sample2 = np.array(data['sample2'])
    alpha = data['alpha']
    hypothesis = data['hypothesis']

    # Realizar la prueba de hipótesis T-Student
    t_stat, p_value = stats.ttest_ind(sample1, sample2)

    # Definir mensaje de resultado según la hipótesis seleccionada
    if hypothesis == 'two-tailed':
        # Zona de rechazo bilateral
        t_critical = stats.t.ppf(1 - alpha / 2, df=len(sample1) + len(sample2) - 2)
        message = f'Prueba bilateral: t-statistic = {t_stat:.2f}, p-value = {p_value:.4f}'
        reject_null = p_value < alpha
    elif hypothesis == 'left-tailed':
        # Zona de rechazo unilateral izquierda
        t_critical = stats.t.ppf(alpha, df=len(sample1) + len(sample2) - 2)
        message = f'Prueba unilateral izquierda: t-statistic = {t_stat:.2f}, p-value = {p_value:.4f}'
        reject_null = t_stat < t_critical
    else:  # right-tailed
        # Zona de rechazo unilateral derecha
        t_critical = stats.t.ppf(1 - alpha, df=len(sample1) + len(sample2) - 2)
        message = f'Prueba unilateral derecha: t-statistic = {t_stat:.2f}, p-value = {p_value:.4f}'
        reject_null = t_stat > t_critical

    # Generar la gráfica de la distribución T-Student
    x = np.linspace(min(-5, t_stat - 3), max(5, t_stat + 3), 1000)
    y = stats.t.pdf(x, df=len(sample1) + len(sample2) - 2)

    plt.figure(figsize=(8, 4))
    plt.plot(x, y, label='Distribución T-Student', color='blue')

    # Ajustar la zona de rechazo según la hipótesis
    if hypothesis == 'two-tailed':
        # Rellenar zonas de rechazo para prueba bilateral
        plt.fill_between(x, y, where=(x < -t_critical) | (x > t_critical), color='red', alpha=0.5, label='Zona de rechazo')
    elif hypothesis == 'left-tailed':
        # Rellenar zona de rechazo para prueba unilateral izquierda
        plt.fill_between(x, y, where=(x < t_critical), color='red', alpha=0.5, label='Zona de rechazo')
    else:  # right-tailed
        # Rellenar zona de rechazo para prueba unilateral derecha
        plt.fill_between(x, y, where=(x > t_critical), color='red', alpha=0.5, label='Zona de rechazo')

    # Añadir línea de t-statistic
    plt.axvline(t_stat, color='red', linestyle='--', label=f't-statistic = {t_stat:.2f}')
    plt.title('Distribución T-Student')
    plt.xlabel('Valor t')
    plt.ylabel('Densidad de probabilidad')
    plt.legend()

    # Verificar si el directorio estático existe, si no, crear
    if not os.path.exists('static'):
        os.makedirs('static')

    # Guardar la imagen de la gráfica
    plt.savefig('static/grafica.png')
    plt.close()

    # Retornar los resultados al frontend
    return jsonify({'message': message, 't_stat': t_stat, 'p_value': p_value})

@app.route('/static/<path:filename>')
def send_image(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)

