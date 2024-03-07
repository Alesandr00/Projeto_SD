from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta'

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
