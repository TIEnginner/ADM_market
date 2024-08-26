import json
import os
import tkinter as tk
from tkinter import ttk
from datetime import datetime

class AgendaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciamento de Produtos")
        
        self.filename = "produto.json"
        self.tasks, self.categories = self.load_data()
        
        self.setup_produto()

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                data = json.load(file)
                return data.get('produtos', []), data.get('categorias', [])
        return [], []

    def save_data(self):
        data = {
            'produtos': self.tasks,
            'categorias': self.categories
        }
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)

    def setup_produto(self):
        style = ttk.Style()
        
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky="nsew")
        
        self.date_entry = ttk.Entry(frame, width=12)
        self.date_entry.bind("<KeyRelease>", self.on_date_entry_keyrelease)
        
        self.fornecedor_entry = ttk.Entry(frame)
        self.categoria_combo = ttk.Combobox(frame, values=self.categories)
        self.task_entry = ttk.Entry(frame)
        self.valor_entry = ttk.Entry(frame)
        self.quantidade_entry = ttk.Entry(frame)
        self.task_listbox = tk.Listbox(frame, selectmode=tk.SINGLE, width=60, height=10)

        self.add_btn = ttk.Button(frame, text="Adicionar", command=self.add_task)
        self.remove_btn = ttk.Button(frame, text="Remover Produto", command=self.remove_task)
        self.alterar_btn = ttk.Button(frame, text="Alterar Produto", command=self.alterar_task)
        self.add_categoria_btn = ttk.Button(frame, text="Adicionar Categoria", command=self.open_categoria_window)

        ttk.Label(frame, text="Data de validade").grid(row=0, column=0, sticky="w")
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="Fornecedor").grid(row=1, column=0, sticky="w")
        self.fornecedor_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
        
        ttk.Label(frame, text="Categoria").grid(row=2, column=0, sticky="w")
        self.categoria_combo.grid(row=2, column=1, columnspan=2, padx=5, pady=5)
        
        ttk.Label(frame, text="Produto").grid(row=3, column=0, sticky="w")
        self.task_entry.grid(row=3, column=1, columnspan=2, padx=5, pady=5)
        
        ttk.Label(frame, text="Preço").grid(row=4, column=0, sticky="w")
        self.valor_entry.grid(row=4, column=1, columnspan=2, padx=5, pady=5)
        
        ttk.Label(frame, text="Quantidade").grid(row=5, column=0, sticky="w")
        self.quantidade_entry.grid(row=5, column=1, columnspan=2, padx=5, pady=5)
        
        self.add_btn.grid(row=6, column=0, padx=5, pady=5)
        self.remove_btn.grid(row=6, column=1, padx=5, pady=5)
        self.alterar_btn.grid(row=6, column=2, padx=5, pady=5)
        self.add_categoria_btn.grid(row=7, column=0, columnspan=3, pady=5)
        
        self.task_listbox.grid(row=8, column=0, columnspan=3, padx=5, pady=5)
        self.update_task_listbox()

    def add_task(self):
        date = self.date_entry.get()
        fornecedor = self.fornecedor_entry.get()
        categoria = self.categoria_combo.get()
        task = self.task_entry.get()
        valor = self.valor_entry.get()
        quantidade = self.quantidade_entry.get()
        
        if date and fornecedor and categoria and task and valor and quantidade:
            now = datetime.now()
            time = now.strftime("%d/%m/%Y %H:%M:%S")
            formatted_task = {
                "codigo": f"prod_{len(self.tasks) + 1}",
                "nome": task,
                "preco": float(valor),
                "quantidade": int(quantidade)
            }
            
            self.tasks.append(formatted_task)
            self.save_data()
            
            self.clear_entries()
            self.update_task_listbox()

    def remove_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            del self.tasks[selected_task_index[0]]
            self.save_data()
            self.update_task_listbox()

    def alterar_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            # Índice selecionado da lista de produtos
            index = selected_task_index[0]
            selected_task = self.task_listbox.get(index)

            # Separar partes do produto selecionado
            parts = selected_task.split(" - ")
            if len(parts) == 4:
                codigo = parts[0]
                nome = parts[1]
                preco = parts[2].replace('R$', '').strip()
                quantidade = parts[3].replace('Qtd: ', '').strip()

                # Preencher campos com detalhes do produto selecionado
                self.date_entry.delete(0, tk.END)
                self.date_entry.insert(0, "01/01/2024")  # Use a data fixa por enquanto

                self.fornecedor_entry.delete(0, tk.END)
                self.fornecedor_entry.insert(0, "Fornecedor Fixo")  # Use o fornecedor fixo por enquanto

                self.categoria_combo.set("Categoria Fixa")  # Use a categoria fixa por enquanto

                self.task_entry.delete(0, tk.END)
                self.task_entry.insert(0, nome)

                self.valor_entry.delete(0, tk.END)
                self.valor_entry.insert(0, preco)

                self.quantidade_entry.delete(0, tk.END)
                self.quantidade_entry.insert(0, quantidade)

                # Atualizar o produto na lista `self.tasks`
                self.tasks[index] = {
                    "codigo": codigo,
                    "nome": nome,
                    "preco": float(preco),
                    "quantidade": int(quantidade)
                }

                # Salvar os dados atualizados
                self.save_data()

                # Atualizar a lista na interface gráfica
                self.update_task_listbox()

    def clear_entries(self):
        self.date_entry.delete(0, tk.END)
        self.fornecedor_entry.delete(0, tk.END)
        self.categoria_combo.set('')
        self.task_entry.delete(0, tk.END)
        self.valor_entry.delete(0, tk.END)
        self.quantidade_entry.delete(0, tk.END)

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            task_str = f"{task['codigo']} - {task['nome']} - R${task['preco']} - Qtd: {task['quantidade']}"
            self.task_listbox.insert(tk.END, task_str)

    def open_categoria_window(self):
        self.categoria_window = tk.Toplevel(self.root)
        self.categoria_window.title("Adicionar Categorias")
        CategoriaApp(self.categoria_window, self)

    def on_date_entry_keyrelease(self, event):
        date_str = self.date_entry.get()
        if not self.validate_date(date_str):
            return
        
        formatted_date = self.format_date(date_str)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, formatted_date)

    def validate_date(self, date_str):
        try:
            if len(date_str) > 10:
                return False
            datetime.strptime(date_str, '%d/%m/%Y')
            year = int(date_str.split('/')[2])
            if year < 2010:
                return False
            return True
        except ValueError:
            return False

    def format_date(self, date_str):
        date_str = ''.join(c for c in date_str if c.isdigit())
        if len(date_str) <= 2:
            return date_str
        elif len(date_str) <= 4:
            return f"{date_str[:2]}/{date_str[2:]}"
        elif len(date_str) <= 6:
            return f"{date_str[:2]}/{date_str[2:4]}/{date_str[4:]}"
        else:
            return f"{date_str[:2]}/{date_str[2:4]}/{date_str[4:8]}"

class CategoriaApp:
    def __init__(self, root, parent_app):
        self.root = root
        self.parent_app = parent_app
        self.filename = "produto.json"
        self.setup_categoria()

    def setup_categoria(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky="nsew")
        
        self.back_btn = ttk.Button(frame, text="Voltar", command=self.close_window)
        self.categoria_entry = ttk.Entry(frame, width=40)
        self.add_categoria_btn = ttk.Button(frame, text="Adicionar Categoria", command=self.add_categoria)

        ttk.Label(frame, text="Nova Categoria").grid(row=0, column=0, padx=5, pady=5)
        self.categoria_entry.grid(row=0, column=1, padx=5, pady=5)
        self.add_categoria_btn.grid(row=1, column=0, columnspan=2, pady=5)
        self.back_btn.grid(row=2, column=0, columnspan=2, pady=5)

    def add_categoria(self):
        categoria = self.categoria_entry.get()
        if categoria:
            if categoria not in self.parent_app.categories:
                self.parent_app.categories.append(categoria)
                self.parent_app.categoria_combo['values'] = self.parent_app.categories
                self.parent_app.save_data()
                self.categoria_entry.delete(0, tk.END)
                self.categoria_entry.focus()

    def close_window(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AgendaApp(root)
    root.mainloop()
