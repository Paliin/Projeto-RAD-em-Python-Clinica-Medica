import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# Paleta de cores do seu projeto
C_VERDE_BASE   = "#41A77A"  
C_AZUL_MARINHO = "#115272"  
C_BRANCO       = "#FFFFFF"
C_VERMELHO     = "#E7272D"

# Lista de ícones disponíveis (baseado nos dicionários do tela_servicos.py)
ICONES_DISPONIVEIS = [
    "hemo", "raiox", "endo", "ecg", "tomo", # Exames
    "cardio", "clinico", "dermato", "ortopedista", "pediatra" # Consultas
]

def criar_tabela_servicos():
    """Cria a tabela no SQLite (se não existir) para manipular o BD"""
    conn = sqlite3.connect('banco_pedidos.db')
    cursor = conn.cursor()
    # Tabela unificada para Exames e Consultas (Médicos)
    cursor.execute('''CREATE TABLE IF NOT EXISTS servicos_cadastrados (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        categoria TEXT NOT NULL,
                        nome TEXT NOT NULL,
                        detalhe TEXT NOT NULL,
                        icone TEXT NOT NULL,
                        preco REAL NOT NULL)''')
    conn.commit()
    conn.close()

def abrir_tela_cadastro(root):
    criar_tabela_servicos()
    
    # Criando janela administrativa sobreposta
    janela_cad = Toplevel(root)
    janela_cad.title("Administrativo - Cadastro de Serviços e Médicos")
    janela_cad.geometry("900x700")
    janela_cad.configure(bg=C_VERDE_BASE)
    
    # Título
    Label(janela_cad, text="Cadastro do Sistema (Exames e Consultas)", font=("Nunito", 22, "bold"), bg=C_VERDE_BASE, fg=C_BRANCO).pack(pady=15)
    
    # Formulário
    frame_form = Frame(janela_cad, bg=C_VERDE_BASE)
    frame_form.pack(pady=10, fill=X, padx=50)
    
    # Variáveis
    var_categoria = StringVar(value="Exame")
    
    # Linha 1: Categoria (Exame ou Consulta)
    Label(frame_form, text="Categoria:", font=("Nunito", 16, "bold"), bg=C_VERDE_BASE, fg=C_BRANCO).grid(row=0, column=0, pady=5, sticky=W)
    frame_radios = Frame(frame_form, bg=C_VERDE_BASE)
    frame_radios.grid(row=0, column=1, pady=5, sticky=W)
    
    def atualizar_label_detalhe():
        if var_categoria.get() == "Consulta":
            lbl_detalhe.config(text="Nome do Médico:")
        else:
            lbl_detalhe.config(text="Descrição do Exame:")
            
    Radiobutton(frame_radios, text="Exame", variable=var_categoria, value="Exame", font=("Nunito", 14), bg=C_VERDE_BASE, fg=C_BRANCO, selectcolor=C_AZUL_MARINHO, command=atualizar_label_detalhe).pack(side=LEFT, padx=(0, 10))
    Radiobutton(frame_radios, text="Consulta", variable=var_categoria, value="Consulta", font=("Nunito", 14), bg=C_VERDE_BASE, fg=C_BRANCO, selectcolor=C_AZUL_MARINHO, command=atualizar_label_detalhe).pack(side=LEFT)

    # Linha 2: Nome do Serviço
    Label(frame_form, text="Nome da Categoria:", font=("Nunito", 16, "bold"), bg=C_VERDE_BASE, fg=C_BRANCO).grid(row=1, column=0, pady=5, sticky=W)
    entry_nome = Entry(frame_form, font=("Nunito", 14), width=40)
    entry_nome.grid(row=1, column=1, pady=5, padx=10, sticky=W)
    entry_nome.insert(0, "Ex: Raio-X ou Cardiologista")

    # Linha 3: Detalhe (Descrição ou Nome do Médico)
    lbl_detalhe = Label(frame_form, text="Descrição do Exame:", font=("Nunito", 16, "bold"), bg=C_VERDE_BASE, fg=C_BRANCO)
    lbl_detalhe.grid(row=2, column=0, pady=5, sticky=W)
    entry_detalhe = Entry(frame_form, font=("Nunito", 14), width=40)
    entry_detalhe.grid(row=2, column=1, pady=5, padx=10, sticky=W)

    # Linha 4: Seleção de Ícone
    Label(frame_form, text="Ícone Base:", font=("Nunito", 16, "bold"), bg=C_VERDE_BASE, fg=C_BRANCO).grid(row=3, column=0, pady=5, sticky=W)
    combo_icone = ttk.Combobox(frame_form, values=ICONES_DISPONIVEIS, font=("Nunito", 14), state="readonly", width=38)
    combo_icone.grid(row=3, column=1, pady=5, padx=10, sticky=W)
    if ICONES_DISPONIVEIS:
        combo_icone.current(0)
    
    # Linha 5: Preço
    Label(frame_form, text="Preço (R$):", font=("Nunito", 16, "bold"), bg=C_VERDE_BASE, fg=C_BRANCO).grid(row=4, column=0, pady=5, sticky=W)
    entry_preco = Entry(frame_form, font=("Nunito", 14), width=15)
    entry_preco.grid(row=4, column=1, pady=5, padx=10, sticky=W)
    
    # Limpa placeholder ao focar
    def limpar_placeholder(event):
        if entry_nome.get() == "Ex: Raio-X ou Cardiologista":
            entry_nome.delete(0, END)
    entry_nome.bind("<FocusIn>", limpar_placeholder)

    def salvar_servico():
        categoria = var_categoria.get()
        nome = entry_nome.get()
        detalhe = entry_detalhe.get()
        icone = combo_icone.get()
        preco = entry_preco.get()
        
        # Tratamento de exceção essencial
        if not nome or not detalhe or not preco or nome == "Ex: Raio-X ou Cardiologista":
            messagebox.showwarning("Atenção", "Preencha todos os campos corretamente!")
            return
        try:
            preco_float = float(preco.replace(',', '.'))
            conn = sqlite3.connect('banco_pedidos.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO servicos_cadastrados (categoria, nome, detalhe, icone, preco) VALUES (?, ?, ?, ?, ?)", 
                           (categoria, nome, detalhe, icone, preco_float))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Sucesso", f"{categoria} cadastrado(a) com sucesso!")
            entry_nome.delete(0, END)
            entry_detalhe.delete(0, END)
            entry_preco.delete(0, END)
            listar_servicos() # Atualiza a tabela
        except ValueError:
            messagebox.showerror("Erro", "Preço inválido. Digite um valor numérico.")
        except sqlite3.Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Ocorreu um erro: {e}")

    def deletar_selecionado():
        item_selecionado = tree.selection()
        if not item_selecionado:
            messagebox.showwarning("Atenção", "Selecione um item na lista para excluir.")
            return
            
        if messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir este item?"):
            try:
                valores = tree.item(item_selecionado[0], 'values')
                id_item = valores[0]
                
                conn = sqlite3.connect('banco_pedidos.db')
                cursor = conn.cursor()
                cursor.execute("DELETE FROM servicos_cadastrados WHERE id = ?", (id_item,))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Sucesso", "Item excluído com sucesso!")
                listar_servicos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir: {e}")

    # Botoes de Ação
    frame_botoes = Frame(janela_cad, bg=C_VERDE_BASE)
    frame_botoes.pack(pady=10)
    
    Button(frame_botoes, text="Salvar Cadastro", font=("Nunito", 14, "bold"), bg=C_AZUL_MARINHO, fg=C_BRANCO, cursor="hand2", command=salvar_servico, width=20).pack(side=LEFT, padx=10)
    Button(frame_botoes, text="Excluir Selecionado", font=("Nunito", 14, "bold"), bg=C_VERMELHO, fg=C_BRANCO, cursor="hand2", command=deletar_selecionado, width=20).pack(side=LEFT, padx=10)
    
    # Estilizando o Treeview
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview.Heading", font=("Nunito", 12, "bold"), background=C_AZUL_MARINHO, foreground="white")
    style.configure("Treeview", font=("Nunito", 11), rowheight=25)
    
    # Treeview (Tabela visual)
    colunas = ("ID", "Categoria", "Nome", "Médico/Detalhe", "Ícone", "Preço")
    tree = ttk.Treeview(janela_cad, columns=colunas, show="headings", height=10)
    
    tree.heading("ID", text="ID")
    tree.heading("Categoria", text="Cat.")
    tree.heading("Nome", text="Especialidade/Tipo")
    tree.heading("Médico/Detalhe", text="Profissional/Descrição")
    tree.heading("Ícone", text="Ícone Ref.")
    tree.heading("Preço", text="Preço (R$)")
    
    tree.column("ID", width=40, anchor=CENTER)
    tree.column("Categoria", width=80, anchor=CENTER)
    tree.column("Nome", width=160, anchor=W)
    tree.column("Médico/Detalhe", width=220, anchor=W)
    tree.column("Ícone", width=80, anchor=CENTER)
    tree.column("Preço", width=100, anchor=CENTER)
    
    tree.pack(pady=10, padx=20, fill=X)
    
    def listar_servicos():
        for i in tree.get_children():
            tree.delete(i)
        conn = sqlite3.connect('banco_pedidos.db')
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM servicos_cadastrados ORDER BY categoria, nome")
            for linha in cursor.fetchall():
                tree.insert("", END, values=(linha[0], linha[1], linha[2], linha[3], linha[4], f"R$ {linha[5]:.2f}"))
        except sqlite3.OperationalError:
            pass # Tabela vazia ou não criada ainda
        finally:
            conn.close()
        
    listar_servicos()