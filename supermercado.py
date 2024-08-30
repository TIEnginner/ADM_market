import tkinter as tk
import json
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from sabemuito import AgendaApp
from tkcalendar import DateEntry
from tkinter import messagebox

produtos = []
carrinho = []

def carregar_produtos():
    global produtos
    try:
        with open('produto.json', 'r', encoding='utf-8') as arquivo_produtos:
            dados_produtos = json.load(arquivo_produtos)
            produtos = dados_produtos.get("produtos", [])
    except FileNotFoundError:
        produtos = []
def placeholder_entry(entry, placeholder_text):
    def on_focusin(event):
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)
            entry.config(fg='black')

    def on_focusout(event):
        if entry.get() == '':
            entry.insert(0, placeholder_text)
            entry.config(fg='gray')
    
    entry.insert(0, placeholder_text)
    entry.config(fg='gray')
    entry.bind('<FocusIn>', on_focusin)
    entry.bind('<FocusOut>', on_focusout)


def add_loja():
    global frame_loja, canvas, scrollbar, entrada_filtro, entrada_categoria

    if frame_loja is not None and frame_loja.winfo_ismapped():
        frame_loja.place_forget()
    else:
        if frame_loja is None:
            frame_loja = tk.Frame(app, width=300, height=80)
            canvas = tk.Canvas(frame_loja, width=300, height=80)
            scrollbar = ttk.Scrollbar(frame_loja, orient="vertical", command=canvas.yview)
            scrollbar.pack(side="right", fill="y")
            canvas.pack(side="left", fill="both", expand=True)
            canvas.create_window((0, 0), window=frame_loja, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            frame_loja.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

            entrada_filtro = tk.Entry(frame_loja)
            placeholder_entry(entrada_filtro, "Filtrar por nome")
            entrada_filtro.pack(pady=5)
            entrada_filtro.bind("<KeyRelease>", aplicar_filtro)

            entrada_categoria = tk.Entry(frame_loja)
            placeholder_entry(entrada_categoria, "Filtrar por categoria")
            entrada_categoria.pack(pady=5)
            entrada_categoria.bind("<KeyRelease>", aplicar_filtro)

        for widget in frame_loja.winfo_children():
            if isinstance(widget, ttk.Button):
                widget.destroy()

        carregar_produtos()

        if produtos:
            for produto in produtos:
                preco = produto.get('preco', 'N/A')
                if preco == 'N/A':
                    texto_preco = 'N/A'
                else:
                    texto_preco = f"R${preco:.2f}"
                
                nome = produto.get('nome', 'N/A')
                codigo = produto.get('codigo', 'N/A')
                texto = f"Nome: {nome}\nCódigo: {codigo}\nPreço: {texto_preco}"
                botao = ttk.Button(frame_loja, text=texto, style="TButton", command=lambda p=produto: adicionar_ao_carrinho(p['codigo'], p['nome'], p['preco']))
                botao.pack(pady=5)
        else:
            label = ttk.Label(frame_loja, text="Nenhum produto encontrado.")
            label.pack(pady=20)

        frame_loja.place(x=400, y=120)


def aplicar_filtro(event):
    filtro_nome = entrada_filtro.get().lower()
    filtro_categoria = entrada_categoria.get().lower()
    
    for botao in frame_loja.winfo_children():
        if isinstance(botao, ttk.Button):
            texto = botao.cget("text").lower()
            if filtro_nome in texto and filtro_categoria in texto:
                botao.pack()
            else:
                botao.pack_forget()

def adicionar_ao_carrinho(codigo, nome, preco):
    global carrinho
    produto = {
        "codigo": codigo,
        "nome": nome,
        "preco": preco
    }
    carrinho.append(produto)
    with open('carrinho.json', 'w', encoding='utf-8') as arquivo:
        json.dump(carrinho, arquivo, indent=4)

    atualizar_carrinho()

def salvar_carrinho():
    with open('carrinho.json', 'w', encoding='utf-8') as arquivo:
        json.dump(carrinho, arquivo, indent=4)
nova_janela = None

def atualizar_carrinho():
    global nova_janela, carrinho
    if nova_janela is not None and nova_janela.winfo_ismapped():
        for widget in nova_janela.winfo_children():
            widget.destroy()

        total_preco = 0

        for index, produto in enumerate(carrinho):
            codigo = produto["codigo"]
            nome = produto["nome"]
            preco = produto["preco"]
            total_preco += preco

            frame_produto = tk.Frame(nova_janela)
            frame_produto.grid(row=index, column=0, padx=10, pady=5, sticky="w")

            label_produto = tk.Label(frame_produto, text=f"Código: {codigo} | Nome: {nome} | Preço: R${preco:.2f}")
            label_produto.grid(row=0, column=0, padx=5)

            btn_remover = ttk.Button(frame_produto, text="Remover", command=lambda idx=index: remover_produto(idx))
            btn_remover.grid(row=0, column=1, padx=5)

        label_total = tk.Label(nova_janela, text=f"Total: R${total_preco:.2f}")
        label_total.grid(row=len(carrinho), column=0, pady=10)

        botaoc = ttk.Button(nova_janela, text="Finalizar Compra", command=finalizar_compra)
        botaoc.grid(row=len(carrinho) + 1, column=0, pady=10)
        botaod = ttk.Button(nova_janela, text="Apagar carrinho", command=remover_produto_02)
        botaod.grid(row=len(carrinho) + 2, column=0, pady=10)

def remover_produto(index):
    global label2, janela_confirmacao, index_produto_remover

    janela_confirmacao = tk.Toplevel()
    janela_confirmacao.title("Cuidado!")

    janela_confirmacao.update_idletasks()

    largura_tela = janela_confirmacao.winfo_screenwidth()
    altura_tela = janela_confirmacao.winfo_screenheight()
    largura_janela = janela_confirmacao.winfo_reqwidth()
    altura_janela = janela_confirmacao.winfo_reqheight()

    x = (largura_tela - largura_janela) // 2
    y = (altura_tela - altura_janela) // 2

    janela_confirmacao.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")

    label = tk.Label(janela_confirmacao, text="Você tem certeza que deseja\nremover esse produto?")
    label.place(x=20, y=20)
    
    label2 = tk.Button(janela_confirmacao, text="Sim", command=lambda: confirmar_remocao(index))
    label2.place(x=100, y=70)
    
    label3 = tk.Button(janela_confirmacao, text="Cancelar", command=cancelar_remocao)
    label3.place(x=130, y=70)

def remover_produto_02():
    global label2, janela_confirmacao, index_produto_remover

    janela_confirmacao = tk.Toplevel()
    janela_confirmacao.title("Cuidado!")

    janela_confirmacao.update_idletasks()

    largura_tela = janela_confirmacao.winfo_screenwidth()
    altura_tela = janela_confirmacao.winfo_screenheight()
    largura_janela = janela_confirmacao.winfo_reqwidth()
    altura_janela = janela_confirmacao.winfo_reqheight()

    x = (largura_tela - largura_janela) // 2
    y = (altura_tela - altura_janela) // 2

    janela_confirmacao.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")

    label = tk.Label(janela_confirmacao, text="Você tem certeza que deseja\nremover esse produto?")
    label.place(x=20, y=20)
        
    label2 = tk.Button(janela_confirmacao, text="Sim", command=lambda: confirmar_remocao_02())
    label2.place(x=100, y=70)
        
    label3 = tk.Button(janela_confirmacao, text="Cancelar", command=cancelar_remocao)
    label3.place(x=130, y=70)

def confirmar_remocao(index):
    global carrinho
    del carrinho[index]
    salvar_carrinho()
    atualizar_carrinho()
    janela_confirmacao.destroy()

def confirmar_remocao_02():
    global carrinho
    carrinho.clear()
    salvar_carrinho()
    atualizar_carrinho()
    janela_confirmacao.destroy()

def cancelar_remocao():
    janela_confirmacao.destroy()

def ver_carrinho():
    global carrinho, nova_janela
    try:
        with open('carrinho.json', 'r') as arquivo:
            carrinho = json.load(arquivo)
    except FileNotFoundError:
        carrinho = []
        with open('carrinho.json', 'w', encoding='utf-8') as arquivo:
            json.dump(carrinho, arquivo, indent=4)

    if nova_janela is None:
        nova_janela = tk.Frame(app)
        nova_janela.place(x=900, y=90)

    atualizar_carrinho()

def finalizar_compra():
    global produtos, carrinho
    ver_carrinho()
    
    try:
        with open('saida.json', 'r', encoding='utf-8') as arquivo_saida:
            saida = json.load(arquivo_saida)
    except FileNotFoundError:
        saida = []

    saida.extend(carrinho)

    with open('saida.json', 'w', encoding='utf-8') as arquivo_saida:
        json.dump(saida, arquivo_saida, indent=4)
    recarregar_produtos()

    for item in carrinho:
        codigo_produto = item['codigo']
        for produto in produtos:
            if produto['codigo'] == codigo_produto:
                produto['quantidade'] -= 1
                break
    with open('produto.json', 'w', encoding='utf-8') as arquivo_produtos:
        json.dump({"produtos": produtos}, arquivo_produtos, indent=4)
    with open('carrinho.json', 'w', encoding='utf-8') as arquivo_carrinho:
        json.dump([], arquivo_carrinho, indent=4)

    carrinho = []
    atualizar_carrinho()

def recarregar_produtos():
    global produtos
    messagebox.showinfo(f"Sucesso", "seus produtos foram para a sua loja!")
    carregar_produtos()

def open_agenda_app():
    global nova_janela_agenda
    if nova_janela_agenda is not None and nova_janela_agenda.winfo_exists():
        nova_janela_agenda.destroy()
        nova_janela_agenda = None
    else:
        nova_janela_agenda = tk.Toplevel(app)
        nova_janela_agenda.geometry("395x547+50+100")
        nova_janela_agenda.title("Agenda App")
        agenda = AgendaApp(nova_janela_agenda)

app = ttk.Window(themename="darkly")
app.title("Supermercado")
app.state('zoomed') 

top_frame = ttk.Frame(app, width=350, height=100, style="TFrame")
top_frame.place(x=600, y=0)

style = ttk.Style()
style.configure("TFrame", background="#4D4D4D")

label = ttk.Label(top_frame, text="Supermercado sabe muito", font=('Helvetica', 14, 'bold'), foreground="white", background="#4D4D4D")

label1 = ttk.Label(app, text= "Lista de compra:")
label1.place(x=600, y= 50)

botao6 = tk.Button(app, text= "Carrinho", command=lambda: ver_carrinho())
botao6.place(x=840, y=55)

label.grid(row=0, column=0, padx=10, pady=10)
botao1 = ttk.Button(app, text="Estoque", command= lambda: open_agenda_app())
botao1.place(x=20, y=30)

botao1 = ttk.Button(app, text="Saída de\nprodutos")
botao1.place(x=1000, y=30)

botao_add_loja = ttk.Button(app, text="abrir Loja", command=add_loja)
botao_add_loja.place(x=600, y=70)

nova_janela = None
frame_loja = None
canvas = None
scrollbar = None
entrada_filtro = None
entrada_categoria = None

nova_janela_agenda = None

app.mainloop()