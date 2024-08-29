import tkinter as tk
import json
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from sabemuito import AgendaApp
from tkcalendar import DateEntry

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

def get_produto_info(nome_produto):
    for produto in produtos:
        if produto["nome"] == nome_produto:
            return produto
    return None

def finalizar_compra():
    ver_carrinho()
    
    try:
        with open('saida.json', 'r', encoding='utf-8') as arquivo_saida:
            saida = json.load(arquivo_saida)
    except FileNotFoundError:
        saida = []

    saida.extend(carrinho)

    with open('saida.json', 'w', encoding='utf-8') as arquivo_saida:
        json.dump(saida, arquivo_saida, indent=4)

    try:
        with open('produto.json', 'r', encoding='utf-8') as arquivo_produtos:
            dados_produtos = json.load(arquivo_produtos)
            produtos = dados_produtos.get("produtos", [])
    except FileNotFoundError:
        produtos = []

    for item in carrinho:
        codigo_produto = item['codigo']
        for produto in produtos:
            if produto['codigo'] == codigo_produto:
                produto['quantidade'] -= 1
                break
    with open('produto.json', 'w', encoding='utf-8') as arquivo_produtos:
        json.dump(dados_produtos, arquivo_produtos, indent=4)
    with open('carrinho.json', 'w', encoding='utf-8') as arquivo_carrinho:
        json.dump([], arquivo_carrinho, indent=4)

    ver_carrinho()

LARGURA_ABA = 600
ALTURA_ABA = 400

def saida_produto():
    global frame_interno
    if frame_interno is not None and frame_interno.winfo_ismapped():
        frame_interno.place_forget()
    else:
        if frame_interno is None:
            frame_interno = tk.Frame(app)
            canvas = tk.Canvas(frame_interno, width=LARGURA_ABA, height=ALTURA_ABA)
            scrollbar = ttk.Scrollbar(frame_interno, orient="vertical", command=canvas.yview)
            scrollbar.pack(side="right", fill="y")
            canvas.pack(side="left", fill="both", expand=True)
            canvas.create_window((0, 0), window=frame_interno, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            frame_interno.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        try:
            with open('saida.json', 'r', encoding='utf-8') as arquivo_saida:
                saida = json.load(arquivo_saida)
        except FileNotFoundError:
            saida = []

        for widget in frame_interno.winfo_children():
            widget.destroy()

        for idx, produto in enumerate(saida):
            label = ttk.Label(frame_interno, text=f"Código: {produto['codigo']}\nNome: {produto['nome']}\nPreço: R${produto['preço']:.2f}", anchor="w")
            label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")

        frame_interno.place(x=1300, y=70)

carrinho = []

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

        ver_carrinho()

def ver_carrinho():
    global carrinho
    try:
        with open('carrinho.json', 'r') as arquivo:
            carrinho = json.load(arquivo)
    except FileNotFoundError:
        carrinho = []
        with open('carrinho.json', 'w', encoding='utf-8') as arquivo:
            json.dump(carrinho, arquivo, indent=4)

nova_janela_agenda = None

def open_agenda_app():
    global nova_janela_agenda
    if nova_janela_agenda is not None and nova_janela_agenda.winfo_exists():
        nova_janela_agenda.destroy()
        nova_janela_agenda = None
    else:
        nova_janela_agenda = tk.Toplevel(app)
        nova_janela_agenda.geometry("395x500+50+100")
        nova_janela_agenda.title("Agenda App")
        agenda = AgendaApp(nova_janela_agenda)

nova_janela = None

def print_carrinho():
    global nova_janela, carrinho
    if nova_janela is not None and nova_janela.winfo_ismapped():
        nova_janela.place_forget()
    else:
        if nova_janela is None:
            nova_janela = tk.Frame(app)
            nova_janela.place(x=900, y=90)

            ver_carrinho()

            try:
                with open('carrinho.json', 'r') as arquivo:
                    carrinho = json.load(arquivo)
            except FileNotFoundError:
                carrinho = []
                with open('carrinho.json', 'w', encoding='utf-8') as arquivo:
                    json.dump(carrinho, arquivo, indent=4)
            
            texto_total = ""
            total_preco = 0
            for produto in carrinho:
                codigo = produto["codigo"]
                nome = produto["nome"]
                preco = produto["preco"]
                total_preco += preco 
                texto_total += f"Código: {codigo}\nNome: {nome}\nPreço: R${preco:.2f}\n\n"

            label = tk.Label(nova_janela, text=texto_total, padx=20, pady=20)
            label.pack()
            label2 = tk.Label(nova_janela, text=f"Total: R${total_preco:.2f}", padx=20, pady=20)
            label2.pack()
            botaoc = ttk.Button(nova_janela, text="finalizar compra", command=finalizar_compra)
            botaoc.pack()
        else:
            nova_janela.place(x=900, y=90)

app = ttk.Window(themename="darkly")
app.title("Supermercado")
app.state('zoomed') 

top_frame = ttk.Frame(app, width=350, height=100, style="TFrame")
top_frame.place(x=600, y=0)

style = ttk.Style()
style.configure("TFrame", background="#4D4D4D")

label = ttk.Label(top_frame, text="Supermercado sabe muito", font=('Helvetica', 14, 'bold'), foreground="white", background="#4D4D4D")


label1 = ttk.Label(app, text= "Lista de compra:")
label1.place(x=380, y= 50)

produto_info = get_produto_info("Arroz 5kg")
if produto_info:
    codigo_arroz = produto_info["codigo"]
    nome_arroz = produto_info["nome"]
    preco_arroz = produto_info["preço"]

botao2 = ttk.Button(app, text=f"{nome_arroz}\n{codigo_arroz}\nR${preco_arroz:.2f}", style="TButton", command= lambda: adicionar_ao_carrinho(codigo_arroz, nome_arroz, preco_arroz))
botao2.place(x=600, y=100)
style.configure("TButton", background="#4D4D4D", relief="flat")
imagem_pillow = Image.open("arroz-tipo-1-camil-5kg.jpg")
imagem_pillow_resized = imagem_pillow.resize((100, 80))
imagem = ImageTk.PhotoImage(imagem_pillow_resized)
botao2.config(image=imagem, compound="top")

produto_info = get_produto_info("Feijão 1kg")
if produto_info:
    codigo_feijao = produto_info["codigo"]
    nome_feijao = produto_info["nome"]
    preco_feijao = produto_info["preço"]
botao3 = ttk.Button(app, text=f"{nome_feijao}\n{codigo_feijao}\nR${preco_feijao:.2f}", style="TButton",  command= lambda: adicionar_ao_carrinho(codigo_feijao, nome_feijao, preco_arroz))
botao3.place(x=750, y=100)
style.configure("TButton", background="#4D4D4D", relief="flat")
imagem_pillow3 = Image.open("images_feijao.jpg")
imagem_pillow_resized3 = imagem_pillow3.resize((100, 80))
imagem3 = ImageTk.PhotoImage(imagem_pillow_resized3)
botao3.config(image=imagem3, compound="top")

produto_info = get_produto_info("Açúcar 1kg")
if produto_info:
    codigo_acucar = produto_info["codigo"]
    nome_acucar = produto_info["nome"]
    preco_acucar = produto_info["preço"]
botao4 = ttk.Button(app, text=f"{nome_acucar}\n{codigo_acucar}\nR${preco_acucar:.2f}", style="TButton",  command= lambda: adicionar_ao_carrinho(codigo_acucar, nome_acucar, preco_acucar))
botao4.place(x=600, y=280)
style.configure("TButton", background="#4D4D4D", relief="flat")
imagem_pillow4 = Image.open("a_car_delta_cristal_1kg.jpg")
imagem_pillow_resized4 = imagem_pillow4.resize((100, 80))
imagem4 = ImageTk.PhotoImage(imagem_pillow_resized4)
botao4.config(image=imagem4, compound="top")

produto_info = get_produto_info("Óleo de Soja 900ml")
if produto_info:
    codigo_oleo = produto_info["codigo"]
    nome_oleo = produto_info["nome"]
    preco_oleo = produto_info["preço"]
botao5 = ttk.Button(app, text=f"{nome_oleo}\n{codigo_oleo}\nR${preco_oleo:.2f}", style="TButton", command= lambda: adicionar_ao_carrinho(codigo_oleo, nome_oleo, preco_oleo))
botao5.place(x=750, y=280)
style.configure("TButton", background="#4D4D4D", relief="flat")
imagem_pillow5 = Image.open("oleo-de-soja-soya-bomboi-madureira-entrega.jpg")
imagem_pillow_resized5 = imagem_pillow5.resize((100, 80))
imagem5 = ImageTk.PhotoImage(imagem_pillow_resized5)
botao5.config(image=imagem5, compound="top")

botao6 = tk.Button(app, command=lambda: print_carrinho())
botao6.place(x=840, y=55)
style.configure("TButton", background="#4D4D4D", relief="flat")
imagem_pillow6 = Image.open("shopping-cart.png")
imagem_pillow_resized6 = imagem_pillow6.resize((15, 15))
imagem6 = ImageTk.PhotoImage(imagem_pillow_resized6)
botao6.config(image=imagem6, compound="top", width=30, height=30)

label.grid(row=0, column=0, padx=10, pady=10)
botao1 = ttk.Button(app, text="Estoque", command= lambda: open_agenda_app())
botao1.place(x=20, y=30)

botao1 = ttk.Button(app, text="Saída de\nprodutos", command= lambda: saida_produto())
botao1.place(x=1000, y=30)

ver_carrinho()

app.mainloop()
