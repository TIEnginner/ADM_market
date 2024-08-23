import PySimpleGUI as sg
import json
import os
import pandas as pd
import time

# Definindo o tema
sg.theme('DarkBlue')

# Arquivo JSON e dados padrão
json_file = 'dados_salvos_supermegado.json'
usuario_file = 'dados_usuario.json'

def load_users():
    if os.path.exists(usuario_file):
        with open(usuario_file, 'r') as file:
            return json.load(file)
    return {}

def save_users(users):
    with open(usuario_file, 'w') as file:
        json.dump(users, file, indent=4)



def remove_user(users, selected_user):
    if selected_user in users:
        del users[selected_user]
        save_users(users)
    return users

def setup_window(users):
    layout = [
     
        [sg.Button("Remover Usuário", font=("Arial", 12)),sg.Button('Sair')],
        [sg.Listbox(values=list(users.keys()), key='-USERLIST-', font=("Arial", 12), size=(60, 10), select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)]
    ]
    return sg.Window("Gerenciamento de Usuários", layout)
def js():
    janela = sg.Window('Tela Inicial', tela_inicial(), size=(480, 300))
def começar():
    users = load_users()
    window = setup_window(users)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Sair':
            window.close()
            return('2')
            break
           
            
            
        elif event == "Remover Usuário":
            selected_user_index = window['-USERLIST-'].get_indexes()
            if selected_user_index:
                selected_user = window['-USERLIST-'].get_list_values()[selected_user_index[0]]
                users = remove_user(users, selected_user)
                window['-USERLIST-'].update(list(users.keys()))

    window.close()
data = {
    "1": [""] * 35,
    "2": [""] * 35,
    "3": [""] * 35,
    "4": [""] * 35,
    "5": [""] * 35,
    "6": [""] * 35,
    "7": [""] * 35,
    "8": [""] * 35,
    "9": [""] * 35,
    "10": [""] * 35,
    "11": [""] * 35,
    "12": [""] * 35,
}

class AgendaApp:
    def __init__(self):
        self.filename = "produto.json"
        self.tasks = self.load_tasks()
        self.filenam = "categoria.json"
        self.categories = self.load_categories()
        self.setup_produto()

    def load_categories(self):
        if os.path.exists(self.filenam):
            with open(self.filenam, 'r') as file:
                return json.load(file)
        return []

    def setup_produto(self):
        layout = [
            [sg.Text("Codigo do produto", font=("Arial", 12)),sg.Input(key = 'codigo',enable_events=True)],
            [sg.Text("Data de validade", font=("Arial", 12)),
             sg.Input(key='-DATE-', size=(12, 1), font=("Arial", 12), disabled=True),
             sg.CalendarButton("Selecionar Data", target='-DATE-', format="%d/%m/%Y", font=("Arial", 12))],
            [sg.Text("Fornecedor", font=("Arial", 12)), sg.Input(key='fornecedor')],
            [sg.Text("Categoria", font=("Arial", 12)),
             sg.Combo(self.categories, key='-CATEGORIA-', font=("Arial", 12), size=(40, 1))],
            [sg.Text("Produto", font=("Arial", 12)),
             sg.Input(key='-TASK-', font=("Arial", 12), size=(40, 1))],
            [sg.Text("Preço", font=("Arial", 12)),
             sg.Input(key='-VALOR-', font=("Arial", 12), size=(40, 1), enable_events=True)],
            [sg.Text("Quantidade", font=("Arial", 12)),
             sg.Input(key='-QUANTIDADE-', font=("Arial", 12), size=(40, 1), enable_events=True)],
            [sg.Button("Adicionar", font=("Arial", 12)),
             sg.Button("Remover Produto", font=("Arial", 12)),
             sg.Button("Alterar Produto", font=("Arial", 12)),
             sg.Button("Adicionar Categoria", font=("Arial", 12)),sg.Button("Adicionar Forma de pagamento", font=("Arial", 12))],
            [sg.Listbox(values=self.tasks, key='-TASKLIST-', font=("Arial", 12), size=(60, 10), select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)]
        ]

        self.window = sg.Window("Gerenciamento de Produtos", layout)

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                return json.load(file)
        return []

    def save_tasks(self):
        with open(self.filename, 'w') as file:
            json.dump(self.window['-TASKLIST-'].get_list_values(), file)

    def add_task(self,codigo, date, fornecedor, categoria, task, valor, quantidade):
        if date and fornecedor and categoria and task and valor and quantidade:
            from datetime import datetime
            date_format = "%d/%m/%Y"
            date_validade = datetime.strptime(date, date_format)
   
            now = datetime.now()
       

            if date_validade < now:
                    sg.popup("A data de validade não pode ser menor que a data atual.",title = 'Erro')
                    return
            time = now.strftime("%d/%m/%Y %H:%M:%S")

            formatted_task = f"{codigo} - {date} - {fornecedor} - {categoria} - {task} - {valor} - {quantidade} - {time}"
            current_tasks = self.window['-TASKLIST-'].get_list_values()
            updated_tasks = current_tasks + [formatted_task]
            self.window['-TASKLIST-'].update(updated_tasks)
            self.save_tasks()
            self.window['codigo'].update('')
            self.window['-DATE-'].update('')
            self.window['fornecedor'].update('')
            self.window['-CATEGORIA-'].update('')
            self.window['-TASK-'].update('')
            self.window['-VALOR-'].update('')
            self.window['-QUANTIDADE-'].update('')

    def remove_task(self):
        selected_task = self.window['-TASKLIST-'].get_indexes()
        if selected_task:
            current_tasks = self.window['-TASKLIST-'].get_list_values()
            del current_tasks[selected_task[0]]
            self.window['-TASKLIST-'].update(current_tasks)
            self.save_tasks()

    def alterar_task(self):
        selected_task_index = self.window['-TASKLIST-'].get_indexes()
        if selected_task_index:
            selected_task = self.window['-TASKLIST-'].get_list_values()[selected_task_index[0]]
            parts = selected_task.split(" - ")
            if len(parts) == 8:
                codigo ,date, fornecedor, categoria, task, valor, quantidade, _ = parts
               
                self.window['codigo'].update(codigo)
                self.window['-DATE-'].update(date)
                self.window['fornecedor'].update(fornecedor)
                self.window['-CATEGORIA-'].update(categoria)
                self.window['-TASK-'].update(task)
                self.window['-VALOR-'].update(valor)
                self.window['-QUANTIDADE-'].update(quantidade)

                current_tasks = self.window['-TASKLIST-'].get_list_values()
                del current_tasks[selected_task_index[0]]
                self.window['-TASKLIST-'].update(current_tasks)
                self.save_tasks()

    def run(self):
        while True:
            event, values = self.window.read()

            if event == sg.WIN_CLOSED:
                break
            elif event == "Adicionar":
                self.add_task(values['codigo'],values['-DATE-'], values['fornecedor'], values['-CATEGORIA-'], values['-TASK-'], values['-VALOR-'], values['-QUANTIDADE-'])
            elif event == "Remover Produto":
                self.remove_task()
            elif event == "Alterar Produto":
                self.alterar_task()
            elif event == "Adicionar Categoria":
                self.window.hide() 
                TelaCadastro().run() 
                self.window.un_hide() 
            elif event == 'codigo':
                quantidade = values['codigo']
                if not quantidade.isdigit():
                    self.window['codigo'].update(quantidade[:-1])
            elif event == '-VALOR-':
                valor = values['-VALOR-']
                if not valor.replace('.', '', 1).isdigit():
                    self.window['-VALOR-'].update(valor[:-1])

            elif event == '-QUANTIDADE-':
                quantidade = values['-QUANTIDADE-']
                if not quantidade.isdigit():
                    self.window['-QUANTIDADE-'].update(quantidade[:-1])

        self.window.close()


class TelaCadastro:
    def __init__(self):
        self.filename = "categoria.json"
        self.tasks = self.load_tasks()
        self.setup_agenda()

    def setup_agenda(self):
        layout = [
            [sg.Text("Categoria", font=("Arial", 12)), sg.Input(key='-TASK-', font=("Arial", 12), size=(40, 1))],
            [sg.Button("Adicionar Categoria", font=("Arial", 12)), sg.Button("Remover Categoria", font=("Arial", 12))],
            [sg.Listbox(values=self.tasks, key='-TASKLIST-', font=("Arial", 12), size=(60, 10), select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)]
        ]

        self.window = sg.Window("Adicionar Categoria", layout)

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                return json.load(file)
        return []

    def save_tasks(self):
        with open(self.filename, 'w') as file:
            json.dump(self.window['-TASKLIST-'].get_list_values(), file)

    def add_task(self, task):
        if task:
            current_tasks = self.window['-TASKLIST-'].get_list_values()
            if task not in current_tasks:
                updated_tasks = current_tasks + [task]
                self.window['-TASKLIST-'].update(updated_tasks)
                self.save_tasks()

    def remove_task(self):
        selected_task = self.window['-TASKLIST-'].get_indexes()
        if selected_task:
            current_tasks = self.window['-TASKLIST-'].get_list_values()
            del current_tasks[selected_task[0]]
            self.window['-TASKLIST-'].update(current_tasks)
            self.save_tasks()

    def run(self):
        while True:
            event, values = self.window.read()

            if event == sg.WIN_CLOSED:
                break
            elif event == "Adicionar Categoria":
                self.add_task(values['-TASK-'])
                self.window['-TASK-'].update('')
            elif event == "Remover Categoria":
                self.remove_task()

        self.window.close()
   
def load_tasks():
        if os.path.exists('produto.json'):
            with open('produto.json', 'r') as file:
                return json.load(file)
        return []
    
def dados_pessoas():
    if not os.path.exists(usuario_file):
        return {}
    with open(usuario_file, 'r') as valor_json:
        return json.load(valor_json)

def verificar_usuario(usu, senha):
    dados = dados_pessoas()
    if usu in dados:
        if dados[usu].get(senha) in ['personal', 'usuario']:
            return dados[usu][senha]
    return None

def tela_Login():
    return [
        [sg.Text('Usuario')],
        [sg.Input(key='-nome-')],
        [sg.Text('Senha')],
        [sg.Input(key='-senha-', password_char='*')],
        [sg.Button('OK'), sg.Button('Cancelar'), sg.Button('Cadastrar')]
    ]

def tela_Cadastro():
    return [
        [sg.Text('Usuario')],
        [sg.Input(key='-nome-')],
        [sg.Text('Senha')],
        [sg.Input(key='-senha-', password_char='*')],
        [sg.Text('Repetir Senha')],
        [sg.Input(key='-senha_rep-', password_char='*')],
        [sg.Radio("Usuario", "1", default=True, key='usuario'), sg.Radio("funcionarios", '1', key='personal')],
        [sg.Button('Cadastrar'), sg.Button('Cancelar')]
    ]

def tela_Cadastro_2():
    return [
        [sg.Text('Senha')],
        [sg.Input(key='-senha-', password_char='*')],
        [sg.Button('Ok'), sg.Button('Cancelar')]
    ]

def loja():
    return [
        [sg.Text('Data de validade que voce deseja para ser notificada')],
        [sg.Input(key='nome')],
        [sg.Button('Adicionar'), sg.Button('Cancelar')]
    ]

def tela_inicial():
    return [
        [sg.Button('?')],
        [sg.Text('Numero para excluir um pedido de compra'), sg.Text('0872',key='-pesquisa-')],
        [sg.Text('Numero para cancelar uma comprar'), sg.Text('0806107',key='-pesquisa-')],
        [sg.Button('loja', key='-loja-'), sg.Button('Estoque', key='-estoque-'), sg.Button('Gerenciamento de produto', key='-produto-')],
        [sg.Button('Planilha', key='-excel-'), sg.Button('Excluir funcionario', key='-excluir-')]
    ]

df = pd.DataFrame(data)



def criar_layout_planilha():
    layout = []
    for i in range(len(df)):
        row = []
        for col in df.columns:
        
            row.append(sg.InputText(default_text=df[col].iloc[i], key=(i, col), size=(20, 1)))
        layout.append(row)
    layout.append([sg.Button('Salvar'), sg.Button('Carregar'), sg.Button('Limpar'), sg.Button('Sair')])
    return layout

def criar_layout_planilha():
    layout = []
    for i in range(len(df)):
        row = []
        for col in df.columns:
           
            row.append(sg.InputText(default_text=df[col].iloc[i], key=(i, col), size=(20, 1)))
        layout.append(row)
    layout.append([sg.Button('Salvar'), sg.Button('Carregar'), sg.Button('Limpar'), sg.Button('Sair')])
    return layout

def tela_usuario():
    return [
        [sg.Button('Remover'),sg.Button('Excluir Compra')],
        [sg.Listbox(values='tasks', key='-produtos-', font=("Arial", 12), size=(60, 10), select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)],
        [sg.Text('Total de itens'),sg.Text('',key ='quantidade' )],
        [sg.Text('Valor'),sg.Text('',key ='preço')],
        [sg.Text('Forma de pagamento'),sg.Combo('-forma_de_pagamento-', key='-CATEGORIA-', font=("Arial", 12), size=(40, 1))],
        [sg.Text('Produto codigo'),sg.Input(key = '-INPUT-',enable_events=True)]
        
        

    ]
def tela_para_excluir_produto():
    return[[sg.Text('Senha para excluir produto')],
           [sg.Input(key = '-senha-')],
           [sg.Button('Excluir'),sg.Button('Sair')]]
    
def exibir_planilha():
    layout = criar_layout_planilha()
    window = sg.Window('Planilha Interativa e Editável', layout)

    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED or event == 'Sair':
            break
        
        if event == 'Salvar':
 
            for i in range(len(df)):
                for col in df.columns:
             
                    if (i, col) in values:
                        df.at[i, col] = values[(i, col)]
            

            with open(json_file, 'w') as f:
                json.dump(df.to_dict(), f)
            sg.popup('Dados salvos com sucesso!')
        
        if event == 'Carregar':
  
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                for i in range(len(df)):
                    for col in df.columns:
                        if (i, col) in window.AllKeysDict:
                            window[(i, col)].update(data[col][str(i)])
                sg.popup('Dados carregados com sucesso!')
            except FileNotFoundError:
                sg.popup('Nenhum arquivo salvo encontrado!')

        if event == 'Limpar':
      
            for i in range(len(df)):
                for col in df.columns:
                    if (i, col) in window.AllKeysDict:  
                        window[(i, col)].update("")
            sg.popup('Dados limpos!')

    window.close()


janela = sg.Window('Login', tela_Login())

while True:
    event, values = janela.read()
    
    if event == sg.WIN_CLOSED or event == 'Cancelar':
        break
    
    if event == 'OK' or event == '\r' :
        usu = values['-nome-']
        senha = values['-senha-']
        papel = verificar_usuario(usu, senha)
        
        if papel == 'personal':
            janela.close()
            janela = sg.Window('Tela Inicial', tela_inicial(), size=(480, 300))
            while True:
                eventos, valor = janela.read()
                
                if eventos == sg.WIN_CLOSED:
                    break
                
                if eventos == '?':
                    janela.close()
                    janela = sg.Window('Adicionar validade minima faltande', loja())
                    while True:
                        evento, valor = janela.read()
                        if evento == sg.WIN_CLOSED or evento == 'Cancelar':
                            janela.close()
                            janela = sg.Window('Tela Inicial', tela_inicial(), size=(480, 300))
                            break
                        if evento == 'Adicionar':
                            if not valor['nome']:
                                sg.popup('Por favor, preencha todos os campos.')
                            else:
                                with open('arquivos.json', 'w') as arquivo_json:
                                    json.dump({'nome': valor['nome']}, arquivo_json, indent=4)
                                sg.popup('Nome da academia registrado com sucesso.')
                                janela.close()
                                janela = sg.Window('Tela Inicial', tela_inicial(), size=(480, 300))
                                break
                if eventos == '-estoque-':
                    app = AgendaApp()
                    app.run()
                if eventos == '-excel-':
                    janela.hide()
                    exibir_planilha()
                    janela.un_hide()
                if eventos == '-excluir-':
                    janela.close()
                    while True:
                      b =  começar()
                      if b == '2':
                          
                          janela = sg.Window('Tela Inicial', tela_inicial(), size=(480,300))
                          break
                if eventos == 'Gerenciamento de produto':
                    janela.close()
                    pass
                 
        
        
        
        
        
        
        
        if papel == 'usuario':
            input_buffer = ""
            input_start_time = time.time()
            is_scanning = False
            janela = sg.Window('Tela Inicial', tela_usuario(), size=(900,700),finalize=True)
            while True:
                eventos, valor = janela.read()
                if eventos == sg.WIN_CLOSED:
                    break
                if eventos == 'Remover':
                       selected_task =janela[''].get_indexes()
                       if selected_task:
                            window = sg.Window('Senha',tela_para_excluir_produto())
                            while True:
                                evento,valor = window.read()
                                if evento == sg.WINDOW_CLOSED or evento == 'Sair':
                                    break
                                if evento == 'Excluir':
                                    if valor['senha'] == '0872':
                                        current_tasks = janela['-produtos-'].get_list_values()
                                        del current_tasks[selected_task[0]]
                                        janela['-produtos-'].update(current_tasks)
                                        window.close()
                                        break        
                                    else:
                                        sg.popup('Senha invalida',title= 'Erro')
                if eventos =='Excluir Compra':
                      window = sg.Window('Senha',tela_para_excluir_produto())
                      while True:
                                evento,valor = window.read()
                                if evento == sg.WINDOW_CLOSED or evento == 'Sair':
                                    break
                                if evento == 'Excluir':
                                    if valor['senha'] == '0806107':
                                        current_tasks = janela['-produtos-'].get_list_values()
                                        del current_tasks
                                        try:
                                            janela['-produtos-'].update(current_tasks)
                                            window.close()
                                            break    
                                        except:
                                                janela['-produtos-'].update('')
                                                window.close()
                                                break
                                    else:
                                        sg.popup('Senha invalida',title= 'Erro')
            

                if eventos == sg.WIN_CLOSED or eventos == 'Sair':
                    break

                if eventos == '\r':
                    if not '-INPUT-':
                        sg.popup('Nenhum produto selecionado',title= 'Erro')
                    else:
                        user_input = valor['-INPUT-'].strip()
                        if user_input:
                            if user_input in load_tasks():
                            
                                window['-INPUT-'].update('')
                            else: 
                                window['-INPUT-'].update('')
                                sg.popup('Não a esse produto no estoque',title = 'Erro')
                        continue

             
                current_time = time.time()
                if current_time - input_start_time > 0.1:
           
                    input_buffer = ""
                    input_start_time = current_time

                if eventos == '-INPUT-':
                    input_text = valor['-INPUT-']
                    if input_text and not is_scanning:
                  
                        input_buffer = input_text
                        input_start_time = current_time
                        if len(input_buffer) > 0 and input_buffer[-1] == '\r':
        
                            if input_buffer[:-1] in load_tasks(): 
                                window['-INPUT-'].update('')
                                input_buffer = ""
                            else:
                                    sg.popup('Não a esse produto no estoque',title = 'Erro')
                            
                        else:
                            is_scanning = True

               
                if values['-INPUT-'] == "":
                    is_scanning = False





 
 
 
 
 
    if event == 'Cadastrar':
        janela.close()
        janela = sg.Window('Cadastro', tela_Cadastro())
        while True:
            evento_cadastro, valores_cadastro = janela.read()
            
            if evento_cadastro == 'Cadastrar' or evento_cadastro == '\r':
                usu = valores_cadastro['-nome-']
                senha = valores_cadastro['-senha-']
                senha_rep = valores_cadastro['-senha_rep-']
                if not usu or not senha or not senha_rep:
                    sg.popup('Por favor, preencha todos os campos.')
                else:
                    if usu in dados_pessoas():
                        sg.popup('Usuário já existe.')
                    elif senha == senha_rep:
                        usuario_tipo = 'usuario' if valores_cadastro['usuario'] else 'personal'
                        if usuario_tipo == 'usuario':
                            dados = dados_pessoas()
                            dados[usu] = {senha: 'usuario'}
                            with open(usuario_file, 'w') as arquivo_json:
                                json.dump(dados, arquivo_json, indent=4)
                            sg.popup('Usuário cadastrado com sucesso.')
                            janela.close()
                            janela = sg.Window('Login', tela_Login())
                            break
                        else:
                            janela.close()
                            janela = sg.Window('Senha dos Funcionários', tela_Cadastro_2())
                            while True:
                                evento, valor = janela.read()
                                if evento == 'Ok' or evento == '\r':
                                    if not valor['-senha-']:
                                        sg.popup('Por favor, preencha todos os campos.')
                                    else:
                                        dados = dados_pessoas()
                                        dados[usu] = {senha: 'personal'}
                                        with open(usuario_file, 'w') as arquivo_json:
                                            json.dump(dados, arquivo_json, indent=4)
                                        sg.popup('Usuário cadastrado com sucesso.')
                                        janela.close()
                                        janela = sg.Window('Login', tela_Login())
                                        break
                                       
                                if  evento == sg.WIN_CLOSED or evento == 'Cancelar':
                                    janela.close()
                                    janela = sg.Window('Cadastro', tela_Cadastro())
                                    break
                            break      
                    else:
                        sg.popup('As senhas não coincidem.')
            if evento_cadastro == sg.WIN_CLOSED or evento_cadastro == 'Cancelar':
                janela.close()
                janela = sg.Window('Login', tela_Login())
                break
    
janela.close()