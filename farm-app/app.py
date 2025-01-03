from flask import Flask, render_template, request, redirect, url_for, flash, session
import uuid

app = Flask(__name__)
app.secret_key = 'nexusurbanfarm'  # Chave secreta para gerenciar sessões

# Classe para o Usuário
class Usuario:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    # Método para validar login
    def validar_login(self, login_code, password):
        return self.username == login_code and self.password == password

# Criando um usuário padrão
usuario_admin = Usuario("admin", "1234")

# Rota para a página de login
@app.route('/')
def login():
    return render_template('login.html')

# Rota para processar o login
@app.route('/login', methods=['POST'])
def do_login():
    login_code = request.form['login_code']
    password = request.form['password']
    
    if usuario_admin.validar_login(login_code, password):
        session['username'] = login_code  # Armazena o nome do usuário na sessão
        return redirect(url_for('home'))
    else:
        flash('Login inválido. Tente novamente.')
        return redirect(url_for('login'))

# Rota para a página inicial após login
@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', username=session['username'])

# Classe para gerenciar rotas de fornecedores
class Fornecedor:
    def __init__(self, app):
        self.app = app
        self.fornecedores_data = []  # Lista de fornecedores (armazena dados temporariamente)
        self.codigo_fornecedor_atual = 1  # Inicia o contador de códigos em um valor simples
        self.register_routes()

    def register_routes(self):
        # Rota para a página de fornecedores
        @self.app.route('/fornecedores')
        def fornecedores():
            if 'username' not in session:
                return redirect(url_for('login'))
            # Passa a lista `fornecedores_data` para a página de fornecedores
            return render_template('fornecedores.html', fornecedores=self.fornecedores_data)

        # Rota para adicionar fornecedor
        @self.app.route('/add_fornecedor')
        def add_fornecedor():
            if 'username' not in session:
                return redirect(url_for('login'))
            
            # Gerar o código do fornecedor automaticamente (sequencial)
            codigo_fornecedor = self.gerar_codigo_fornecedor()  # Gera um código numérico sequencial
            return render_template('add_fornecedor.html', codigo=codigo_fornecedor)

        # Rota para salvar fornecedor
        @self.app.route('/save_fornecedor', methods=['POST'])
        def save_fornecedor():
            if 'username' not in session:
                return redirect(url_for('login'))

            # Processa os dados do formulário de fornecedor
            fornecedor = {
                'codigo': request.form['codigo'],
                'cnpj': request.form['cnpj'],
                'razao_social': request.form['razao_social'],
                'nome_fantasia': request.form['nome_fantasia'],
                'status': request.form['status'],
                'cep': request.form['cep'],
                'cidade': request.form['cidade'],
                'bairro': request.form['bairro'],
                'rua': request.form['rua'],
                'numero': request.form['numero'],
                'complemento': request.form.get('complemento', ''),
                'telefone': request.form['telefone'],
                'email': request.form['email'],
                'nome_representante': request.form['nome_representante']
            }

            # Adiciona o fornecedor na lista de dados
            self.fornecedores_data.append(fornecedor)

            flash('Fornecedor salvo com sucesso!')
            return redirect(url_for('fornecedores'))

    def gerar_codigo_fornecedor(self):
        # Gera um código sequencial para o fornecedor
        codigo = self.codigo_fornecedor_atual
        self.codigo_fornecedor_atual += 1  # Incrementa o contador para o próximo fornecedor
        return str(codigo)  # Retorna o código como string para o formulário

# Inicializando o controlador de fornecedores
fornecedor_controller = Fornecedor(app)

# Classe para gerenciar rotas de insumos
class Insumos:
    def __init__(self, app):
        self.app = app
        self.register_routes()

    def register_routes(self):
        # Rota para a página de insumos
        @self.app.route('/insumos')
        def insumos():
            if 'username' not in session:
                return redirect(url_for('login'))
            return render_template('insumos.html')

        # Rota para adicionar insumo
        @self.app.route('/add_insumo')
        def add_insumo():
            if 'username' not in session:
                return redirect(url_for('login'))
            return render_template('add_insumo.html')

        # Rota para salvar insumo
        @self.app.route('/save_insumo', methods=['POST'])
        def save_insumo():
            if 'username' not in session:
                return redirect(url_for('login'))

            # Processa os dados do formulário de insumo
            nome = request.form['nome']  # Nome do insumo
            tipo = request.form['tipo']  # Tipo do insumo
            quantidade = request.form['quantidade']  # Quantidade disponível
            fornecedor = request.form['fornecedor']  # Fornecedor
            status = request.form['status']  # Status (ativo/inativo)

            # Armazena os dados no banco de dados ou outra estrutura
            # Aqui você deve incluir a lógica para salvar os dados no banco de dados

            flash('Insumo salvo com sucesso!')
            return redirect(url_for('insumos'))

# Inicializando o controlador de insumos
insumos_controller = Insumos(app)

# Classe para gerenciar rotas de clientes
class Clientes:
    def __init__(self, app):
        self.app = app
        self.clientes_data = []  # Lista de clientes (armazena dados temporariamente)
        self.codigo_cliente_atual = 1000  # Inicia o contador de códigos em um valor simples
        self.register_routes()

    def register_routes(self):
        # Rota para a página de clientes
        @self.app.route('/clientes')
        def clientes():
            if 'username' not in session:
                return redirect(url_for('login'))
            # Passa a lista `clientes_data` para a página de clientes
            return render_template('clientes.html', clientes=self.clientes_data)

        # Rota para adicionar cliente
        @self.app.route('/add_cliente')
        def add_cliente():
            if 'username' not in session:
                return redirect(url_for('login'))
            
            # Gerar o código do cliente automaticamente (sequencial)
            codigo_cliente = self.gerar_codigo_cliente()  # Gera um código numérico sequencial
            return render_template('add_cliente.html', codigo=codigo_cliente)

        # Rota para salvar cliente
        @self.app.route('/save_cliente', methods=['POST'])
        def save_cliente():
            if 'username' not in session:
                return redirect(url_for('login'))

            # Captura os dados do formulário
            status = request.form['status']  # Obtém o valor do status
            print("Status recebido:", status)  # Linha de debug para verificar o valor do status

            cliente = {
                'codigo': request.form['codigo'],
                'razao_social': request.form['razao_social'],
                'nome_fantasia': request.form.get('nome_fantasia', ''),
                'cnpj': request.form['cnpj'],
                'status': status,  # Usa o valor recebido diretamente
                'cep': request.form['cep'],
                'estado': request.form['estado'],
                'cidade': request.form['cidade'],
                'bairro': request.form['bairro'],
                'rua': request.form['rua'],
                'numero': request.form['numero'],   
                'complemento': request.form.get('complemento', ''),
                'telefone': request.form['telefone'],
                'email': request.form['email'],
                'nome_representante': request.form['nome_representante']
            }

            # Adiciona o cliente na lista de dados
            self.clientes_data.append(cliente)
            
            flash('Cliente salvo com sucesso!')
            return redirect(url_for('clientes'))

    def gerar_codigo_cliente(self):
        # Gera um código sequencial para o cliente
        codigo = self.codigo_cliente_atual
        self.codigo_cliente_atual += 1  # Incrementa o contador para o próximo cliente
        return str(codigo)  # Retorna o código como string para o formulário


# Inicializando o controlador de clientes
clientes_controller = Clientes(app)

# Classe para gerenciar rotas de funcionários
class Funcionarios:
    def __init__(self, app):
        self.app = app
        self.equipes = ["Equipe A", "Equipe B", "Equipe C"]
        self.funcionarios_data = []  # Lista para armazenar os funcionários
        self.register_routes()

    def register_routes(self):
        # Rota para a página de funcionários
        @self.app.route('/funcionarios')
        def funcionarios():
            if 'username' not in session:
                return redirect(url_for('login'))
            # Passa a lista de funcionários para a página
            return render_template('funcionarios.html', funcionarios=self.funcionarios_data)

        # Rota para adicionar funcionário
        @self.app.route('/add_funcionario')
        def add_funcionario():
            if 'username' not in session:
                return redirect(url_for('login'))
            
            # Gerar o ID do funcionário automaticamente
            codigo_funcionario = str(uuid.uuid4())  # Gera um UUID como código
            return render_template('add_funcionario.html', equipes=self.equipes, codigo=codigo_funcionario)

        # Rota para salvar funcionário
        @self.app.route('/save_funcionario', methods=['POST'])
        def save_funcionario():
            if 'username' not in session:
                return redirect(url_for('login'))

            # Processa os dados do formulário de funcionário
            funcionario = {
                'codigo': request.form['codigo'],
                'nome': request.form['nome'],
                'cpf': request.form['cpf'],
                'cargo': request.form['cargo'],
                'status': request.form['status'],
                'equipe': request.form['equipe'],
            }

            # Adiciona o funcionário na lista de funcionários
            self.funcionarios_data.append(funcionario)

            flash('Funcionário salvo com sucesso!')
            return redirect(url_for('funcionarios'))

# Inicializando o controlador de funcionários
funcionarios_controller = Funcionarios(app)

# Classe para gerenciar rotas de equipes
class Equipes:
    def __init__(self, app):
        self.app = app
        self.register_routes()

    def register_routes(self):
        # Rota para a página de equipes
        @self.app.route('/equipes')
        def equipes():
            if 'username' not in session:
                return redirect(url_for('login'))
            return render_template('equipes.html')

        # Rota para adicionar equipe
        @self.app.route('/add_equipes')
        def add_equipes():
            if 'username' not in session:
                return redirect(url_for('login'))
            return render_template('add_equipes.html')

        # Rota para salvar equipe
        @self.app.route('/save_equipe', methods=['POST'])
        def save_equipe():
            if 'username' not in session:
                return redirect(url_for('login'))

            # Processa os dados do formulário de equipe
            nome_equipe = request.form['nome_equipe']
            lider = request.form['lider']
            email_lider = request.form['email_lider']

            # Lógica para salvar os dados no banco de dados ou estrutura de dados

            flash('Equipe salva com sucesso!')
            return redirect(url_for('equipes'))

# Inicializando o controlador de equipes
equipes_controller = Equipes(app)

from flask import Flask, render_template, request, redirect, url_for, session, flash

# Classe para gerenciar rotas de compras
class Compras:
    def __init__(self, app):
        self.app = app
        self.compras_data = []  # Lista de compras (armazena dados temporariamente)
        self.codigo_compra_atual = 1  # Inicia o contador de códigos em um valor simples
        self.register_routes()

    def register_routes(self):
        # Rota para a página de compras
        @self.app.route('/compras')
        def compras():
            if 'username' not in session:
                return redirect(url_for('login'))
            
            # Exemplo de dados de compras
            compras_data = self.compras_data  # Usando a lista de compras armazenadas
            return render_template('compras.html', compras=compras_data)

        # Rota para adicionar compra
        @self.app.route('/add_compra')
        def add_compra():
            if 'username' not in session:
                return redirect(url_for('login'))

            # Gerar o código automaticamente para a compra
            codigo = self.gerar_codigo_compra()  # Gera um código numérico sequencial
            return render_template('add_compras.html', codigo=codigo)

        # Rota para salvar compra
        @self.app.route('/save_compra', methods=['POST'])
        def save_compra():
            if 'username' not in session:
                return redirect(url_for('login'))

            # Processa os dados do formulário de compra
            codigo = request.form['codigo']
            fornecedor = request.form['fornecedor']
            produtos = request.form['produtos']  # Lista de produtos
            status = request.form['status']  # Status da compra

            # Lógica para armazenar os dados no banco de dados (aqui estamos apenas armazenando na lista)
            compra = {
                'codigo': codigo,
                'fornecedor': fornecedor,
                'produtos': produtos,
                'status': status,
                'data': '2024-10-01'  # Data de exemplo, pode ser alterada conforme a necessidade
            }

            # Adiciona a compra na lista de compras
            self.compras_data.append(compra)

            flash('Compra salva com sucesso!')
            return redirect(url_for('compras'))

        # Rota para visualizar compra
        @self.app.route('/view_compra/<codigo>')
        def view_compra(codigo):
            if 'username' not in session:
                return redirect(url_for('login'))
            
            # Busca a compra pelo código
            compra = next((compra for compra in self.compras_data if compra['codigo'] == codigo), None)
            if compra is None:
                return "Compra não encontrada", 404

            return render_template('view_compra.html', compra=compra)

        # Rota para editar compra
        @self.app.route('/edit_compra/<codigo>', methods=['GET', 'POST'])
        def edit_compra(codigo):
            if 'username' not in session:
                return redirect(url_for('login'))

            # Busca a compra pelo código
            compra = next((compra for compra in self.compras_data if compra['codigo'] == codigo), None)
            if compra is None:
                return "Compra não encontrada", 404

            if request.method == 'POST':
                # Atualiza os dados da compra
                compra['fornecedor'] = request.form['fornecedor']
                compra['produtos'] = request.form['produtos']
                compra['status'] = request.form['status']
                flash('Compra atualizada com sucesso!')
                return redirect(url_for('compras'))

            return render_template('edit_compra.html', compra=compra)

    def gerar_codigo_compra(self):
        # Gera um código sequencial para a compra
        codigo = self.codigo_compra_atual
        self.codigo_compra_atual += 1  # Incrementa o contador para a próxima compra
        return str(codigo)  # Retorna o código como string para o formulário

# Inicializando o controlador de compras
compras_controller = Compras(app)


# Classe para gerenciar rotas de vendas
class Vendas:
    def __init__(self, app):
        self.app = app
        self.vendas_data = []  # Lista de vendas (armazena dados temporariamente)
        self.codigo_venda_atual = 1  # Inicia o contador de códigos em um valor simples
        self.register_routes()

    def register_routes(self):
        # Rota para a página de vendas
        @self.app.route('/vendas')
        def vendas():
            if 'username' not in session:
                return redirect(url_for('login'))
            
            # Dados de exemplo de vendas
            vendas_data = self.vendas_data  # Usando a lista de vendas armazenadas
            return render_template('vendas.html', vendas=vendas_data)

        # Rota para adicionar venda
        @self.app.route('/add_venda')
        def add_venda():
            if 'username' not in session:
                return redirect(url_for('login'))
            
            # Gera um ID sequencial para a nova venda
            venda_id = self.gerar_codigo_venda()  # Gera um código numérico sequencial
            return render_template('add_vendas.html', id=venda_id)

        # Rota para salvar venda
        @self.app.route('/save_venda', methods=['POST'])
        def save_venda():
            if 'username' not in session:
                return redirect(url_for('login'))

            # Processa os dados do formulário de venda
            cliente = request.form['cliente']
            data_envio = request.form['data_envio']
            status = request.form['status']
            produtos = request.form.getlist('produtos')

            venda_data = {
                'id': request.form['id'],  # ID da venda gerado sequencialmente
                'cliente': cliente,
                'data_envio': data_envio,
                'status': status,
                'produtos': produtos
            }

            # Adiciona a venda à lista de vendas
            self.vendas_data.append(venda_data)

            flash('Venda salva com sucesso!')
            return redirect(url_for('vendas'))

        # Rota para visualizar venda
        @self.app.route('/view_venda/<id>')
        def view_venda(id):
            if 'username' not in session:
                return redirect(url_for('login'))
            
            # Busca a venda pelo ID
            venda = next((venda for venda in self.vendas_data if venda['id'] == id), None)
            if venda is None:
                return "Venda não encontrada", 404

            return render_template('view_venda.html', venda=venda)

        # Rota para editar venda
        @self.app.route('/edit_venda/<id>', methods=['GET', 'POST'])
        def edit_venda(id):
            if 'username' not in session:
                return redirect(url_for('login'))

            # Busca a venda pelo ID
            venda = next((venda for venda in self.vendas_data if venda['id'] == id), None)
            if venda is None:
                return "Venda não encontrada", 404

            if request.method == 'POST':
                # Atualiza os dados da venda
                venda['cliente'] = request.form['cliente']
                venda['data_envio'] = request.form['data_envio']
                venda['status'] = request.form['status']
                venda['produtos'] = request.form.getlist('produtos')
                flash('Venda atualizada com sucesso!')
                return redirect(url_for('vendas'))

            return render_template('edit_venda.html', venda=venda)

    def gerar_codigo_venda(self):
        # Gera um código sequencial para a venda
        codigo = self.codigo_venda_atual
        self.codigo_venda_atual += 1  # Incrementa o contador para a próxima venda
        return str(codigo)  # Retorna o código como string para o formulário

# Inicializando o controlador de vendas
vendas_controller = Vendas(app)


# Classe para gerenciar rotas de produção
class Producao:
    def __init__(self, app):
        self.app = app
        self.register_routes()

    def register_routes(self):
        # Rota para a página de produção
        @self.app.route('/producao')
        def producao():
            if 'username' not in session:
                return redirect(url_for('login'))

            producoes = [
                {
                    "nome": "Alface", "classe": "Hortaliça", "tempo_maturacao": 4,
                    "medida_tempo": "semanas", "umidade": 80, "temperatura": 20,
                    "nivel_luz": "Moderado", "ultima_colheita": "2024-10-01",
                    "proxima_colheita": "2024-11-01", "estoque": 100, "status": "Ativo"
                },
                {
                    "nome": "Laranja", "classe": "Fruta", "tempo_maturacao": 12,
                    "medida_tempo": "meses", "umidade": 75, "temperatura": 25,
                    "nivel_luz": "Alto", "ultima_colheita": "2024-09-15",
                    "proxima_colheita": "2024-11-15", "estoque": 150, "status": "Ativo"
                },
                {
                    "nome": "Beterraba", "classe": "Legume", "tempo_maturacao": 6,
                    "medida_tempo": "semanas", "umidade": 85, "temperatura": 18,
                    "nivel_luz": "Baixo", "ultima_colheita": "2024-08-20",
                    "proxima_colheita": "2024-10-20", "estoque": 50, "status": "Inativo"
                }
            ]

            return render_template('producao.html', producoes=producoes)

        # Rota para adicionar nova produção
        @self.app.route('/add_producao')
        def add_producao():
            if 'username' not in session:
                return redirect(url_for('login'))
            return render_template('add_producao.html')

        # Rota para salvar produção
        @self.app.route('/save_producao', methods=['POST'])
        def save_producao():
            if 'username' not in session:
                return redirect(url_for('login'))
            
            nome = request.form['nome']
            classe = request.form['classe']
            tempo_maturacao = request.form['tempo_maturacao']
            medida_tempo = request.form['medida_tempo']
            umidade = request.form['umidade']
            temperatura = request.form['temperatura']
            nivel_luz = request.form['nivel_luz']
            ultima_colheita = request.form['ultima_colheita']
            proxima_colheita = request.form['proxima_colheita']
            estoque = request.form['estoque']
            status = request.form['status']

            flash('Produção adicionada com sucesso!')
            return redirect(url_for('producao'))

# Inicializando o controlador de produção
producao_controller = Producao(app)

# Rota para deslogar
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove o nome do usuário da sessão
    return redirect(url_for('login'))  # Redireciona para a página de login

if __name__ == '__main__':
    app.run(debug=True)  # Executa o aplicativo em modo de depuração