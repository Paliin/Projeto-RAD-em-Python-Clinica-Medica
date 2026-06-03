from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import sys
import os
from PIL import Image, ImageTk
from datetime import datetime, timedelta

# =========================================================
# PALETA DE CORES GLOBAL (Single Source of Truth)
# =========================================================
C_VERDE_BASE   = "#41A77A"  
C_VERDE_ESCURO = "#2A6B4B"  
C_AZUL_MARINHO = "#115272"  
C_VERMELHO     = "#E7272D"  
C_BRANCO       = "#FFFFFF"
C_CINZA_FUNDO  = "#F9F9F9"
C_CINZA_TEXTO  = "gray"
C_PRETO        = "black"

# ---------------------------------------------------------
# CLASSE: Botão Arredondado Genérico
# ---------------------------------------------------------
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

# ---------------------------------------------------------
# CLASSE: Botão de Opção (Carrossel de Exames)
# ---------------------------------------------------------
class BotOpcao(Canvas):
    def __init__(self, master, text, image, valor, command_select, **kwargs):
        super().__init__(master, bg=C_BRANCO, highlightthickness=0, width=650, height=110, **kwargs)
        self.text = text
        self.imagem = image
        self.valor = valor
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
            cor_base, cor_interna, cor_texto = "#76847D", "#515B56", "#D0D0D0"
        else:
            cor_base, cor_interna, cor_texto = C_VERDE_BASE, C_VERDE_ESCURO, C_BRANCO

        def draw_round_rect(x1, y1, x2, y2, r, cor):
            self.create_oval(x1, y1, x1+r*2, y1+r*2, fill=cor, outline="")
            self.create_oval(x2-r*2, y1, x2, y1+r*2, fill=cor, outline="")
            self.create_oval(x1, y2-r*2, x1+r*2, y2, fill=cor, outline="")
            self.create_oval(x2-r*2, y2-r*2, x2, y2, fill=cor, outline="")
            self.create_rectangle(x1+r, y1, x2-r, y2, fill=cor, outline="")
            self.create_rectangle(x1, y1+r, x2, y2-r, fill=cor, outline="")

        draw_round_rect(0, 0, w, h, r, cor_base)
        draw_round_rect(15, 15, 120, h-15, 20, cor_interna)
        if self.imagem: self.create_image(67, h/2, image=self.imagem)
        self.create_text(150, h/2, text=self.text, font=("Nunito", 24, "bold"), fill=cor_texto, anchor=W)

    def on_click(self, event):
        if self.command_select: self.command_select(self)

    def set_estado(self, novo_estado):
        self.estado = novo_estado
        self.desenhar()

# ---------------------------------------------------------
# CLASSE: Botão de Data (Calendário Visual)
# ---------------------------------------------------------
class BotaoData(Canvas):
    def __init__(self, master, dia_semana, dia_mes, data_completa, command_select, **kwargs):
        super().__init__(master, bg=C_BRANCO, highlightthickness=0, width=95, height=110, **kwargs)
        self.dia_semana = dia_semana
        self.dia_mes = dia_mes
        self.valor = data_completa
        self.command_select = command_select
        self.estado = "normal" 
        self.config(cursor="hand2")
        self.bind("<Configure>", self.desenhar)
        self.bind("<ButtonRelease-1>", self.on_click)

    def desenhar(self, event=None):
        self.delete("all")
        w, h, r = self.winfo_width(), self.winfo_height(), 15
        if w < r*2 or h < r*2: return

        if self.estado == "escurecido":
            cor_topo, cor_base, cor_texto = "#515B56", "#76847D", "#D0D0D0"
        else:
            cor_topo, cor_base, cor_texto = C_VERDE_ESCURO, C_VERDE_BASE, C_BRANCO

        self.create_oval(0, 0, r*2, r*2, fill=cor_base, outline="")
        self.create_oval(w-r*2, 0, w, r*2, fill=cor_base, outline="")
        self.create_oval(0, h-r*2, r*2, h, fill=cor_base, outline="")
        self.create_oval(w-r*2, h-r*2, w, h, fill=cor_base, outline="")
        self.create_rectangle(r, 0, w-r, h, fill=cor_base, outline="")
        self.create_rectangle(0, r, w, h-r, fill=cor_base, outline="")

        altura_topo = h * 0.35
        self.create_oval(0, 0, r*2, r*2, fill=cor_topo, outline="")
        self.create_oval(w-r*2, 0, w, r*2, fill=cor_topo, outline="")
        self.create_rectangle(r, 0, w-r, r, fill=cor_topo, outline="")
        self.create_rectangle(0, r, w, altura_topo, fill=cor_topo, outline="")

        self.create_text(w/2, altura_topo/2, text=self.dia_semana, font=("Nunito", 16, "bold"), fill=cor_texto)
        self.create_text(w/2, altura_topo + (h-altura_topo)/2, text=self.dia_mes, font=("Nunito", 32, "bold"), fill=cor_texto)

    def on_click(self, event):
        if self.command_select: self.command_select(self)

    def set_estado(self, novo_estado):
        self.estado = novo_estado
        self.desenhar()

# ---------------------------------------------------------
# CLASSE: Botão de Horário (Pílula)
# ---------------------------------------------------------
class BotaoHorario(Canvas):
    def __init__(self, master, horario, command_select, **kwargs):
        super().__init__(master, bg=C_BRANCO, highlightthickness=0, width=130, height=50, **kwargs)
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
            draw_round_rect(0, 0, w, h, r, C_VERDE_BASE)
            fg_color = C_BRANCO
        else:
            draw_round_rect(0, 0, w, h, r, C_VERDE_ESCURO)
            draw_round_rect(2, 2, w-2, h-2, r-2, C_BRANCO)
            fg_color = C_VERDE_ESCURO

        self.create_text(w/2, h/2, text=self.valor, font=("Nunito", 20, "bold"), fill=fg_color)

    def on_click(self, event):
        if self.command_select: self.command_select(self)

    def set_selecionado(self, status):
        self.selecionado = status
        self.desenhar()


# ---------------------------------------------------------
# SISTEMA PRINCIPAL DO PDV
# ---------------------------------------------------------
def iniciar_pdv(cpf_cliente, root=None):
    if root: janela = Toplevel(root)
    else: janela = Tk()
        
    janela.title("Atendimento - Clínica Legal")
    janela.geometry("1280x720")
    janela.state('zoomed')
    janela.resizable(width=True, height=True)
    janela.configure(background=C_BRANCO)

    def alternar_fullscreen_pdv(event=None):
        state = not janela.attributes('-fullscreen')
        janela.attributes('-fullscreen', state)
    janela.bind("<F11>", alternar_fullscreen_pdv)

    def fechar_programa():
        if root: root.destroy()
        else: janela.destroy()
    janela.protocol("WM_DELETE_WINDOW", fechar_programa)

    # --- FUNÇÃO DE LOGOUT SIMPLES ---
    def deslogar_usuario(event=None):
        resposta = messagebox.askyesno(
            "Encerrar Atendimento", 
            "Tem certeza que deseja encerrar seu atendimento e sair?"
        )
        
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

    pedido_atual = {"cpf": cpf_cliente, "tipo": "", "profissional": "", "data": "", "horario": ""}
    
    botoes_carrossel_ativos = []
    botoes_data_ativos = []
    botoes_horario_ativos = []

    # --- Carregando as Imagens ---
    img_dict = {}
    try:
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        
        img_logo_topo = Image.open(os.path.join(diretorio_atual, "Assets", "Logo", "main_logo.png"))
        proporcao_topo = (260 / float(img_logo_topo.size[0]))
        altura_topo_img = int((float(img_logo_topo.size[1]) * float(proporcao_topo)))
        img_dict['logo_topo'] = ImageTk.PhotoImage(img_logo_topo.resize((260, altura_topo_img), Image.Resampling.LANCZOS))
        
        img_dict['sair_btn'] = ImageTk.PhotoImage(Image.open(os.path.join(diretorio_atual, "Assets", "icone_sair.png")).resize((50, 50), Image.Resampling.LANCZOS))
        
        img_dict['exame_consulta_btn'] = ImageTk.PhotoImage(Image.open(os.path.join(diretorio_atual, "Assets", "icone_exame_consulta.png")).resize((130, 130), Image.Resampling.LANCZOS))
        img_dict['agenda_btn'] = ImageTk.PhotoImage(Image.open(os.path.join(diretorio_atual, "Assets", "icone_agenda.png")).resize((130, 130), Image.Resampling.LANCZOS))
        
        img_dict['exame_only_btn'] = ImageTk.PhotoImage(Image.open(os.path.join(diretorio_atual, "Assets", "icone_exame.png")).resize((130, 130), Image.Resampling.LANCZOS))
        img_dict['consulta_only_btn'] = ImageTk.PhotoImage(Image.open(os.path.join(diretorio_atual, "Assets", "icone_consulta.png")).resize((130, 130), Image.Resampling.LANCZOS))
        
        pasta_exames = os.path.join(diretorio_atual, "Assets", "exames")
        img_dict['hemo'] = ImageTk.PhotoImage(Image.open(os.path.join(pasta_exames, "icone_hemograma.png")).resize((55, 55), Image.Resampling.LANCZOS))
        img_dict['raiox'] = ImageTk.PhotoImage(Image.open(os.path.join(pasta_exames, "icone_raiox.png")).resize((55, 55), Image.Resampling.LANCZOS))
        img_dict['endo'] = ImageTk.PhotoImage(Image.open(os.path.join(pasta_exames, "icone_endoscopia.png")).resize((55, 55), Image.Resampling.LANCZOS))
        img_dict['ecg'] = ImageTk.PhotoImage(Image.open(os.path.join(pasta_exames, "icone_electrocardiograma.png")).resize((55, 55), Image.Resampling.LANCZOS))
        img_dict['tomo'] = ImageTk.PhotoImage(Image.open(os.path.join(pasta_exames, "icone_tomografia.png")).resize((55, 55), Image.Resampling.LANCZOS))
    except Exception as e: print(f"Aviso nas imagens: {e}")

    # ---------------------------------------------------------
    # FUNÇÕES DE LÓGICA E NAVEGAÇÃO
    # ---------------------------------------------------------
    def mostrar_frame(frame_destino):
        frame_passo1.pack_forget()
        frame_passo1_meio.pack_forget()
        frame_passo2.pack_forget()
        frame_passo3.pack_forget()
        frame_passo4.pack_forget()
        frame_destino.pack(fill=BOTH, expand=True)

    def abrir_meus_agendamentos():
        conn = sqlite3.connect('banco_pedidos.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='agendamentos'")
        tabela_existe = cursor.fetchone()
        
        historico_texto = ""
        if tabela_existe:
            cursor.execute("SELECT tipo_servico, profissional_procedimento, data_agendamento, horario_agendamento FROM agendamentos WHERE cpf_cliente=?", (cpf_cliente,))
            registros = cursor.fetchall()
            if registros:
                for reg in registros:
                    historico_texto += f"• {reg[0]}: {reg[1]} | {reg[2]} às {reg[3]}\n\n"
            else:
                historico_texto = "Nenhum agendamento encontrado para este cliente."
        else:
            historico_texto = "Nenhum agendamento registrado no sistema ainda."
        
        conn.close()
        messagebox.showinfo(f"Agenda do Cliente - CPF: {cpf_cliente}", historico_texto)

    def selecionar_item_carrossel(botao_clicado):
        if botao_clicado.estado == "selecionado":
            for btn in botoes_carrossel_ativos: btn.set_estado("normal")
            pedido_atual["profissional"] = ""
        else:
            for btn in botoes_carrossel_ativos:
                btn.set_estado("selecionado" if btn == botao_clicado else "escurecido")
            pedido_atual["profissional"] = botao_clicado.valor

    def montar_carrossel(tipo_escolhido):
        pedido_atual["tipo"] = tipo_escolhido
        pedido_atual["profissional"] = ""
        lbl_titulo_carrossel.config(text=f"Selecione {'sua' if tipo_escolhido == 'Consulta' else 'seu'} {tipo_escolhido.lower()}")
        
        for widget in scroll_interno.winfo_children(): widget.destroy()
        botoes_carrossel_ativos.clear()

        if tipo_escolhido == "Exame":
            dados = [
                ("Hemograma", img_dict.get('hemo'), "Hemograma Completo"),
                ("Raio-X", img_dict.get('raiox'), "Raio-X"),
                ("Endoscopia", img_dict.get('endo'), "Endoscopia Digestiva"),
                ("Eletrocardiograma", img_dict.get('ecg'), "Eletrocardiograma"),
                ("Tomografia", img_dict.get('tomo'), "Tomografia Computadorizada")
            ]
        else:
            dados = [("Clínico Geral", None, "Dr. Carlos Silva"), ("Pediatria", None, "Dra. Ana Beatriz"), ("Cardiologia", None, "Dr. Roberto Souza")]

        for texto, img, valor_real in dados:
            btn = BotOpcao(scroll_interno, text=texto, image=img, valor=valor_real, command_select=selecionar_item_carrossel)
            btn.pack(pady=10)
            botoes_carrossel_ativos.append(btn)
        mostrar_frame(frame_passo2)

    def selecionar_data(botao_clicado):
        for btn in botoes_data_ativos:
            btn.set_estado("selecionado" if btn == botao_clicado else "escurecido")
        pedido_atual["data"] = botao_clicado.valor

    def selecionar_horario(botao_clicado):
        for btn in botoes_horario_ativos:
            btn.set_selecionado(btn == botao_clicado)
        pedido_atual["horario"] = botao_clicado.valor

    def ir_para_data_hora():
        if not pedido_atual["profissional"]:
            messagebox.showwarning("Atenção", "Selecione uma opção na lista.")
            return
        
        pedido_atual["data"] = ""
        pedido_atual["horario"] = ""
        
        for widget in scroll_data_interno.winfo_children(): widget.destroy()
        for widget in grid_horarios.winfo_children(): widget.destroy()
        botoes_data_ativos.clear()
        botoes_horario_ativos.clear()

        dias_semana_pt = {0:"Seg", 1:"Ter", 2:"Qua", 3:"Qui", 4:"Sex", 5:"Sáb", 6:"Dom"}
        hoje = datetime.now()
        dias_adicionados = 0
        dia_iteracao = hoje

        while dias_adicionados < 10:
            dia_iteracao += timedelta(days=1)
            if dia_iteracao.weekday() < 5:
                str_semana = dias_semana_pt[dia_iteracao.weekday()]
                str_dia = str(dia_iteracao.day)
                str_completa = dia_iteracao.strftime("%d/%m/%Y")
                
                btn_d = BotaoData(scroll_data_interno, dia_semana=str_semana, dia_mes=str_dia, data_completa=str_completa, command_select=selecionar_data)
                btn_d.pack(side=LEFT, padx=10)
                botoes_data_ativos.append(btn_d)
                dias_adicionados += 1

        prof = pedido_atual["profissional"]
        if "Pediatra" in prof or "Hemograma" in prof:
            horarios = ["08:00", "08:30", "09:00", "09:30", "10:00"]
        elif "Cardio" in prof:
            horarios = ["14:00", "14:30", "15:00", "15:30", "16:00"]
        else:
            horarios = ["08:00", "08:30", "09:00", "14:00", "14:30", "15:00"]

        for i, h in enumerate(horarios):
            row, col = i // 3, i % 3
            btn_h = BotaoHorario(grid_horarios, horario=h, command_select=selecionar_horario)
            btn_h.grid(row=row, column=col, padx=12, pady=12)
            botoes_horario_ativos.append(btn_h)

        mostrar_frame(frame_passo3)

    def confirmar_pedido():
        if not pedido_atual["data"] or not pedido_atual["horario"]:
            messagebox.showwarning("Atenção", "Selecione a data e o horário para confirmar.")
            return

        conn = sqlite3.connect('banco_pedidos.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT, cpf_cliente TEXT, tipo_servico TEXT, 
            profissional_procedimento TEXT, data_agendamento TEXT, horario_agendamento TEXT)''')
        try:
            cursor.execute('''INSERT INTO agendamentos (cpf_cliente, tipo_servico, profissional_procedimento, data_agendamento, horario_agendamento)
                VALUES (?, ?, ?, ?, ?)''', (pedido_atual["cpf"], pedido_atual["tipo"], pedido_atual["profissional"], pedido_atual["data"], pedido_atual["horario"]))
            conn.commit()
            numero_ticket = f"{(cursor.lastrowid + 1000):04d}"
            lbl_num_ticket.config(text=f"#{numero_ticket}")
            lbl_resumo_ticket.config(text=f"Tipo: {pedido_atual['tipo']}\nServiço: {pedido_atual['profissional']}\nData: {pedido_atual['data']}\nHorário: {pedido_atual['horario']}\nCPF: {pedido_atual['cpf']}")
            mostrar_frame(frame_passo4)
        except Exception as e: messagebox.showerror("Erro", f"Erro ao salvar: {e}")
        finally: conn.close()

    # =========================================================
    # CONSTRUÇÃO DAS TELAS (GRID ALINHADO)
    # =========================================================

    # --- PASSO 1: MENU PRINCIPAL ---
    frame_passo1 = Frame(janela, bg=C_VERDE_BASE)
    
    # 1. Cabeçalho exato
    topo_branco_1 = Frame(frame_passo1, bg=C_BRANCO, height=140)
    topo_branco_1.pack(fill=X, side=TOP)
    topo_branco_1.pack_propagate(False)
    
    if img_dict.get('logo_topo'):
        lbl_logo_t1 = Label(topo_branco_1, image=img_dict['logo_topo'], bg=C_BRANCO)
        lbl_logo_t1.pack(side=LEFT, padx=50, pady=15)
        
    btn_sair_container_1 = Frame(topo_branco_1, bg=C_BRANCO, cursor="hand2")
    btn_sair_container_1.pack(side=RIGHT, padx=50, pady=15)
    
    if img_dict.get('sair_btn'):
        lbl_img_sair_1 = Label(btn_sair_container_1, image=img_dict['sair_btn'], bg=C_BRANCO)
        lbl_img_sair_1.pack(side=LEFT)
        lbl_img_sair_1.bind("<Button-1>", deslogar_usuario)
        
    lbl_txt_sair_1 = Label(btn_sair_container_1, text="Sair", font=("Nunito", 28, "bold"), fg=C_VERMELHO, bg=C_BRANCO)
    lbl_txt_sair_1.pack(side=LEFT, padx=(10, 0))
    lbl_txt_sair_1.bind("<Button-1>", deslogar_usuario)
    btn_sair_container_1.bind("<Button-1>", deslogar_usuario)

    # 2. Rodapé de grid (Vazio e travado com height=140)
    rodape_p1 = Frame(frame_passo1, bg=C_VERDE_BASE, height=140)
    rodape_p1.pack(fill=X, side=BOTTOM)
    rodape_p1.pack_propagate(False)

    # 3. Corpo central
    corpo_verde_1 = Frame(frame_passo1, bg=C_VERDE_BASE)
    corpo_verde_1.pack(fill=BOTH, expand=True)

    # 4. Título e Botões na posição exata
    Label(corpo_verde_1, text="Selecione a opção desejada", font=("Nunito", 36, "bold"), bg=C_VERDE_BASE, fg=C_BRANCO).pack(pady=(40, 20))
    
    container_gigante_1 = Frame(corpo_verde_1, bg=C_VERDE_BASE)
    container_gigante_1.place(relx=0.5, rely=0.5, anchor="center")
    
    BotaoArredondado(container_gigante_1, text="Consultas/\nExames", bg_color=C_BRANCO, fg_color=C_AZUL_MARINHO, font=("Nunito", 32, "bold"), command=lambda: mostrar_frame(frame_passo1_meio), radius=45, image=img_dict.get('exame_consulta_btn'), width=400, height=360).pack(side=LEFT, padx=30)
    BotaoArredondado(container_gigante_1, text="Meus\nAgendamentos", bg_color=C_AZUL_MARINHO, fg_color=C_BRANCO, font=("Nunito", 32, "bold"), command=abrir_meus_agendamentos, radius=45, image=img_dict.get('agenda_btn'), width=400, height=360).pack(side=RIGHT, padx=30)


    # --- PASSO 1.5: TELA INTERMEDIÁRIA (Cópia fiel do Grid 1) ---
    frame_passo1_meio = Frame(janela, bg=C_VERDE_BASE)
    
    # 1. Cabeçalho exato
    topo_branco_m = Frame(frame_passo1_meio, bg=C_BRANCO, height=140)
    topo_branco_m.pack(fill=X, side=TOP)
    topo_branco_m.pack_propagate(False)
    
    if img_dict.get('logo_topo'):
        lbl_logo_tm = Label(topo_branco_m, image=img_dict['logo_topo'], bg=C_BRANCO)
        lbl_logo_tm.pack(side=LEFT, padx=50, pady=15)
        
    btn_sair_container_m = Frame(topo_branco_m, bg=C_BRANCO, cursor="hand2")
    btn_sair_container_m.pack(side=RIGHT, padx=50, pady=15)
    
    if img_dict.get('sair_btn'):
        lbl_img_sair_m = Label(btn_sair_container_m, image=img_dict['sair_btn'], bg=C_BRANCO)
        lbl_img_sair_m.pack(side=LEFT)
        lbl_img_sair_m.bind("<Button-1>", deslogar_usuario)
        
    lbl_txt_sair_m = Label(btn_sair_container_m, text="Sair", font=("Nunito", 28, "bold"), fg=C_VERMELHO, bg=C_BRANCO)
    lbl_txt_sair_m.pack(side=LEFT, padx=(10, 0))
    lbl_txt_sair_m.bind("<Button-1>", deslogar_usuario)
    btn_sair_container_m.bind("<Button-1>", deslogar_usuario)

    # 2. Rodapé de grid (Com o botão voltar)
    rodape_p1_meio = Frame(frame_passo1_meio, bg=C_VERDE_BASE, height=140)
    rodape_p1_meio.pack(fill=X, side=BOTTOM)
    rodape_p1_meio.pack_propagate(False)
    
    # Botão de Voltar centralizado verticalmente no rodapé
    BotaoArredondado(rodape_p1_meio, text="🡄 Voltar Menu", bg_color=C_VERMELHO, fg_color=C_BRANCO, font=("Nunito", 18, "bold"), command=lambda: mostrar_frame(frame_passo1), width=200, height=60, radius=15).pack(side=LEFT, padx=120, pady=40)

    # 3. Corpo central
    corpo_verde_m = Frame(frame_passo1_meio, bg=C_VERDE_BASE)
    corpo_verde_m.pack(fill=BOTH, expand=True)

    # 4. Título e Botões na posição exata
    Label(corpo_verde_m, text="Selecione a opção desejada", font=("Nunito", 36, "bold"), bg=C_VERDE_BASE, fg=C_BRANCO).pack(pady=(40, 20))
    
    container_gigante_m = Frame(corpo_verde_m, bg=C_VERDE_BASE)
    container_gigante_m.place(relx=0.5, rely=0.5, anchor="center")
    
    BotaoArredondado(container_gigante_m, text="Exames", bg_color=C_BRANCO, fg_color=C_AZUL_MARINHO, font=("Nunito", 32, "bold"), command=lambda: montar_carrossel("Exame"), radius=45, image=img_dict.get('exame_only_btn'), width=400, height=360).pack(side=LEFT, padx=30)
    BotaoArredondado(container_gigante_m, text="Consultas", bg_color=C_AZUL_MARINHO, fg_color=C_BRANCO, font=("Nunito", 32, "bold"), command=lambda: montar_carrossel("Consulta"), radius=45, image=img_dict.get('consulta_only_btn'), width=400, height=360).pack(side=RIGHT, padx=30)


    # --- PASSO 2: LISTA DE SELEÇÃO (CARROSSEL) ---
    frame_passo2 = Frame(janela, bg=C_BRANCO)
    lbl_titulo_carrossel = Label(frame_passo2, text="Selecione seu exame", font=("Nunito", 32, "bold"), bg=C_BRANCO, fg=C_VERDE_ESCURO)
    lbl_titulo_carrossel.pack(pady=(40, 20))

    frame_scroll = Frame(frame_passo2, bg=C_BRANCO)
    frame_scroll.pack(fill=BOTH, expand=True, padx=80, pady=10)
    canvas_scroll = Canvas(frame_scroll, bg=C_BRANCO, highlightthickness=0)
    scrollbar = Scrollbar(frame_scroll, orient="vertical", command=canvas_scroll.yview)
    scroll_interno = Frame(canvas_scroll, bg=C_BRANCO)
    scroll_interno.bind("<Configure>", lambda e: canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all")))
    
    janela_canvas_id = canvas_scroll.create_window((0, 0), window=scroll_interno, anchor="n")
    canvas_scroll.bind('<Configure>', lambda e: canvas_scroll.coords(janela_canvas_id, e.width/2, 0))
    
    canvas_scroll.configure(yscrollcommand=scrollbar.set)
    canvas_scroll.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)
    def _on_mousewheel(event): canvas_scroll.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas_scroll.bind_all("<MouseWheel>", _on_mousewheel)

    rodape_p2 = Frame(frame_passo2, bg=C_BRANCO)
    rodape_p2.pack(fill=X, pady=40, padx=120)
    BotaoArredondado(rodape_p2, text="🡄 Voltar", bg_color=C_VERMELHO, fg_color=C_BRANCO, font=("Nunito", 18, "bold"), command=lambda: mostrar_frame(frame_passo1_meio), width=180, height=60, radius=15).pack(side=LEFT)
    BotaoArredondado(rodape_p2, text="Confirmar ➔", bg_color=C_VERDE_BASE, fg_color=C_BRANCO, font=("Nunito", 18, "bold"), command=ir_para_data_hora, width=220, height=60, radius=15).pack(side=RIGHT)


    # --- PASSO 3: DATA E HORA ---
    frame_passo3 = Frame(janela, bg=C_BRANCO)
    Label(frame_passo3, text="Selecione a Data\ne horario", font=("Nunito", 32, "bold"), bg=C_BRANCO, fg=C_VERDE_ESCURO, justify=CENTER).pack(pady=(40, 20))

    form_container = Frame(frame_passo3, bg=C_BRANCO)
    form_container.pack(fill=BOTH, expand=True, padx=80, pady=10)

    frame_col_esquerda = Frame(form_container, bg=C_BRANCO)
    frame_col_esquerda.pack(side=LEFT, fill=BOTH, expand=True, padx=40)
    Label(frame_col_esquerda, text="Data do Atendimento:", font=("Nunito", 22, "bold"), bg=C_BRANCO, fg=C_VERDE_ESCURO).pack(anchor=W, pady=(10, 15))
    
    frame_scroll_data = Frame(frame_col_esquerda, bg=C_BRANCO)
    frame_scroll_data.pack(fill=X, pady=10)
    canvas_data = Canvas(frame_scroll_data, bg=C_BRANCO, highlightthickness=0, height=130)
    scrollbar_data = Scrollbar(frame_scroll_data, orient="horizontal", command=canvas_data.xview)
    scroll_data_interno = Frame(canvas_data, bg=C_BRANCO)
    scroll_data_interno.bind("<Configure>", lambda e: canvas_data.configure(scrollregion=canvas_data.bbox("all")))
    canvas_data.create_window((0, 0), window=scroll_data_interno, anchor="nw")
    canvas_data.configure(xscrollcommand=scrollbar_data.set)
    canvas_data.pack(fill=X)
    scrollbar_data.pack(fill=X)

    frame_col_direita = Frame(form_container, bg=C_BRANCO)
    frame_col_direita.pack(side=RIGHT, fill=BOTH, expand=True, padx=40)
    Label(frame_col_direita, text="Horario:", font=("Nunito", 22, "bold"), bg=C_BRANCO, fg=C_VERDE_ESCURO).pack(anchor=W, pady=(10, 15))
    
    wrapper_grade = Frame(frame_col_direita, bg=C_BRANCO)
    wrapper_grade.pack(anchor=W)
    grid_horarios = Frame(wrapper_grade, bg=C_BRANCO)
    grid_horarios.pack()

    rodape_p3 = Frame(frame_passo3, bg=C_BRANCO)
    rodape_p3.pack(fill=X, pady=40, padx=120)
    BotaoArredondado(rodape_p3, text="🡄 Voltar", bg_color=C_VERMELHO, fg_color=C_BRANCO, font=("Nunito", 18, "bold"), command=lambda: mostrar_frame(frame_passo2), width=180, height=60, radius=15).pack(side=LEFT)
    BotaoArredondado(rodape_p3, text="Confirmar ➔", bg_color=C_VERDE_BASE, fg_color=C_BRANCO, font=("Nunito", 18, "bold"), command=confirmar_pedido, width=220, height=60, radius=15).pack(side=RIGHT)


    # --- PASSO 4: TICKET FINAL ---
    frame_passo4 = Frame(janela, bg=C_BRANCO)
    centro_ticket = Frame(frame_passo4, bg=C_BRANCO)
    centro_ticket.place(relx=0.5, rely=0.45, anchor="center")
    
    Label(centro_ticket, text="✔ Pedido Finalizado com Sucesso!", font=("Nunito", 32, "bold"), bg=C_BRANCO, fg=C_VERDE_BASE).pack(pady=10)
    Label(centro_ticket, text="Guarde seu número de chamada:", font=("Nunito", 16), bg=C_BRANCO, fg=C_CINZA_TEXTO).pack()
    lbl_num_ticket = Label(centro_ticket, text="#0000", font=("Nunito", 80, "bold"), bg=C_BRANCO, fg=C_PRETO)
    lbl_num_ticket.pack(pady=15)

    caixa_recibo = Frame(centro_ticket, bg=C_CINZA_FUNDO, highlightbackground="#cccccc", highlightthickness=2, padx=30, pady=30, width=550)
    caixa_recibo.pack(fill=X, pady=10)
    lbl_resumo_ticket = Label(caixa_recibo, text="Resumo...", font=("Nunito", 18), bg=C_CINZA_FUNDO, fg=C_PRETO, justify=LEFT)
    lbl_resumo_ticket.pack(anchor=W)

    BotaoArredondado(frame_passo4, text="VOLTAR AO INÍCIO", bg_color="#333333", fg_color=C_BRANCO, font=("Nunito", 18, "bold"), command=deslogar_usuario, height=65, width=350).pack(side=BOTTOM, pady=60)

    mostrar_frame(frame_passo1)
    if not root: janela.mainloop()

if __name__ == "__main__":
    iniciar_pdv("123.456.789-00")