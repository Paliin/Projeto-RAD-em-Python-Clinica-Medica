# importando as bibliotecas necessárias
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk 
import sqlite3
import re
import tela_servicos  # Importando o arquivo da próxima tela

janela_login = Tk()
janela_login.title("Bem vindo(a) à Clínica Legal")
janela_login.geometry("1280x720") 
janela_login.state('zoomed') 
janela_login.resizable(width=True, height=True)
janela_login.configure(background="white")

def alternar_fullscreen(event=None):
    estado_atual = janela_login.attributes('-fullscreen')
    janela_login.attributes('-fullscreen', not estado_atual)
janela_login.bind("<F11>", alternar_fullscreen)

# ----- controle das imagens e config ---
img_original = Image.open("Assets/Logo/main_logo.png")

# Definimos uma largura grande e imponente para o Desktop
largura_desejada = 700

# Calcula a altura automaticamente para NUNCA esticar a imagem
proporcao = (largura_desejada / float(img_original.size[0]))
altura_proporcional = int((float(img_original.size[1]) * float(proporcao)))

img_resize = img_original.resize((largura_desejada, altura_proporcional), Image.Resampling.LANCZOS)
logo = ImageTk.PhotoImage(img_resize)

# ----- Disposição em Colunas (Formato Desktop Moderno) -------
# Coluna Esquerda: Fundo cinza bem claro para destacar a logo branca (Split Screen)
cor_fundo_esquerda = "#F4F7F6" 
Leftframe = Frame(janela_login, relief=FLAT, bg=cor_fundo_esquerda)
Leftframe.pack(side=LEFT, fill=BOTH, expand=True)

# Centraliza a logo dentro da coluna esquerda
logo_container = Frame(Leftframe, bg=cor_fundo_esquerda)
logo_container.place(relx=0.5, rely=0.5, anchor="center")
logo_label = Label(logo_container, image=logo, bg=cor_fundo_esquerda)
logo_label.pack()

# Coluna Direita: Formulário de Login (Fundo Branco)
Rightframe = Frame(janela_login, relief=FLAT, bg="white")
Rightframe.pack(side=RIGHT, fill=BOTH, expand=True)

login_container = Frame(Rightframe, bg="white")
login_container.place(relx=0.5, rely=0.5, anchor="center")

welcome_label = Label(login_container, text="Seja bem vindo(a)", font=("Nunito", 32, "bold"), bg="white", fg="black")
welcome_label.pack(pady=(0, 25))

cpf_label = Label(login_container, text="Digite seu CPF (apenas números):", font=("Nunito", 20), bg="white", fg="black")
cpf_label.pack(pady=10)

# ---------------------------------------------------------
# FUNÇÕES DE LÓGICA DO LOGIN
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

def limitar_tamanho(*args):
    valor = cpf_var.get()
    valor_numerico = re.sub(r'[^0-9]', '', valor)
    if len(valor_numerico) > 11:
        valor_numerico = valor_numerico[:11]
    if valor != valor_numerico:
        cpf_var.set(valor_numerico)

def abrir_tela_de_servicos(cpf_logado):
    janela_login.withdraw()
    tela_servicos.iniciar_pdv(cpf_logado, janela_login)

def salvar_e_logar():
    cpf_digitado = cpf_var.get()
    if validar_cpf(cpf_digitado):
        conn = sqlite3.connect('banco_pedidos.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS sessao_usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT, cpf TEXT UNIQUE)''')
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
# INTERFACE E VÍNCULOS
# ---------------------------------------------------------
cpf_var = StringVar()
cpf_var.trace_add("write", limitar_tamanho)

cpf_entry = ttk.Entry(login_container, textvariable=cpf_var, width=22, font=("Nunito", 24), justify="center")
cpf_entry.pack(pady=10, ipady=5) # ipady dá uma altura extra confortável para o campo de digitação

mensagem_label = Label(login_container, text="", font=("Nunito", 14, "bold"), bg="white")
mensagem_label.pack(pady=10)

btn_entrar = Button(login_container, text="CONFIRMAR", command=salvar_e_logar, 
                    bg="#3BA97A", fg="white", activebackground="#2e8560", activeforeground="white",
                    font=("Nunito", 18, "bold"), width=22, height=2, relief=FLAT, cursor="hand2")
btn_entrar.pack(pady=15)

janela_login.mainloop()