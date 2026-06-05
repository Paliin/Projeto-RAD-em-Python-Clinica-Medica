# main.py
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import simpledialog
from PIL import Image, ImageTk 
import sqlite3
import re
import os
import sys
import tela_servicos  

# ANA: arrumei aquele bug do icone sumindo no exe dps do build pelo pyinstaller
def obter_pasta_correta():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

DIRETORIO_BASE = obter_pasta_correta()

# PAULO: ui base (botoes e inputs)
class BotaoArredondado(Canvas):
    def __init__(self, master, text, bg_color, fg_color, font, command, radius=25, **kwargs):
        super().__init__(master, bg="#41A77A", highlightthickness=0, **kwargs) # <--- funcionou de alguma forma o highlightthickness=0, deixar assim
        self.command = command
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.radius = radius
        self.config(cursor="hand2")
        self.bind("<Configure>", self.desenhar)
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)

    def desenhar(self, event=None):
        self.delete("all")
        w, h, r = self.winfo_width(), self.winfo_height(), self.radius
        if w < r*2 or h < r*2: return
        
        self.create_oval(0, 0, r*2, r*2, fill=self.bg_color, outline="", tags="bg")
        self.create_oval(w-r*2, 0, w, r*2, fill=self.bg_color, outline="", tags="bg")
        self.create_oval(0, h-r*2, r*2, h, fill=self.bg_color, outline="", tags="bg")
        self.create_oval(w-r*2, h-r*2, w, h, fill=self.bg_color, outline="", tags="bg")
        self.create_rectangle(r, 0, w-r, h, fill=self.bg_color, outline="", tags="bg")
        self.create_rectangle(0, r, w, h-r, fill=self.bg_color, outline="", tags="bg")
        
        self.create_text(w/2, h/2, text=self.text, fill=self.fg_color, font=self.font, justify="center", tags="fg")

    def on_press(self, event): 
        self.itemconfig("bg", fill="#115272")
        self.itemconfig("fg", fill="white")
        self.move("all", 0, 2)
        
    def on_release(self, event):
        self.itemconfig("bg", fill=self.bg_color)
        self.itemconfig("fg", fill=self.fg_color)
        self.move("all", 0, -2)
        
        if 0 <= event.x <= self.winfo_width() and 0 <= event.y <= self.winfo_height() and self.command:
            self.command()

class EntradaArredondada(Canvas):
    def __init__(self, master, textvariable, placeholder, width=350, height=60, radius=25, **kwargs):
        super().__init__(master, bg="#41A77A", highlightthickness=0, width=width, height=height, **kwargs)
        self.textvariable = textvariable
        self.placeholder = placeholder
        self.radius = radius
        self.entry_criada = False
        self.bind("<Configure>", self.desenhar)

    def desenhar(self, event=None):
        self.delete("all")
        w, h, r = self.winfo_width(), self.winfo_height(), self.radius
        if w < r*2 or h < r*2: return
        
        self.create_oval(0, 0, r*2, r*2, fill="white", outline="")
        self.create_oval(w-r*2, 0, w, r*2, fill="white", outline="")
        self.create_oval(0, h-r*2, r*2, h, fill="white", outline="")
        self.create_oval(w-r*2, h-r*2, w, h, fill="white", outline="")
        self.create_rectangle(r, 0, w-r, h, fill="white", outline="")
        self.create_rectangle(0, r, w, h-r, fill="white", outline="")

        if not self.entry_criada:
            self.entry = Entry(self, textvariable=self.textvariable, font=("Nunito", 24, "bold"), 
                               bg="white", fg="gray", bd=0, highlightthickness=0, justify="center")
            self.inserir_placeholder()
            self.entry.bind("<FocusIn>", self.limpar_placeholder)
            self.entry.bind("<FocusOut>", self.inserir_placeholder)
            self.create_window(w/2, h/2, window=self.entry, width=w-40, anchor="center")
            self.entry_criada = True

    def inserir_placeholder(self, event=None):
        if not self.entry.get():
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg="gray")

    def limpar_placeholder(self, event=None):
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, END)
            self.entry.config(fg="black")

# PAULO: janela principal setup
janela_login = Tk()
janela_login.title("Bem vindo(a) à Clínica Legal")
janela_login.geometry("1280x720") 
janela_login.state('zoomed') 
janela_login.resizable(width=True, height=True)
janela_login.configure(background="white")

try:
    caminho_icone = os.path.join(DIRETORIO_BASE, "Assets", "Logo", "logo_icon.ico")
    janela_login.iconbitmap(caminho_icone)
except Exception as e:
    print(f"Erro ao carregar ícone: {e}")

def alternar_fullscreen(event=None):
    estado_atual = janela_login.attributes('-fullscreen')
    janela_login.attributes('-fullscreen', not estado_atual)
janela_login.bind("<F11>", alternar_fullscreen)

try:
    caminho_logo = os.path.join(DIRETORIO_BASE, "Assets", "Logo", "main_logo.png")
    img_original = Image.open(caminho_logo)

    largura_desejada = 700
    proporcao = (largura_desejada / float(img_original.size[0]))
    altura_proporcional = int((float(img_original.size[1]) * float(proporcao)))

    img_resize = img_original.resize((largura_desejada, altura_proporcional), Image.Resampling.LANCZOS)
    logo = ImageTk.PhotoImage(img_resize)
except Exception as e:
    print(f"Erro na logo: {e}")
    logo = None

# PAULO: layout dividido no meio pra logo e login
cor_fundo_esquerda = "#F4F7F6" 
Leftframe = Frame(janela_login, relief=FLAT, bg=cor_fundo_esquerda)
Leftframe.pack(side=LEFT, fill=BOTH, expand=True)

logo_container = Frame(Leftframe, bg=cor_fundo_esquerda)
logo_container.place(relx=0.5, rely=0.5, anchor="center")
if logo:
    logo_label = Label(logo_container, image=logo, bg=cor_fundo_esquerda)
    logo_label.pack()

Rightframe = Frame(janela_login, relief=FLAT, bg="#41A77A")
Rightframe.pack(side=RIGHT, fill=BOTH, expand=True)

login_container = Frame(Rightframe, bg="#41A77A")
login_container.place(relx=0.5, rely=0.5, anchor="center")

welcome_label = Label(login_container, text="Seja bem vindo(a)", font=("Nunito", 36, "bold"), bg="#41A77A", fg="white")
welcome_label.pack(pady=(0, 10))

cpf_label = Label(login_container, text="Para iniciar, digite o seu CPF:", font=("Nunito", 20), bg="#41A77A", fg="white")
cpf_label.pack(pady=(0, 40))

#criação do acesso restrito
def verificar_acesso_restrito():
    # Abre uma janelinha nativa pedindo a senha
    senha = simpledialog.askstring("Acesso Restrito", "Digite a senha do administrador:", show='*')
    
    # Verifica se a senha é a padrão
    if senha == "123456":
        import tela_cadastro # Importa o arquivo da tela administrativa
        tela_cadastro.abrir_tela_cadastro(janela_login) # Passa a janela_login como root
    elif senha is not None: 
        # Se ele não clicou em "Cancelar", mas errou a senha
        messagebox.showerror("Acesso Negado", "Senha incorreta. Acesso exclusivo para administradores.")

# ENRIQUE: regras de negocio e banco
TEXTO_PLACEHOLDER = "CPF(Somente números)"

# ANA: peguei esse validador do SO
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
    if valor == TEXTO_PLACEHOLDER: return
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
    
    if cpf_digitado == TEXTO_PLACEHOLDER or not cpf_digitado:
        mensagem_label.config(text="Atenção: Preencha o seu CPF.", fg="#FFCDD2")
        return

    if validar_cpf(cpf_digitado):
        # ENRIQUE: gambiarra p manter a sessao salva local por enquanto nos testes
        conn = sqlite3.connect('banco_pedidos.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS sessao_usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT, cpf TEXT UNIQUE)''')
        try:
            cursor.execute("INSERT INTO sessao_usuario (cpf) VALUES (?)", (cpf_digitado,))
            conn.commit()
            mensagem_label.config(text="CPF validado! Acessando...", fg="white")
        except sqlite3.IntegrityError:
            mensagem_label.config(text="Bem-vindo de volta! Acessando...", fg="white")
        conn.close()
        
        janela_login.after(1000, lambda: abrir_tela_de_servicos(cpf_digitado))
    else:
        mensagem_label.config(text="Atenção: Digite um CPF válido.", fg="#FFCDD2")

cpf_var = StringVar()
cpf_var.trace_add("write", limitar_tamanho)

campo_cpf = EntradaArredondada(login_container, textvariable=cpf_var, placeholder=TEXTO_PLACEHOLDER, width=420, height=75)
campo_cpf.pack(pady=10)

mensagem_label = Label(login_container, text="", font=("Nunito", 16, "bold"), bg="#41A77A")
mensagem_label.pack(pady=10)

btn_entrar = BotaoArredondado(login_container, text="CONFIRMAR", bg_color="white", fg_color="#41A77A", font=("Nunito", 22, "bold"), command=salvar_e_logar, width=350, height=75, radius=35)
btn_entrar.pack(pady=20)

# Botão de Acesso Restrito no canto superior direito
btn_restrito = Button(janela_login, text="⚙️ Acesso Restrito", font=("Nunito", 10, "bold"), 
                      bg="#115272", fg="#FFFFFF", bd=0, cursor="hand2", 
                      command=verificar_acesso_restrito, padx=10, pady=5)

# O place ancora o botão no canto direito (relx=0.98) e um pouco abaixo do topo (rely=0.02)
btn_restrito.place(relx=0.98, rely=0.02, anchor="ne")

janela_login.mainloop()