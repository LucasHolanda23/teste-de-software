from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'chave-secreta'

# teste usuarios
USUARIOS = {'admin': 'admin123', 'estudante': 'senha123'}

#ele verifica se existe um usuario na sessao, se nao, e lancado de volta para login
@app.route('/')
def home():
    if 'usuario' in session:
        return redirect(url_for('calculadora'))
    return redirect(url_for('login'))

#aqui ele aceita o metodo get e post. se o usuario e a senha batarem, usuario e direcionando a pag home(calculadora)
@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        u, s = request.form.get('username'), request.form.get('password')
        if USUARIOS.get(u) == s:
            session['usuario'] = u
            return redirect(url_for('calculadora'))
        erro = 'Usuário ou senha inválidos!'
    return render_template('login.html', erro=erro)
#recebe o metodo get e post, e verifica se ja existe um USUARIO cadastrado na listagem, se n ouver, ele passa
@app.route('/register', methods=['GET', 'POST'])
def register():
    erro = None
    if request.method == 'POST':
        u, s = request.form.get('username'), request.form.get('password')
        if u in USUARIOS:
            erro = 'Este usuário já existe!'
        else:
            USUARIOS[u] = s
            session['usuario'] = u
            return redirect(url_for('calculadora'))
    return render_template('register.html', erro=erro)
# aqui e pagina home, ainda sem nada        
@app.route('/calculadora')
def calculadora():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('calculadora.html', usuario=session['usuario'])
#aqui e o botao de saida que limpa/esquece o usuario da sessao e manda de volta para o login
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
#aqui inicia o servidor, nao mexa
if __name__ == '__main__':
    app.run(debug=True)
