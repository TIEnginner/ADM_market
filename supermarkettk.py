import tkinter as tk
from tkinter import messagebox
import sqlite3
import ttkbootstrap as ttk

def connect_db():
    conn = sqlite3.connect('database.db')
    return conn

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) / 2
    y = (screen_height - height) / 2
    window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
    
def setup_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_type TEXT NOT NULL,
            name TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            gender TEXT
        )
    ''')
    conn.commit()
    conn.close()

def login():
    user_type_client = user_type_var_register_client.get()
    nome = name_login_entry.get().strip()
    password = password_login_entry.get().strip()

    if not nome or not password:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
        return

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users WHERE user_type=? AND name=? AND password=?
    ''', (user_type_client, nome, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        messagebox.showinfo("Sucesso", f"Bem-vindo, {user[2]}!")
    else:
        messagebox.showerror("Erro", "Usuário ou senha inválidos.")
    root.withdraw()

def save_registration_cliente():
    name = name_register_entry.get().strip()
    genero = option_combobox.get()
    password = senha_client.get().strip()

    if not name or not genero or not password:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
        return

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (user_type, name, password, gender)
            VALUES (?, ?, ?, ?)
        ''', ('cliente', name, password, genero))
        conn.commit()
        messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso")
        register_window.destroy()
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "Usuário já cadastrado")
    conn.close()

def storage_view():
    window_s = tk.Toplevel()
    window_s.title("Estoque")
    center_window(window_s, 800, 600)
    
    tk.Label(window_s, text="Estoque de Produtos", font=('Arial', 14)).pack(pady=20)

    produto_list = tk.Listbox(window_s, width=50, height=20)
    produto_list.pack(pady=10)

    for produto in produtos:
        produto_list.insert(tk.END, produto['nome'])

    detalhes_label = tk.Label(window_s, text="", justify="left")
    detalhes_label.pack(pady=20)

    def mostrar_detalhes(event):
        selecionado = produto_list.get(produto_list.curselection())
        for produto in produtos:
            if produto['nome'] == selecionado:
                detalhes = (f"Código: {produto['codigo']}\n"
                            f"Nome: {produto['nome']}\n"
                            f"Categoria: {produto['categoria']}\n"
                            f"Preço: R${produto['preço']:.2f}\n"
                            f"Quantidade: {produto['quantidade']}")
                detalhes_label.config(text=detalhes)
                break

    produto_list.bind('<<ListboxSelect>>', mostrar_detalhes)

def register():
    global register_window, user_type_var_register_client
    register_window = tk.Toplevel(root)
    register_window.title("Registro")
    register_window.geometry("400x300")
    center_window(register_window, 400, 300)

    tk.Label(register_window, text="Tela de cadastro de clientes", font=('Arial', 14)).pack(pady=20)

    tk.Label(register_window, text="Nome", font=('Arial', 10)).pack(pady=10)
    global name_register_entry
    name_register_entry = tk.Entry(register_window, font=('Arial', 10))
    name_register_entry.pack(pady=5)

    tk.Label(register_window, text="Gênero", font=('Arial', 10)).pack(pady=10)
    global option_combobox
    selected_option = tk.StringVar()
    genero_register_entry = ['Masculino', 'Feminino', 'Relâmpago Marquinhos']
    option_combobox = ttk.Combobox(register_window, textvariable=selected_option, values=genero_register_entry)
    option_combobox.pack(pady=10)
    
    tk.Label(register_window, text="Senha", font=('Arial', 10)).pack(pady=10)
    global senha_client
    senha_client = tk.Entry(register_window, font=('Arial', 10), show='*')
    senha_client.pack(pady=5)

    user_type_var_register_client = tk.StringVar(value="cliente")

    tk.Button(register_window, text="Registrar", command=save_registration_cliente, font=('Arial', 12)).pack(pady=20)

def main_little_car():
    global root, name_login_entry, password_login_entry, user_type_var_register_client
    setup_db()
    global produtos
    produtos = [
        {"codigo": "P001", "nome": "Arroz 5kg", "categoria": "Alimentos", "preço": 25.90, "quantidade": 50},
        {"codigo": "P002", "nome": "Feijão 1kg", "categoria": "Alimentos", "preço": 7.50, "quantidade": 40},
        {"codigo": "P003", "nome": "Açúcar 1kg", "categoria": "Alimentos", "preço": 4.20, "quantidade": 60},
        {"codigo": "P004", "nome": "Óleo de Soja 900ml", "categoria": "Alimentos", "preço": 6.80, "quantidade": 35},
        {"codigo": "P005", "nome": "Macarrão 500g", "categoria": "Alimentos", "preço": 3.50, "quantidade": 45},
        {"codigo": "P006", "nome": "Sabão em Pó 1kg", "categoria": "Limpeza", "preço": 9.50, "quantidade": 20},
        {"codigo": "P007", "nome": "Amaciante 2L", "categoria": "Limpeza", "preço": 10.90, "quantidade": 15},
        {"codigo": "P008", "nome": "Papel Higiênico 12 rolos", "categoria": "Higiene", "preço": 15.00, "quantidade": 30},
        {"codigo": "P009", "nome": "Shampoo 400ml", "categoria": "Higiene", "preço": 9.00, "quantidade": 20},
        {"codigo": "P010", "nome": "Frango Inteiro Congelado 1kg", "categoria": "Carnes", "preço": 10.50, "quantidade": 25}
    ]
    
    root = tk.Tk()
    root.title("Carrinho de compras")
    root.geometry("1080x800")

    tk.Label(root, text="Menu de compras", font=('Arial', 14)).pack(pady=20)

    tk.Label(root, text="Nome", font=('Arial', 10)).pack(pady=10)
    global name_login_entry
    name_login_entry = tk.Entry(root, font=('Arial', 10))
    name_login_entry.pack(pady=5)

    tk.Label(root, text="Senha", font=('Arial', 10)).pack(pady=10)
    global password_login_entry
    password_login_entry = tk.Entry(root, font=('Arial', 10), show='*')
    password_login_entry.pack(pady=5)

    tk.Button(root, text="Login", command=login, font=('Arial', 10)).pack(pady=10)

    tk.Button(root, text="Cadastrar clientes", command=register, font=('Arial', 10)).pack(pady=10)
    tk.Button(root, text="Ver Estoque", command=storage_view, font=('Arial', 10)).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_little_car()
