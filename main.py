# main.py
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

usuarios = []

class Usuario:
    def __init__(self, id, nome, email, telefone):
        self.id = id
        self.nome = nome
        self.email = email
        self.telefone = telefone

usuarios.append(Usuario(1, 'Guilherme', 'guivega7@gmail.com', '(11) 99639-1346'))
usuarios.append(Usuario(2, 'Sophia', 'sophia@gmail.com', '(11) 4002-8922'))

@app.route('/')
def index():
    return render_template('index.html', usuarios=usuarios)

@app.route('/criar', methods=['GET', 'POST'])
def criar():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip().lower()
        telefone = request.form.get('telefone', '').strip()
        
        # Validação básica
        if not nome or not email or not telefone:
            flash('Todos os campos são obrigatórios!', 'error')
            return redirect(url_for('criar'))
            
        # Verifica se email já existe
        if any(u.email.lower() == email for u in usuarios):
            flash('Este email já está cadastrado!', 'error')
            return redirect(url_for('criar'))
            
        novo_id = max(u.id for u in usuarios) + 1 if usuarios else 1
        novo_usuario = Usuario(novo_id, nome, email, telefone)
        usuarios.append(novo_usuario)
        flash('Usuário adicionado com sucesso!', 'success')
        return redirect(url_for('index'))
    return render_template('criar.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    usuario = next((u for u in usuarios if u.id == id), None)
    if not usuario:
        flash('Usuário não encontrado!', 'error')
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip().lower()
        telefone = request.form.get('telefone', '').strip()
        
        # Validação básica
        if not nome or not email or not telefone:
            flash('Todos os campos são obrigatórios!', 'error')
            return redirect(url_for('editar', id=id))
            
        # Verifica se outro usuário já tem este email
        if any(u.email.lower() == email and u.id != id for u in usuarios):
            flash('Este email já está cadastrado para outro usuário!', 'error')
            return redirect(url_for('editar', id=id))
            
        usuario.nome = nome
        usuario.email = email
        usuario.telefone = telefone
        flash('Usuário alterado com sucesso!', 'success')
        return redirect(url_for('index'))
    return render_template('editar.html', usuario=usuario)

@app.route('/deletar/<int:id>', methods=['POST'])  # Adicionada a barra faltante
def deletar(id):
    global usuarios
    usuario = next((u for u in usuarios if u.id == id), None)
    if not usuario:
        flash('Usuário não encontrado!', 'error')
        return redirect(url_for('index'))
        
    usuarios = [u for u in usuarios if u.id != id]
    flash('Usuário deletado com sucesso', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)