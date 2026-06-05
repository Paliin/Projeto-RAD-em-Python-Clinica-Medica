# tela_servicos.py
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import sys
import os
import calendar
from PIL import Image, ImageTk
from datetime import datetime, timedelta

# PAULO: decidi usar essa paleta de verde pra dar uma cara mais clean
C_VERDE_BASE   = "#41A77A"  
C_VERDE_ESCURO = "#2A6B4B"  
C_AZUL_MARINHO = "#115272"  
C_VERMELHO     = "#E7272D"  
C_BRANCO       = "#FFFFFF"
C_CINZA_FUNDO  = "#F9F9F9"
C_CINZA_TEXTO  = "gray"
C_PRETO        = "black"

class BotaoArredondado(Canvas):
    def __init__(self, master, text, bg_color, fg_color, font, command, radius=20, image=None, **kwargs):
        super().__init__(master, bg=master.cget("bg"), highlightthickness=0, **kwargs)
        self.command = command
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.radius = radius
        self.imagem_icone = image
        self.config(cursor="hand2")
        self.bind("<Configure>", self.desenhar)
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)

    def desenhar(self, event=None):
        self.delete("all")
        w, h, r = self.winfo_width(), self.winfo_height(), self.radius
        if w < r*2 or h < r*2: return
        
        self.create_oval(0, 0, r*2, r*2, fill=self.bg_color, outline="")
        self.create_oval(w-r*2, 0, w, r*2, fill=self.bg_color, outline="")
        self.create_oval(0, h-r*2, r*2, h, fill=self.bg_color, outline="")
        self.create_oval(w-r*2, h-r*2, w, h, fill=self.bg_color, outline="")
        self.create_rectangle(r, 0, w-r, h, fill=self.bg_color, outline="")
        self.create_rectangle(0, r, w, h-r, fill=self.bg_color, outline="")
        
        if self.imagem_icone:
            self.create_image(w/2, h/2 - 40, image=self.imagem_icone)
            self.create_text(w/2, h/2 + 65, text=self.text, fill=self.fg_color, font=self.font, justify="center")
        else:
            self.create_text(w/2, h/2, text=self.text, fill=self.fg_color, font=self.font, justify="center")

    def on_press(self, event): self.move("all", 0, 2)
    def on_release(self, event):
        self.move("all", 0, -2)
        if 0 <= event.x <= self.winfo_width() and 0 <= event.y <= self.winfo_height() and self.command:
            self.command()

class BuscadorArredondado(Canvas):
    def __init__(self, master, command_keyrelease, **kwargs):
        super().__init__(master, bg=C_VERDE_BASE, highlightthickness=0, width=600, height=60, **kwargs)
        self.command_keyrelease = command_keyrelease
        self.entry = Entry(self, font=("Nunito", 20), bg=C_BRANCO, fg=C_PRETO, bd=0, highlightthickness=0)
        self.entry.bind("<KeyRelease>", self.command_keyrelease)
        self.entry_criada = False
        self.bind("<Configure>", self.desenhar)
        
    def desenhar(self, event=None):
        self.delete("all")
        w, h, r = self.winfo_width(), self.winfo_height(), 25
        if w < r*2 or h < r*2: return
        self.create_oval(0, 0, r*2, r*2, fill=C_BRANCO, outline="")
        self.create_oval(w-r*2, 0, w, r*2, fill=C_BRANCO, outline="")
        self.create_oval(0, h-r*2, r*2, h, fill=C_BRANCO, outline="")
        self.create_oval(w-r*2, h-r*2, w, h, fill=C_BRANCO, outline="")
        self.create_rectangle(r, 0, w-r, h, fill=C_BRANCO, outline="")
        self.create_rectangle(0, r, w, h-r, fill=C_BRANCO, outline="")
        self.create_text(35, h/2, text="🔍", font=("Nunito", 20), fill=C_CINZA_TEXTO)
        
        if not self.entry_criada:
            self.create_window(70, h/2, window=self.entry, width=w-105, anchor=W)
            self.entry_criada = True
            
class BotOpcao(Canvas):
    def __init__(self, master, text, image, valor, preco, command_select, **kwargs):
        super().__init__(master, bg=C_VERDE_BASE, highlightthickness=0, width=520, height=110, **kwargs)
        self.text = text
        self.imagem = image
        self.valor = valor
        self.preco = preco
        self.command_select = command_select
        self.estado = "normal" 
        self.config(cursor="hand2")
        self.bind("<Configure>", self.desenhar)
        self.bind("<ButtonRelease-1>", self.on_click)

    def desenhar(self, event=None):
        self.delete("all")
        w, h, r = self.winfo_width(), self.winfo_height(), 25
        if w < r*2 or h < r*2: return
        if self.estado == "escurecido":
            cor_base, cor_interna, cor_texto, cor_preco = "#D9D9D9", "#C4C4C4", "#7A7A7A", "#7A7A7A"
        elif self.estado == "selecionado":
            cor_base, cor_interna, cor_texto, cor_preco = C_AZUL_MARINHO, "#0A3A52", C_BRANCO, "#A1D0E6"
        else:
            cor_base, cor_interna, cor_texto, cor_preco = C_BRANCO, C_CINZA_FUNDO, C_VERDE_ESCURO, C_VERDE_BASE

        def draw_round_rect(x1, y1, x2, y2, r, cor):
            self.create_oval(x1, y1, x1+r*2, y1+r*2, fill=cor, outline="")
            self.create_oval(x2-r*2, y1, x2, y1+r*2, fill=cor, outline="")
            self.create_oval(x1, y2-r*2, x1+r*2, y2, fill=cor, outline="")
            self.create_oval(x2-r*2, y2-r*2, x2, y2, fill=cor, outline="")
            self.create_rectangle(x1+r, y1, x2-r, y2, fill=cor, outline="")
            self.create_rectangle(0, r, w, h-r, fill=cor, outline="")

        draw_round_rect(0, 0, w, h, r, cor_base)
        draw_round_rect(15, 15, 120, h-15, 20, cor_interna)
        if self.imagem: 
            self.create_image(67, h/2, image=self.imagem)
        self.create_text(150, h/2 - 15, text=self.text, font=("Nunito", 22, "bold"), fill=cor_texto, anchor=W)
        self.create_text(150, h/2 + 20, text=self.preco, font=("Nunito", 16, "bold"), fill=cor_preco, anchor=W)

    def on_click(self, event):
        if self.estado == "desativado":
            return

        if self.command_select:
            self.command_select(self)

    def set_estado(self, novo_estado):
        self.estado = novo_estado
        self.desenhar()

# ANA: ajustei aqui pra 50x50 pra nao cortar o calendario em telas menores
class BotaoData(Canvas):
    def __init__(self, master, dia_mes, data_completa, command_select, **kwargs):
        super().__init__(master, bg=C_VERDE_BASE, highlightthickness=0, width=50, height=50, **kwargs)
        self.dia_mes = dia_mes
        self.valor = data_completa
        self.command_select = command_select
        self.estado = "normal" 
        self.config(cursor="hand2")
        self.bind("<Configure>", self.desenhar)
        self.bind("<ButtonRelease-1>", self.on_click)

    def desenhar(self, event=None):
        self.delete("all")
        w, h, r = self.winfo_width(), self.winfo_height(), 10
        if w < r*2 or h < r*2: return

        if self.estado == "desativado":
            cor_base, cor_texto = "#C4C4C4", "#7A7A7A"
        elif self.estado == "selecionado":
            cor_base, cor_texto = C_AZUL_MARINHO, C_BRANCO
        else:
            cor_base, cor_texto = C_BRANCO, C_VERDE_ESCURO

        self.create_oval(0, 0, r*2, r*2, fill=cor_base, outline="")
        self.create_oval(w-r*2, 0, w, r*2, fill=cor_base, outline="")
        self.create_oval(0, h-r*2, r*2, h, fill=cor_base, outline="")
        self.create_oval(w-r*2, h-r*2, w, h, fill=cor_base, outline="")
        self.create_rectangle(r, 0, w-r, h, fill=cor_base, outline="")
        self.create_rectangle(0, r, w, h-r, fill=cor_base, outline="")

        self.create_text(w/2, h/2, text=self.dia_mes, font=("Nunito", 18, "bold"), fill=cor_texto)

    def on_click(self, event):
        if self.estado == "desativado": return 
        if self.command_select: self.command_select(self)

    def set_estado(self, novo_estado):
        self.estado = novo_estado
        self.desenhar()

class BotaoHorario(Canvas):
    def __init__(self, master, horario, command_select, **kwargs):
        super().__init__(master, bg=C_VERDE_BASE, highlightthickness=0, width=130, height=45, **kwargs)
        self.valor = horario
        self.command_select = command_select
        self.selecionado = False
        self.config(cursor="hand2")
        self.bind("<Configure>", self.desenhar)
        self.bind("<ButtonRelease-1>", self.on_click)

    def desenhar(self, event=None):
        self.delete("all")
        w, h, r = self.winfo_width(), self.winfo_height(), 20
        if w < r*2 or h < r*2: return

        def draw_round_rect(x1, y1, x2, y2, raio, cor):
            self.create_oval(x1, y1, x1+raio*2, y1+raio*2, fill=cor, outline="")
            self.create_oval(x2-raio*2, y1, x2, y1+raio*2, fill=cor, outline="")
            self.create_oval(x1, y2-raio*2, x1+raio*2, y2, fill=cor, outline="")
            self.create_oval(x2-raio*2, y2-raio*2, x2, y2, fill=cor, outline="")
            self.create_rectangle(x1+raio, y1, x2-raio, y2, fill=cor, outline="")
            self.create_rectangle(x1, y1+raio, x2, y2-raio, fill=cor, outline="")

        if self.selecionado:
            draw_round_rect(0, 0, w, h, r, C_AZUL_MARINHO)
            fg_color = C_BRANCO
        else:
            draw_round_rect(0, 0, w, h, r, C_BRANCO)
            fg_color = C_VERDE_ESCURO
        self.create_text(w/2, h/2, text=self.valor, font=("Nunito", 18, "bold"), fill=fg_color)

    def on_click(self, event):
        if self.command_select: self.command_select(self)

    def set_selecionado(self, status):
        self.selecionado = status
        self.desenhar()


# ENRIQUE: main form agendamentos pdv
def iniciar_pdv(cpf_cliente, root=None):
    if root: janela = Toplevel(root)
    else: janela = Tk()
        
    janela.title("Atendimento - Clínica Legal")
    janela.geometry("1280x720")
    janela.state('zoomed')
    janela.resizable(width=True, height=True)
    janela.configure(background=C_VERDE_BASE)

    def obter_pasta_correta():
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        else:
            return os.path.dirname(os.path.abspath(__file__))

    DIRETORIO_BASE = obter_pasta_correta()

    try:
        caminho_icone = os.path.join(DIRETORIO_BASE, "Assets", "Logo", "logo_icon.ico")
        janela.iconbitmap(caminho_icone)
    except Exception as e:
        pass

    def alternar_fullscreen_pdv(event=None):
        state = not janela.attributes('-fullscreen')
        janela.attributes('-fullscreen', state)
    janela.bind("<F11>", alternar_fullscreen_pdv)

    def fechar_programa():
        if root: root.destroy()
        else: janela.destroy()
    janela.protocol("WM_DELETE_WINDOW", fechar_programa)

    def deslogar_usuario(event=None):
        resposta = messagebox.askyesno("Encerrar Atendimento", "Tem certeza que deseja encerrar seu atendimento e sair?")
        if resposta: 
            if root:
                janela.destroy() 
                root.deiconify() 
                for widget in root.winfo_children():
                    if isinstance(widget, Frame):
                        for sub_w in widget.winfo_children():
                            if isinstance(sub_w, Frame):
                                for final_w in sub_w.winfo_children():
                                    if isinstance(final_w, ttk.Entry):
                                        final_w.delete(0, END)
                                    if isinstance(final_w, Label) and final_w.cget("text") not in ["Seja bem vindo(a)", "Digite seu CPF (apenas números):"]:
                                        final_w.config(text="")
            else:
                janela.destroy()

    def voltar_ao_inicio_fluxo():
        nonlocal pedidos_selecionados, tipo_atual_selecionado
        pedidos_selecionados = []
        tipo_atual_selecionado = ""
        mostrar_frame(frame_passo1)

    pedidos_selecionados = [] 
    tipo_atual_selecionado = ""
    indice_agendamento_atual = 0
    
    mes_visualizado = datetime.now().month
    ano_visualizado = datetime.now().year
    
    MESES_PT = {1:"Janeiro", 2:"Fevereiro", 3:"Março", 4:"Abril", 5:"Maio", 6:"Junho", 
                7:"Julho", 8:"Agosto", 9:"Setembro", 10:"Outubro", 11:"Novembro", 12:"Dezembro"}
    
    botoes_carrossel_ativos = []
    botoes_data_ativos = []
    botoes_horario_ativos = []
    dados_lista_atual = [] 

    img_dict = {}
    try:
        img_logo_topo = Image.open(os.path.join(DIRETORIO_BASE, "Assets", "Logo", "main_logo.png"))
        proporcao_topo = (260 / float(img_logo_topo.size[0]))
        altura_topo_img = int((float(img_logo_topo.size[1]) * float(proporcao_topo)))
        img_dict['logo_topo'] = ImageTk.PhotoImage(img_logo_topo.resize((260, altura_topo_img), Image.Resampling.LANCZOS))
        
        img_dict['sair_btn'] = ImageTk.PhotoImage(Image.open(os.path.join(DIRETORIO_BASE, "Assets", "icone_sair.png")).resize((50, 50), Image.Resampling.LANCZOS))
        img_dict['exame_consulta_btn'] = ImageTk.PhotoImage(Image.open(os.path.join(DIRETORIO_BASE, "Assets", "icone_exame_consulta.png")).resize((130, 130), Image.Resampling.LANCZOS))
        img_dict['agenda_btn'] = ImageTk.PhotoImage(Image.open(os.path.join(DIRETORIO_BASE, "Assets", "icone_agenda.png")).resize((130, 130), Image.Resampling.LANCZOS))
        img_dict['exame_only_btn'] = ImageTk.PhotoImage(Image.open(os.path.join(DIRETORIO_BASE, "Assets", "icone_exame.png")).resize((130, 130), Image.Resampling.LANCZOS))
        img_dict['consulta_only_btn'] = ImageTk.PhotoImage(Image.open(os.path.join(DIRETORIO_BASE, "Assets", "icone_consulta.png")).resize((130, 130), Image.Resampling.LANCZOS))
        
        pasta_exames = os.path.join(DIRETORIO_BASE, "Assets", "exames")
        img_dict['hemo'] = ImageTk.PhotoImage(Image.open(os.path.join(pasta_exames, "icone_hemograma.png")).resize((55, 55), Image.Resampling.LANCZOS))
        img_dict['raiox'] = ImageTk.PhotoImage(Image.open(os.path.join(pasta_exames, "icone_raiox.png")).resize((55, 55), Image.Resampling.LANCZOS))
        img_dict['endo'] = ImageTk.PhotoImage(Image.open(os.path.join(pasta_exames, "icone_endoscopia.png")).resize((55, 55), Image.Resampling.LANCZOS))
        img_dict['ecg'] = ImageTk.PhotoImage(Image.open(os.path.join(pasta_exames, "icone_electrocardiograma.png")).resize((55, 55), Image.Resampling.LANCZOS))
        img_dict['tomo'] = ImageTk.PhotoImage(Image.open(os.path.join(pasta_exames, "icone_tomografia.png")).resize((55, 55), Image.Resampling.LANCZOS))

        pasta_consultas = os.path.join(DIRETORIO_BASE, "Assets", "consultas")
        img_dict['cardio'] = ImageTk.PhotoImage(Image.open(os.path.join(pasta_consultas, "icone_cardiologista.png")).resize((55, 55), Image.Resampling.LANCZOS))
        img_dict['clinico'] = ImageTk.PhotoImage(Image.open(os.path.join(pasta_consultas, "icone_clinico_geral.png")).resize((55, 55), Image.Resampling.LANCZOS))
        img_dict['dermato'] = ImageTk.PhotoImage(Image.open(os.path.join(pasta_consultas, "icone_dermatologista.png")).resize((55, 55), Image.Resampling.LANCZOS))
        img_dict['ortopedista'] = ImageTk.PhotoImage(Image.open(os.path.join(pasta_consultas, "icone_ortopedista.png")).resize((55, 55), Image.Resampling.LANCZOS))
        img_dict['pediatra'] = ImageTk.PhotoImage(Image.open(os.path.join(pasta_consultas, "icone_pediatra.png")).resize((55, 55), Image.Resampling.LANCZOS))
    except Exception as e: print(f"Aviso nas imagens: {e}")

    # PAULO: header reutilizavel pras outras telas
    def criar_cabecalho(parent_frame, titulo=""):
        topo_branco = Frame(parent_frame, bg=C_BRANCO, height=100)
        topo_branco.pack(fill=X, side=TOP)
        topo_branco.pack_propagate(False)
        if img_dict.get('logo_topo'):
            lbl_logo = Label(topo_branco, image=img_dict['logo_topo'], bg=C_BRANCO)
            lbl_logo.pack(side=LEFT, padx=30, pady=5)
        lbl_tit = None
        if titulo:
            lbl_tit = Label(topo_branco, text=titulo, font=("Nunito", 24, "bold"), fg=C_VERDE_ESCURO, bg=C_BRANCO)
            lbl_tit.place(relx=0.5, rely=0.5, anchor="center")
        btn_sair_container = Frame(topo_branco, bg=C_BRANCO, cursor="hand2")
        btn_sair_container.pack(side=RIGHT, padx=30, pady=5)
        if img_dict.get('sair_btn'):
            lbl_img_sair = Label(btn_sair_container, image=img_dict['sair_btn'], bg=C_BRANCO)
            lbl_img_sair.pack(side=LEFT)
            lbl_img_sair.bind("<Button-1>", deslogar_usuario)
        lbl_txt_sair = Label(btn_sair_container, text="Sair", font=("Nunito", 24, "bold"), fg=C_VERMELHO, bg=C_BRANCO)
        lbl_txt_sair.pack(side=LEFT, padx=(10, 0))
        lbl_txt_sair.bind("<Button-1>", deslogar_usuario)
        btn_sair_container.bind("<Button-1>", deslogar_usuario)
        return lbl_tit

    def mostrar_frame(frame_destino):
        frame_passo1.pack_forget()
        frame_passo1_meio.pack_forget()
        frame_passo2.pack_forget()
        frame_passo3.pack_forget()
        frame_passo3_meio.pack_forget() 
        frame_passo4.pack_forget()
        frame_meus_agendamentos.pack_forget()
        frame_destino.pack(fill=BOTH, expand=True)

    dados_agendamentos_atual = [] 

    # ENRIQUE: select cruzin, ver se melhora dps
    def carregar_dados_agendamentos():
        nonlocal dados_agendamentos_atual
        conn = sqlite3.connect('banco_pedidos.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='agendamentos'") # <--- funcionou de alguma forma
        if cursor.fetchone():
            try:
                cursor.execute("SELECT id, tipo_servico, profissional_procedimento, data_agendamento, horario_agendamento, valor FROM agendamentos WHERE cpf_cliente=?", (cpf_cliente,))
            except sqlite3.OperationalError:
                cursor.execute("SELECT id, tipo_servico, profissional_procedimento, data_agendamento, horario_agendamento, 'N/A' FROM agendamentos WHERE cpf_cliente=?", (cpf_cliente,))
            dados_agendamentos_atual = cursor.fetchall()
        else:
            dados_agendamentos_atual = []
        conn.close()

    def cancelar_agendamento(id_agendamento):
        if messagebox.askyesno("Cancelar Agendamento", "Tem certeza que deseja cancelar este agendamento?"):
            conn = sqlite3.connect('banco_pedidos.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM agendamentos WHERE id=?", (id_agendamento,))
            conn.commit()
            conn.close()
            abrir_meus_agendamentos()

    def reimprimir_ticket(agendamento):
        id_ag, tipo, prof, data, hora, valor = agendamento
        lbl_num_ticket.config(text=f"#{id_ag + 1000:04d}")
        
        for widget in caixa_recibo.winfo_children(): widget.destroy()
        Label(caixa_recibo, text=f"Ticket Re-impresso | CPF: {cpf_cliente}", font=("Nunito", 18, "bold"), bg=C_BRANCO, fg=C_PRETO, anchor=W).pack(fill=X, pady=(0, 10))
        Label(caixa_recibo, text=f"• {prof} ({data} às {hora})", font=("Nunito", 16), bg=C_BRANCO, fg=C_PRETO, anchor=W).pack(fill=X, pady=2)
        Label(caixa_recibo, text=f"Total do Pedido: {valor}", font=("Nunito", 20, "bold"), bg=C_BRANCO, fg=C_AZUL_MARINHO, anchor=W).pack(fill=X, pady=(15, 0))
        
        mostrar_frame(frame_passo4)

    def atualizar_lista_agendamentos(event=None):
        termo = buscador_agendamentos.entry.get().lower()
        for widget in scroll_agendamentos_interno.winfo_children(): widget.destroy()

        filtrados = [a for a in dados_agendamentos_atual if termo in a[1].lower() or termo in a[2].lower() or termo in a[3].lower()]

        if not filtrados:
            Label(scroll_agendamentos_interno, text="Nenhum agendamento encontrado.", font=("Nunito", 24, "bold"), bg=C_VERDE_BASE, fg=C_BRANCO).pack(pady=80)
            return

        for i, ag in enumerate(filtrados):
            id_ag, tipo, prof, data, hora, valor = ag

            card = Frame(scroll_agendamentos_interno, bg=C_BRANCO, highlightbackground=C_AZUL_MARINHO, highlightthickness=3, padx=20, pady=20)
            Label(card, text=f"{tipo}: {prof}", font=("Nunito", 22, "bold"), bg=C_BRANCO, fg=C_VERDE_ESCURO, anchor=W).pack(fill=X, pady=(0, 10))
            Label(card, text=f"Data: {data} às {hora} | Valor: {valor}", font=("Nunito", 18), bg=C_BRANCO, fg=C_PRETO, anchor=W).pack(fill=X)
            Label(card, text=f"Ticket: #{id_ag + 1000:04d}", font=("Nunito", 18), bg=C_BRANCO, fg=C_CINZA_TEXTO, anchor=W).pack(fill=X, pady=(0, 20))
            
            btn_frame = Frame(card, bg=C_BRANCO)
            btn_frame.pack(fill=X)
            BotaoArredondado(btn_frame, text="Cancelar", bg_color=C_VERMELHO, fg_color=C_BRANCO, font=("Nunito", 14, "bold"), command=lambda a=id_ag: cancelar_agendamento(a), width=160, height=50, radius=15).pack(side=LEFT, padx=(0, 10))
            BotaoArredondado(btn_frame, text="Reimprimir", bg_color=C_AZUL_MARINHO, fg_color=C_BRANCO, font=("Nunito", 14, "bold"), command=lambda a=ag: reimprimir_ticket(a), width=180, height=50, radius=15).pack(side=RIGHT)
            row, col = i // 2, i % 2
            card.grid(row=row, column=col, padx=20, pady=15, sticky="nsew")

    def abrir_meus_agendamentos():
        carregar_dados_agendamentos()
        buscador_agendamentos.entry.delete(0, END)
        atualizar_lista_agendamentos()
        mostrar_frame(frame_meus_agendamentos)

    def calcular_total_pedidos():
        total = 0.0
        for p in pedidos_selecionados:
            try:
                v_str = p["preco"].replace("R$", "").strip().replace(".", "").replace(",", ".")
                total += float(v_str)
            except: pass
        return f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def selecionar_item_carrossel(botao_clicado):
        if botao_clicado.estado == "selecionado":
            botao_clicado.set_estado("normal")
            pedidos_selecionados[:] = [p for p in pedidos_selecionados if p["profissional"] != botao_clicado.valor]
        else:
            botao_clicado.set_estado("selecionado")
            pedidos_selecionados.append({
                "tipo": tipo_atual_selecionado,
                "profissional": botao_clicado.valor,
                "preco": botao_clicado.preco,
                "imagem": botao_clicado.imagem,
                "data": "",
                "horario": ""
            })

    def atualizar_grid_pesquisa(event=None):
        termo = buscador.entry.get().lower()
        for widget in scroll_interno.winfo_children(): widget.destroy()
        botoes_carrossel_ativos.clear()

        filtrados = [d for d in dados_lista_atual if termo in d[0].lower() or termo in d[2].lower()]
        profissionais_selecionados = [p["profissional"] for p in pedidos_selecionados]

        for i, (texto, img, valor_real, preco_real) in enumerate(filtrados):
            row, col = i // 2, i % 2 
            btn = BotOpcao(scroll_interno, text=texto, image=img, valor=valor_real, preco=preco_real, command_select=selecionar_item_carrossel)
            
            if valor_real in profissionais_selecionados:
                btn.set_estado("selecionado")
                
            btn.grid(row=row, column=col, padx=20, pady=10)
            botoes_carrossel_ativos.append(btn)

    def montar_carrossel(tipo_escolhido):
        nonlocal dados_lista_atual, tipo_atual_selecionado, pedidos_selecionados
        tipo_atual_selecionado = tipo_escolhido
        pedidos_selecionados = [] 
        
        lbl_titulo_carrossel.config(text=f"Selecione {'suas' if tipo_escolhido == 'Consulta' else 'seus'} {tipo_escolhido.lower()}s")
        
        if tipo_escolhido == "Exame":
            dados_lista_atual = [
                ("Hemograma", img_dict.get('hemo'), "Hemograma Completo", "R$ 25,00"),
                ("Raio-X", img_dict.get('raiox'), "Raio-X", "R$ 90,00"),
                ("Endoscopia", img_dict.get('endo'), "Endoscopia Digestiva", "R$ 350,00"),
                ("Eletrocardiograma", img_dict.get('ecg'), "Eletrocardiograma", "R$ 80,00"),
                ("Tomografia", img_dict.get('tomo'), "Tomografia Computadorizada", "R$ 450,00"),
                ("Glicemia", img_dict.get('hemo'), "Glicemia em Jejum", "R$ 15,00"),
                ("Ultrassom", img_dict.get('tomo'), "Ultrassonografia Geral", "R$ 140,00")
            ]
        else:
            dados_lista_atual = [
                ("Clínico Geral", img_dict.get('clinico'), "Dr. Carlos Silva", "R$ 120,00"), 
                ("Pediatra", img_dict.get('pediatra'), "Dra. Ana Beatriz", "R$ 150,00"), 
                ("Cardiologista", img_dict.get('cardio'), "Dr. Roberto Souza", "R$ 200,00"),
                ("Dermatologista", img_dict.get('dermato'), "Dra. Juliana Mendes", "R$ 180,00"),
                ("Ortopedista", img_dict.get('ortopedista'), "Dr. Fernando Torres", "R$ 160,00")
            ]
        buscador.entry.delete(0, END)
        atualizar_grid_pesquisa()
        mostrar_frame(frame_passo2)

    def iniciar_agendamentos():
        nonlocal indice_agendamento_atual
        if not pedidos_selecionados:
            messagebox.showwarning("Atenção", "Selecione pelo menos uma opção para avançar.")
            return
        indice_agendamento_atual = 0
        
        nonlocal mes_visualizado, ano_visualizado
        hoje = datetime.now()
        mes_visualizado = hoje.month
        ano_visualizado = hoje.year
        
        preparar_tela_data_hora()

    # ANA: calendario tava bugando dia 31, refiz com a lib calendar setando firstweekday=6
    def desenhar_grid_calendario():
        for widget in grid_data.winfo_children():
            widget.destroy()

        botoes_data_ativos.clear()

        nome_mes = MESES_PT[mes_visualizado]
        lbl_mes_ano.config(text=f"{nome_mes} {ano_visualizado}")

        hoje = datetime.now()
        pedido_ativo = pedidos_selecionados[indice_agendamento_atual]

        dias_headers = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]

        for col, nome in enumerate(dias_headers):
            Label(
                grid_data,
                text=nome,
                font=("Nunito", 14, "bold"),
                bg=C_VERDE_BASE,
                fg=C_BRANCO
            ).grid(row=0, column=col, pady=(0, 5))

        cal = calendar.Calendar(firstweekday=6)

        semanas = cal.monthdayscalendar(
            ano_visualizado,
            mes_visualizado
        )

        for linha, semana in enumerate(semanas, start=1):

            for coluna, dia in enumerate(semana):

                if dia == 0:
                    continue

                data_iteracao = datetime(
                    ano_visualizado,
                    mes_visualizado,
                    dia
                )

                data_str = data_iteracao.strftime("%d/%m/%Y")

                btn_d = BotaoData(
                    grid_data,
                    dia_mes=str(dia),
                    data_completa=data_str,
                    command_select=selecionar_data
                )

                fim_de_semana = data_iteracao.weekday() in (5, 6)

                dia_passado = data_iteracao.date() < hoje.date()

                if fim_de_semana or dia_passado:
                    btn_d.set_estado("desativado")

                elif pedido_ativo["data"] == data_str:
                    btn_d.set_estado("selecionado")

                btn_d.grid(
                    row=linha,
                    column=coluna,
                    padx=3,
                    pady=2
                )

                botoes_data_ativos.append(btn_d)

                coluna += 1

                if coluna > 6:
                    coluna = 0
                    linha += 1

                botoes_data_ativos.append(btn_d)

    def mes_anterior():
        nonlocal mes_visualizado, ano_visualizado
        hoje = datetime.now()
        if ano_visualizado == hoje.year and mes_visualizado <= hoje.month:
            return
            
        mes_visualizado -= 1
        if mes_visualizado < 1:
            mes_visualizado = 12
            ano_visualizado -= 1
        desenhar_grid_calendario()

    def mes_seguinte():
        nonlocal mes_visualizado, ano_visualizado
        mes_visualizado += 1
        if mes_visualizado > 12:
            mes_visualizado = 1
            ano_visualizado += 1
        desenhar_grid_calendario()

    def preparar_tela_data_hora():
        pedido = pedidos_selecionados[indice_agendamento_atual] # <--- mudei os timeslots pra testar a grade de horários - ANA
        
        lbl_resumo_servico_p3.config(
            text=f"   Passo {indice_agendamento_atual+1} de {len(pedidos_selecionados)}: {pedido['profissional']}  |  {pedido['preco']}",
            image=pedido["imagem"],
            compound=LEFT
        )

        desenhar_grid_calendario()

        for widget in grid_horarios.winfo_children(): widget.destroy()
        botoes_horario_ativos.clear()

        prof = pedido["profissional"]
        if "Hemograma" in prof:
            horarios = ["07:00", "07:30", "08:00", "08:30", "09:00", "09:30", "10:00"]
        elif "Raio-X" in prof:
            horarios = ["08:00", "10:00", "14:00", "16:00"]
        elif "Endoscopia" in prof:
            horarios = ["08:00", "09:00", "10:00"]
        elif "Eletrocardiograma" in prof:
            horarios = ["13:00", "14:00", "15:00"]
        elif "Tomografia" in prof:
            horarios = ["14:30", "15:30", "16:30"]
        elif "Glicemia" in prof:
            horarios = ["07:00", "07:15", "07:30", "07:45"]
        elif "Ultrassom" in prof:
            horarios = ["09:00", "11:00", "15:00", "17:00"]
        elif "Clínico Geral" in prof:
            horarios = ["08:00", "09:00", "14:00", "15:00"]
        elif "Pediatra" in prof:
            horarios = ["08:00", "08:45", "09:30", "10:15", "11:00"]
        elif "Cardiologista" in prof:
            horarios = ["14:00", "14:40", "15:20", "16:00", "16:40"]
        elif "Dermatologista" in prof:
            horarios = ["10:00", "10:30", "11:00", "11:30"]
        elif "Ortopedista" in prof:
            horarios = ["16:00", "16:30", "17:00", "17:30"]
        else:
            horarios = ["08:00", "09:00", "14:00", "15:00"]

        for i, h in enumerate(horarios):
            row, col = i // 3, i % 3
            btn_h = BotaoHorario(grid_horarios, horario=h, command_select=selecionar_horario)
            if pedido["horario"] == h: btn_h.set_selecionado(True)
            btn_h.grid(row=row, column=col, padx=8, pady=5)
            botoes_horario_ativos.append(btn_h)

        mostrar_frame(frame_passo3)

    def avancar_data_hora():
        nonlocal indice_agendamento_atual
        pedido = pedidos_selecionados[indice_agendamento_atual]
        
        if not pedido["data"] or not pedido["horario"]:
            messagebox.showwarning("Atenção", "Selecione a data e o horário para este serviço.")
            return
            
        indice_agendamento_atual += 1
        if indice_agendamento_atual < len(pedidos_selecionados):
            preparar_tela_data_hora()
        else:
            ir_para_confirmacao()

    def voltar_passo3():
        nonlocal indice_agendamento_atual
        if indice_agendamento_atual > 0:
            indice_agendamento_atual -= 1
            preparar_tela_data_hora()
        else:
            mostrar_frame(frame_passo2)
            
    def voltar_da_confirmacao():
        nonlocal indice_agendamento_atual
        indice_agendamento_atual = len(pedidos_selecionados) - 1
        preparar_tela_data_hora()

    def selecionar_data(botao_clicado):
        for btn in botoes_data_ativos:
            if btn.estado == "desativado": continue
            btn.set_estado("selecionado" if btn == botao_clicado else ("normal" if btn.estado != "desativado" else "desativado"))
        pedidos_selecionados[indice_agendamento_atual]["data"] = botao_clicado.valor

    def selecionar_horario(botao_clicado):
        for btn in botoes_horario_ativos:
            btn.set_selecionado(btn == botao_clicado)
        pedidos_selecionados[indice_agendamento_atual]["horario"] = botao_clicado.valor

    def ir_para_confirmacao():
        for widget in caixa_confirmacao.winfo_children(): widget.destroy()
        
        frame_itens_conf = Frame(caixa_confirmacao, bg=C_BRANCO)
        frame_itens_conf.pack(fill=X)
        frame_itens_conf.columnconfigure(0, weight=1)
        frame_itens_conf.columnconfigure(1, weight=1)

        for i, p in enumerate(pedidos_selecionados):
            linha = Frame(frame_itens_conf, bg=C_BRANCO)
            linha.grid(row=i//2, column=i%2, padx=10, pady=5, sticky="w")
            
            if p["imagem"]:
                img_lbl = Label(linha, image=p["imagem"], bg=C_BRANCO)
                img_lbl.pack(side=LEFT, padx=(0, 10))
            
            info_frame = Frame(linha, bg=C_BRANCO)
            info_frame.pack(side=LEFT, fill=BOTH, expand=True)
            
            Label(info_frame, text=f"{p['profissional']}", font=("Nunito", 16, "bold"), bg=C_BRANCO, fg=C_VERDE_ESCURO, anchor=W).pack(fill=X)
            Label(info_frame, text=f"{p['data']} às {p['horario']} | {p['preco']}", font=("Nunito", 14), bg=C_BRANCO, fg=C_PRETO, anchor=W).pack(fill=X)
            
        Label(caixa_confirmacao, text=f"Total a Pagar: {calcular_total_pedidos()}", font=("Nunito", 24, "bold"), bg=C_BRANCO, fg=C_AZUL_MARINHO, anchor=E).pack(fill=X, pady=(20, 0))

        mostrar_frame(frame_passo3_meio)

    def confirmar_pedido():
        # ENRIQUE: persistencia final no bd
        conn = sqlite3.connect('banco_pedidos.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT, cpf_cliente TEXT, tipo_servico TEXT, 
            profissional_procedimento TEXT, data_agendamento TEXT, horario_agendamento TEXT)''')
        try: cursor.execute("ALTER TABLE agendamentos ADD COLUMN valor TEXT")
        except sqlite3.OperationalError: pass 
            
        try:
            primeiro_id = None
            for p in pedidos_selecionados:
                cursor.execute('''INSERT INTO agendamentos (cpf_cliente, tipo_servico, profissional_procedimento, data_agendamento, horario_agendamento, valor)
                    VALUES (?, ?, ?, ?, ?, ?)''', (cpf_cliente, p["tipo"], p["profissional"], p["data"], p["horario"], p["preco"]))
                if primeiro_id is None:
                    primeiro_id = cursor.lastrowid
                    
            conn.commit()
            numero_ticket = f"{(primeiro_id + 1000):04d}"
            lbl_num_ticket.config(text=f"#{numero_ticket}")
            
            for widget in caixa_recibo.winfo_children(): widget.destroy()
            Label(caixa_recibo, text=f"Ticket: #{numero_ticket} | CPF: {cpf_cliente}", font=("Nunito", 18, "bold"), bg=C_BRANCO, fg=C_PRETO, anchor=W).pack(fill=X, pady=(0, 10))
            
            for p in pedidos_selecionados:
                texto_item = f"• {p['profissional']} ({p['data']} às {p['horario']}) - {p['preco']}"
                Label(caixa_recibo, text=texto_item, font=("Nunito", 16), bg=C_BRANCO, fg=C_PRETO, anchor=W).pack(fill=X, pady=2)

            Label(caixa_recibo, text=f"Total do Pedido: {calcular_total_pedidos()}", font=("Nunito", 20, "bold"), bg=C_BRANCO, fg=C_AZUL_MARINHO, anchor=W).pack(fill=X, pady=(15, 0))
            
            mostrar_frame(frame_passo4)
        except Exception as e: messagebox.showerror("Erro", f"Erro ao salvar: {e}")
        finally: conn.close()

    def scroll_universal(event):
        if frame_passo2.winfo_ismapped():
            canvas_scroll.yview_scroll(int(-1*(event.delta/120)), "units")
        elif frame_meus_agendamentos.winfo_ismapped():
            canvas_scroll_ag.yview_scroll(int(-1*(event.delta/120)), "units")

    janela.bind_all("<MouseWheel>", scroll_universal)

    # PAULO: ================= frames das telas abaixo, arrumei o bug do footer sumindo =================
    frame_meus_agendamentos = Frame(janela, bg=C_VERDE_BASE)
    criar_cabecalho(frame_meus_agendamentos, titulo="Meus Agendamentos")

    corpo_verde_ag = Frame(frame_meus_agendamentos, bg=C_VERDE_BASE)
    corpo_verde_ag.pack(fill=BOTH, expand=True)

    rodape_ag = Frame(corpo_verde_ag, bg=C_VERDE_BASE)
    rodape_ag.pack(side=BOTTOM, fill=X, pady=15, padx=80) 
    BotaoArredondado(rodape_ag, text="🡄 Voltar Menu", bg_color=C_VERMELHO, fg_color=C_BRANCO, font=("Nunito", 18, "bold"), command=lambda: mostrar_frame(frame_passo1), width=220, height=60, radius=15).pack(side=LEFT)

    frame_busca_ag = Frame(corpo_verde_ag, bg=C_VERDE_BASE)
    frame_busca_ag.pack(pady=10)
    buscador_agendamentos = BuscadorArredondado(frame_busca_ag, command_keyrelease=atualizar_lista_agendamentos)
    buscador_agendamentos.pack()

    frame_scroll_ag = Frame(corpo_verde_ag, bg=C_VERDE_BASE)
    frame_scroll_ag.pack(fill=BOTH, expand=True, padx=80, pady=5)
    
    canvas_scroll_ag = Canvas(frame_scroll_ag, bg=C_VERDE_BASE, highlightthickness=0)
    scrollbar_ag = Scrollbar(frame_scroll_ag, orient="vertical", command=canvas_scroll_ag.yview)
    scroll_agendamentos_interno = Frame(canvas_scroll_ag, bg=C_VERDE_BASE)
    scroll_agendamentos_interno.bind("<Configure>", lambda e: canvas_scroll_ag.configure(scrollregion=canvas_scroll_ag.bbox("all")))
    janela_canvas_id_ag = canvas_scroll_ag.create_window((0, 0), window=scroll_agendamentos_interno, anchor="n")
    canvas_scroll_ag.bind('<Configure>', lambda e: canvas_scroll_ag.coords(janela_canvas_id_ag, e.width/2, 0))
    canvas_scroll_ag.configure(yscrollcommand=scrollbar_ag.set)
    canvas_scroll_ag.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar_ag.pack(side=RIGHT, fill=Y)

    frame_passo1 = Frame(janela, bg=C_VERDE_BASE)
    criar_cabecalho(frame_passo1, titulo="Menu de Atendimento")
    
    rodape_p1 = Frame(frame_passo1, bg=C_VERDE_BASE, height=100)
    rodape_p1.pack(side=BOTTOM, fill=X)
    rodape_p1.pack_propagate(False)

    corpo_verde_1 = Frame(frame_passo1, bg=C_VERDE_BASE)
    corpo_verde_1.pack(fill=BOTH, expand=True)
    
    container_gigante_1 = Frame(corpo_verde_1, bg=C_VERDE_BASE)
    container_gigante_1.place(relx=0.5, rely=0.5, anchor="center")
    BotaoArredondado(container_gigante_1, text="Consultas/\nExames", bg_color=C_BRANCO, fg_color=C_AZUL_MARINHO, font=("Nunito", 32, "bold"), command=lambda: mostrar_frame(frame_passo1_meio), radius=45, image=img_dict.get('exame_consulta_btn'), width=400, height=360).pack(side=LEFT, padx=30)
    BotaoArredondado(container_gigante_1, text="Meus\nAgendamentos", bg_color=C_AZUL_MARINHO, fg_color=C_BRANCO, font=("Nunito", 32, "bold"), command=abrir_meus_agendamentos, radius=45, image=img_dict.get('agenda_btn'), width=400, height=360).pack(side=RIGHT, padx=30)

    frame_passo1_meio = Frame(janela, bg=C_VERDE_BASE)
    criar_cabecalho(frame_passo1_meio, titulo="Selecione o Tipo de Serviço")

    rodape_p1_meio = Frame(frame_passo1_meio, bg=C_VERDE_BASE, height=100)
    rodape_p1_meio.pack(side=BOTTOM, fill=X)
    rodape_p1_meio.pack_propagate(False)
    BotaoArredondado(rodape_p1_meio, text="🡄 Voltar Menu", bg_color=C_VERMELHO, fg_color=C_BRANCO, font=("Nunito", 18, "bold"), command=lambda: mostrar_frame(frame_passo1), width=200, height=60, radius=15).pack(side=LEFT, padx=80, pady=20)

    corpo_verde_m = Frame(frame_passo1_meio, bg=C_VERDE_BASE)
    corpo_verde_m.pack(fill=BOTH, expand=True)
    
    container_gigante_m = Frame(corpo_verde_m, bg=C_VERDE_BASE)
    container_gigante_m.place(relx=0.5, rely=0.5, anchor="center")
    BotaoArredondado(container_gigante_m, text="Exames", bg_color=C_BRANCO, fg_color=C_AZUL_MARINHO, font=("Nunito", 32, "bold"), command=lambda: montar_carrossel("Exame"), radius=45, image=img_dict.get('exame_only_btn'), width=400, height=360).pack(side=LEFT, padx=30)
    BotaoArredondado(container_gigante_m, text="Consultas", bg_color=C_AZUL_MARINHO, fg_color=C_BRANCO, font=("Nunito", 32, "bold"), command=lambda: montar_carrossel("Consulta"), radius=45, image=img_dict.get('consulta_only_btn'), width=400, height=360).pack(side=RIGHT, padx=30)

    frame_passo2 = Frame(janela, bg=C_VERDE_BASE)
    lbl_titulo_carrossel = criar_cabecalho(frame_passo2, titulo="Selecione")

    corpo_verde_2 = Frame(frame_passo2, bg=C_VERDE_BASE)
    corpo_verde_2.pack(fill=BOTH, expand=True)

    rodape_p2 = Frame(corpo_verde_2, bg=C_VERDE_BASE)
    rodape_p2.pack(side=BOTTOM, fill=X, pady=15, padx=80) 
    BotaoArredondado(rodape_p2, text="🡄 Voltar", bg_color=C_VERMELHO, fg_color=C_BRANCO, font=("Nunito", 18, "bold"), command=lambda: mostrar_frame(frame_passo1_meio), width=180, height=60, radius=15).pack(side=LEFT)
    BotaoArredondado(rodape_p2, text="Avançar ➔", bg_color=C_AZUL_MARINHO, fg_color=C_BRANCO, font=("Nunito", 18, "bold"), command=iniciar_agendamentos, width=220, height=60, radius=15).pack(side=RIGHT)

    frame_busca = Frame(corpo_verde_2, bg=C_VERDE_BASE)
    frame_busca.pack(pady=10)
    buscador = BuscadorArredondado(frame_busca, command_keyrelease=atualizar_grid_pesquisa)
    buscador.pack()

    frame_scroll = Frame(corpo_verde_2, bg=C_VERDE_BASE)
    frame_scroll.pack(fill=BOTH, expand=True, padx=80, pady=5)
    
    canvas_scroll = Canvas(frame_scroll, bg=C_VERDE_BASE, highlightthickness=0)
    scrollbar = Scrollbar(frame_scroll, orient="vertical", command=canvas_scroll.yview)
    scroll_interno = Frame(canvas_scroll, bg=C_VERDE_BASE)
    scroll_interno.bind("<Configure>", lambda e: canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all")))
    janela_canvas_id = canvas_scroll.create_window((0, 0), window=scroll_interno, anchor="n")
    canvas_scroll.bind('<Configure>', lambda e: canvas_scroll.coords(janela_canvas_id, e.width/2, 0))
    canvas_scroll.configure(yscrollcommand=scrollbar.set)
    canvas_scroll.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    frame_passo3 = Frame(janela, bg=C_VERDE_BASE)
    criar_cabecalho(frame_passo3, titulo="Selecione a Data e Horário")
    
    corpo_verde_3 = Frame(frame_passo3, bg=C_VERDE_BASE)
    corpo_verde_3.pack(fill=BOTH, expand=True)

    rodape_p3 = Frame(corpo_verde_3, bg=C_VERDE_BASE)
    rodape_p3.pack(side=BOTTOM, fill=X, pady=15, padx=80) 
    BotaoArredondado(rodape_p3, text="🡄 Voltar", bg_color=C_VERMELHO, fg_color=C_BRANCO, font=("Nunito", 18, "bold"), command=voltar_passo3, width=180, height=60, radius=15).pack(side=LEFT)
    BotaoArredondado(rodape_p3, text="Avançar ➔", bg_color=C_AZUL_MARINHO, fg_color=C_BRANCO, font=("Nunito", 18, "bold"), command=avancar_data_hora, width=220, height=60, radius=15).pack(side=RIGHT)

    lbl_resumo_servico_p3 = Label(corpo_verde_3, text="", font=("Nunito", 20, "bold"), bg=C_VERDE_BASE, fg=C_BRANCO, padx=20)
    lbl_resumo_servico_p3.pack(side=TOP, pady=(5, 0))

    form_container = Frame(corpo_verde_3, bg=C_VERDE_BASE)
    form_container.pack(fill=BOTH, expand=True, padx=40, pady=5)

    frame_col_esquerda = Frame(form_container, bg=C_VERDE_BASE)
    frame_col_esquerda.pack(side=LEFT, fill=BOTH, expand=True, padx=20)
    
    Label(frame_col_esquerda, text="Data do Atendimento:", font=("Nunito", 18, "bold"), bg=C_VERDE_BASE, fg=C_BRANCO).pack(anchor=W, pady=(0, 2))
    
    nav_frame = Frame(frame_col_esquerda, bg=C_VERDE_BASE)
    nav_frame.pack(fill=X, pady=2)
    BotaoArredondado(nav_frame, text="<", bg_color=C_BRANCO, fg_color=C_AZUL_MARINHO, font=("Nunito", 16, "bold"), command=mes_anterior, width=40, height=40, radius=10).pack(side=LEFT)
    lbl_mes_ano = Label(nav_frame, text="", font=("Nunito", 18, "bold"), bg=C_VERDE_BASE, fg=C_BRANCO, width=15)
    lbl_mes_ano.pack(side=LEFT, padx=10)
    BotaoArredondado(nav_frame, text=">", bg_color=C_BRANCO, fg_color=C_AZUL_MARINHO, font=("Nunito", 16, "bold"), command=mes_seguinte, width=40, height=40, radius=10).pack(side=LEFT)

    grid_data = Frame(frame_col_esquerda, bg=C_VERDE_BASE)
    grid_data.pack(anchor=W, pady=0)

    frame_col_direita = Frame(form_container, bg=C_VERDE_BASE)
    frame_col_direita.pack(side=RIGHT, fill=BOTH, expand=True, padx=20)
    Label(frame_col_direita, text="Horário:", font=("Nunito", 18, "bold"), bg=C_VERDE_BASE, fg=C_BRANCO).pack(anchor=W, pady=(0, 10))
    
    wrapper_grade = Frame(frame_col_direita, bg=C_VERDE_BASE)
    wrapper_grade.pack(anchor=W)
    grid_horarios = Frame(wrapper_grade, bg=C_VERDE_BASE)
    grid_horarios.pack()

    frame_passo3_meio = Frame(janela, bg=C_VERDE_BASE)
    criar_cabecalho(frame_passo3_meio, titulo="Confirme seu Agendamento")

    corpo_verde_3_meio = Frame(frame_passo3_meio, bg=C_VERDE_BASE)
    corpo_verde_3_meio.pack(fill=BOTH, expand=True)

    rodape_p3_meio = Frame(corpo_verde_3_meio, bg=C_VERDE_BASE)
    rodape_p3_meio.pack(side=BOTTOM, fill=X, pady=20, padx=80) 
    BotaoArredondado(rodape_p3_meio, text="🡄 Voltar", bg_color=C_VERMELHO, fg_color=C_BRANCO, font=("Nunito", 18, "bold"), command=voltar_da_confirmacao, width=180, height=60, radius=15).pack(side=LEFT)
    BotaoArredondado(rodape_p3_meio, text="Confirmar Pedido ✔", bg_color=C_AZUL_MARINHO, fg_color=C_BRANCO, font=("Nunito", 20, "bold"), command=confirmar_pedido, width=320, height=65, radius=20).pack(side=RIGHT)

    centro_confirmacao = Frame(corpo_verde_3_meio, bg=C_VERDE_BASE)
    centro_confirmacao.pack(fill=BOTH, expand=True, pady=10) 

    Label(centro_confirmacao, text="Por favor, revise as informações abaixo:", font=("Nunito", 24, "bold"), bg=C_VERDE_BASE, fg=C_BRANCO).pack(pady=(20, 10))

    caixa_confirmacao = Frame(centro_confirmacao, bg=C_BRANCO, highlightbackground=C_AZUL_MARINHO, highlightthickness=3, padx=50, pady=20, width=800)
    caixa_confirmacao.pack(fill=X, padx=150)

    frame_passo4 = Frame(janela, bg=C_VERDE_BASE)
    criar_cabecalho(frame_passo4, titulo="Atendimento Concluído")

    corpo_verde_4 = Frame(frame_passo4, bg=C_VERDE_BASE)
    corpo_verde_4.pack(fill=BOTH, expand=True)

    rodape_p4 = Frame(corpo_verde_4, bg=C_VERDE_BASE)
    rodape_p4.pack(side=BOTTOM, fill=X, pady=20) 
    BotaoArredondado(rodape_p4, text="VOLTAR AO INÍCIO", bg_color=C_AZUL_MARINHO, fg_color=C_BRANCO, font=("Nunito", 18, "bold"), command=voltar_ao_inicio_fluxo, height=65, width=350).pack(pady=10)

    centro_ticket = Frame(corpo_verde_4, bg=C_VERDE_BASE)
    centro_ticket.pack(fill=BOTH, expand=True, pady=10)
    
    Label(centro_ticket, text="Pedido Finalizado com Sucesso!", font=("Nunito", 20, "bold"), bg=C_VERDE_BASE, fg=C_BRANCO).pack(pady=(10, 5))
    Label(centro_ticket, text="Guarde seu número de chamada:", font=("Nunito", 18), bg=C_VERDE_BASE, fg=C_BRANCO).pack()
    
    lbl_num_ticket = Label(centro_ticket, text="#0000", font=("Nunito", 60, "bold"), bg=C_VERDE_BASE, fg=C_AZUL_MARINHO)
    lbl_num_ticket.pack(pady=(5, 10))

    caixa_recibo = Frame(centro_ticket, bg=C_BRANCO, highlightbackground=C_AZUL_MARINHO, highlightthickness=3, padx=40, pady=20, width=700)
    caixa_recibo.pack(fill=X, padx=150)

    mostrar_frame(frame_passo1)
    if not root: janela.mainloop()

if __name__ == "__main__":
    iniciar_pdv("123.456.789-00")