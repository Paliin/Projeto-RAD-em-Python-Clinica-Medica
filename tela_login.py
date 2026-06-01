# importando as bibliotecas necessárias
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk 
import sqlite3
import re
import tela_servicos  # Importando o arquivo da próxima tela

# criando a primeira janela "Login"
janela_login = Tk()
janela_login.title("Bem vindo(a) à Clínica Legal")
janela_login.geometry("600x800")
janela_login.resizable(width=FALSE, height=FALSE)
janela_login.configure(background="white")

# ----- controle das imagens e config ---
img_original = Image.open("Assets/Logo/main_logo.png")
img_resize = img_original.resize((600, 300), Image.Resampling.LANCZOS)
logo = ImageTk.PhotoImage(img_resize)

# ----- criando a janela de login -------
Upframe = Frame(janela_login, width=600, height=300, relief=FLAT, bg="white")
Upframe.pack(side=TOP)

logo_label = Label(Upframe, image=logo, bg="white")
logo_label.place(x=0, y=0, relwidth=1, relheight=1)

Downframe = Frame(janela_login, width=600, height=500, relief=FLAT, bg="white")
Downframe.pack(side=BOTTOM, fill=X)

welcome_label = Label(Downframe, text="Seja bem vindo(a)", font=("Nunito", 26), bg="white", fg="black")
welcome_label.place(x=0, y=10, relwidth=1)

cpf_label = Label(Downframe, text="Digite seu CPF (apenas números):", font=("Nunito", 20), bg="white", fg="black")
cpf_label.place(x=0, y=60, relwidth=1)

# ---------------------------------------------------------
# 1. Função para validar CPF matematicamente
# ---------------------------------------------------------
def validar_cpf(cpf):
    cpf = re.sub(r'[^0-9]', '', str(cpf))
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    for i in range(9, 11):
        valor = sum((int(cpf[num]) * ((i + 1) - num) for num in range(0, i)))
        digito = ((valor * 10) % 11) % 10
        if str(digito) != cpf[i]:
            return False
    return True

# ---------------------------------------------------------
# 2. Função para limitar os caracteres e aceitar só números
# ---------------------------------------------------------
def limitar_tamanho(*args):
    valor = cpf_var.get()
    valor_numerico = re.sub(r'[^0-9]', '', valor)
    if len(valor_numerico) > 11:
        valor_numerico = valor_numerico[:11]
    if valor != valor_numerico:
        cpf_var.set(valor_numerico)

# ---------------------------------------------------------
# 3. Função para abrir a próxima tela
# ---------------------------------------------------------
def abrir_tela_de_servicos(cpf_logado):
    # Oculta a tela de login (mantendo o motor gráfico vivo no fundo)
    janela_login.withdraw()
    
    # Chama a tela de serviços passando o CPF e a janela principal (root)
    tela_servicos.iniciar_pdv(cpf_logado, janela_login)

# ---------------------------------------------------------
# 4. Função para salvar no Banco de Dados
# ---------------------------------------------------------
def salvar_e_logar():
    cpf_digitado = cpf_var.get()
    
    if validar_cpf(cpf_digitado):
        conn = sqlite3.connect('banco_pedidos.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessao_usuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cpf TEXT UNIQUE
            )
        ''')
        
        try:
            cursor.execute("INSERT INTO sessao_usuario (cpf) VALUES (?)", (cpf_digitado,))
            conn.commit()
            mensagem_label.config(text="CPF cadastrado! Redirecionando...", fg="green")
        except sqlite3.IntegrityError:
            mensagem_label.config(text="Bem-vindo de volta! Redirecionando...", fg="blue")
            
        conn.close()
        
        janela_login.after(1000, lambda: abrir_tela_de_servicos(cpf_digitado))
    else:
        mensagem_label.config(text="Atenção: Digite um CPF válido.", fg="red")

# ---------------------------------------------------------
# 5. Interface e Vínculo das Variáveis
# ---------------------------------------------------------
cpf_var = StringVar()
cpf_var.trace_add("write", limitar_tamanho)

cpf_entry = ttk.Entry(Downframe, textvariable=cpf_var, width=20, font=("Nunito", 20), justify="center")
cpf_entry.place(relx=0.5, y=110, anchor="n")

mensagem_label = Label(Downframe, text="", font=("Nunito", 12, "bold"), bg="white")
mensagem_label.place(relx=0.5, y=160, anchor="n")

cor_verde_logo = "#3BA97A"

btn_entrar = Button(Downframe, text="CONFIRMAR", command=salvar_e_logar, 
                    bg=cor_verde_logo, fg="white", 
                    activebackground="#2e8560", activeforeground="white",
                    font=("Nunito", 18, "bold"), 
                    width=20, height=2, 
                    relief=FLAT, cursor="hand2")
btn_entrar.place(relx=0.5, y=230, anchor="n")

janela_login.mainloop()