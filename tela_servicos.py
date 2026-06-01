from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import sys
import os
from PIL import Image, ImageTk
from datetime import datetime, timedelta # Para gerar as datas dinâmicas

# ---------------------------------------------------------
# CLASSE: Botão Arredondado Simples (Voltar, Confirmar)
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
            self.create_image(w/2, h/2 - 20, image=self.imagem_icone)
            self.create_text(w/2, h/2 + 40, text=self.text, fill=self.fg_color, font=self.font, justify="center")
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
class BotaoOpcao(Canvas):
    def __init__(self, master, text, image, valor, command_select, **kwargs):
        super().__init__(master, bg="white", highlightthickness=0, height=110, **kwargs)
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
            cor_base, cor_interna, cor_texto = "#41A77A", "#2A6B4B", "white"

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
        super().__init__(master, bg="white", highlightthickness=0, width=90, height=100, **kwargs)
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
            cor_topo, cor_base, cor_texto = "#2A6B4B", "#41A77A", "white"

        # Base completa (verde claro)
        self.create_oval(0, 0, r*2, r*2, fill=cor_base, outline="")
        self.create_oval(w-r*2, 0, w, r*2, fill=cor_base, outline="")
        self.create_oval(0, h-r*2, r*2, h, fill=cor_base, outline="")
        self.create_oval(w-r*2, h-r*2, w, h, fill=cor_base, outline="")
        self.create_rectangle(r, 0, w-r, h, fill=cor_base, outline="")
        self.create_rectangle(0, r, w, h-r, fill=cor_base, outline="")

        # Topo (verde escuro)
        altura_topo = h * 0.35
        self.create_oval(0, 0, r*2, r*2, fill=cor_topo, outline="")
        self.create_oval(w-r*2, 0, w, r*2, fill=cor_topo, outline="")
        self.create_rectangle(r, 0, w-r, r, fill=cor_topo, outline="")
        self.create_rectangle(0, r, w, altura_topo, fill=cor_topo, outline="")

        # Textos
        self.create_text(w/2, altura_topo/2, text=self.dia_semana, font=("Nunito", 16, "bold"), fill=cor_texto)
        self.create_text(w/2, altura_topo + (h-altura_topo)/2, text=self.dia_mes, font=("Nunito", 32, "bold"), fill=cor_texto)

    def on_click(self, event):
        if self.command_select: self.command_select(self)

    def set_estado(self, novo_estado):
        self.estado = novo_estado
        self.desenhar()

# ---------------------------------------------------------
# CLASSE: Botão de Horário (Pílula) - CORRIGIDA
# ---------------------------------------------------------
class BotaoHorario(Canvas):
    def __init__(self, master, horario, command_select, **kwargs):
        super().__init__(master, bg="white", highlightthickness=0, width=120, height=45, **kwargs)
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

        # Função auxiliar limpa para desenhar pílulas sólidas
        def draw_round_rect(x1, y1, x2, y2, raio, cor):
            self.create_oval(x1, y1, x1+raio*2, y1+raio*2, fill=cor, outline="")
            self.create_oval(x2-raio*2, y1, x2, y1+raio*2, fill=cor, outline="")
            self.create_oval(x1, y2-raio*2, x1+raio*2, y2, fill=cor, outline="")
            self.create_oval(x2-raio*2, y2-raio*2, x2, y2, fill=cor, outline="")
            self.create_rectangle(x1+raio, y1, x2-raio, y2, fill=cor, outline="")
            self.create_rectangle(x1, y1+raio, x2, y2-raio, fill=cor, outline="")

        if self.selecionado:
            # Se selecionado, desenha a pílula toda verde
            draw_round_rect(0, 0, w, h, r, "#41A77A")
            fg_color = "white"
        else:
            # Se não selecionado, desenha uma base verde escura (que servirá de borda)
            draw_round_rect(0, 0, w, h, r, "#2A6B4B")
            # E desenha uma pílula branca 2 pixels menor por cima (apagando o centro)
            draw_round_rect(2, 2, w-2, h-2, r-2, "white")
            fg_color = "#2A6B4B"

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
    janela.geometry("600x800")
    janela.resizable(width=FALSE, height=FALSE)
    janela.configure(background="white")

    def fechar_programa():
        if root: root.destroy()
        else: janela.destroy()
    janela.protocol("WM_DELETE_WINDOW", fechar_programa)

    cor_verde_escuro = "#2A6B4B"
    cor_verde = "#41A77A"
    cor_azul = "#2E6678"
    cor_vermelha = "#E04F53"
    
    pedido_atual = {"cpf": cpf_cliente, "tipo": "", "profissional": "", "data": "", "horario": ""}
    
    botoes_carrossel_ativos = []
    botoes_data_ativos = []
    botoes_horario_ativos = []

    # --- Carregando as Imagens ---
    img_dict = {}
    try:
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        img_dict['exame_btn'] = ImageTk.PhotoImage(Image.open(os.path.join(diretorio_atual, "Assets", "icone_exame.png")).resize((80, 80), Image.Resampling.LANCZOS))
        img_dict['consulta_btn'] = ImageTk.PhotoImage(Image.open(os.path.join(diretorio_atual, "Assets", "icone_consulta.png")).resize((80, 80), Image.Resampling.LANCZOS))
        
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
        frame_passo2.pack_forget()
        frame_passo3.pack_forget()
        frame_passo4.pack_forget()
        frame_destino.pack(fill=BOTH, expand=True)

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
            btn = BotaoOpcao(scroll_interno, text=texto, image=img, valor=valor_real, command_select=selecionar_item_carrossel)
            btn.pack(fill=X, padx=10, pady=10)
            botoes_carrossel_ativos.append(btn)
        mostrar_frame(frame_passo2)

    # Lógica de Seleção de Data e Hora
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
        
        # Limpa as listas antigas
        for widget in scroll_data_interno.winfo_children(): widget.destroy()
        for widget in grid_horarios.winfo_children(): widget.destroy()
        botoes_data_ativos.clear()
        botoes_horario_ativos.clear()

        # 1. Gerar Datas Dinâmicas (Próximos 10 dias úteis)
        dias_semana_pt = {0:"Seg", 1:"Ter", 2:"Qua", 3:"Qui", 4:"Sex", 5:"Sáb", 6:"Dom"}
        hoje = datetime.now()
        dias_adicionados = 0
        dia_iteracao = hoje

        while dias_adicionados < 10:
            dia_iteracao += timedelta(days=1)
            if dia_iteracao.weekday() < 5: # Ignora Sábado e Domingo
                str_semana = dias_semana_pt[dia_iteracao.weekday()]
                str_dia = str(dia_iteracao.day)
                str_completa = dia_iteracao.strftime("%d/%m/%Y")
                
                btn_d = BotaoData(scroll_data_interno, dia_semana=str_semana, dia_mes=str_dia, data_completa=str_completa, command_select=selecionar_data)
                btn_d.pack(side=LEFT, padx=8)
                botoes_data_ativos.append(btn_d)
                dias_adicionados += 1

        # 2. Gerar Horários Dinâmicos
        prof = pedido_atual["profissional"]
        if "Pediatra" in prof or "Hemograma" in prof:
            horarios = ["08:00", "08:30", "09:00", "09:30", "10:00"]
        elif "Cardio" in prof:
            horarios = ["14:00", "14:30", "15:00", "15:30", "16:00"]
        else:
            horarios = ["08:00", "08:30", "09:00", "14:00", "14:30", "15:00"]

        # Organiza os horários em uma grade (3 colunas)
        for i, h in enumerate(horarios):
            row, col = i // 3, i % 3
            btn_h = BotaoHorario(grid_horarios, horario=h, command_select=selecionar_horario)
            btn_h.grid(row=row, column=col, padx=10, pady=10)
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
    # CONSTRUÇÃO DAS TELAS
    # =========================================================

    # --- PASSO 1: INÍCIO ---
    frame_passo1 = Frame(janela, bg="white")
    Label(frame_passo1, text="Selecione a opção\ndesejada", font=("Nunito", 28, "bold"), bg="white", fg="black", justify=CENTER).pack(pady=(60, 30))
    container_botoes = Frame(frame_passo1, bg="white")
    container_botoes.pack(fill=BOTH, expand=True, padx=70, pady=10)
    BotaoArredondado(container_botoes, text="Exames", bg_color=cor_verde, fg_color="white", font=("Nunito", 32, "bold"), command=lambda: montar_carrossel("Exame"), radius=45, image=img_dict.get('exame_btn')).pack(fill=BOTH, expand=True, pady=(0, 20))
    BotaoArredondado(container_botoes, text="Consultas", bg_color=cor_azul, fg_color="white", font=("Nunito", 32, "bold"), command=lambda: montar_carrossel("Consulta"), radius=45, image=img_dict.get('consulta_btn')).pack(fill=BOTH, expand=True, pady=(20, 60))


    # --- PASSO 2: CARROSSEL DE SELEÇÃO ---
    frame_passo2 = Frame(janela, bg="white")
    lbl_titulo_carrossel = Label(frame_passo2, text="Selecione seu exame", font=("Nunito", 28, "bold"), bg="white", fg=cor_verde_escuro)
    lbl_titulo_carrossel.pack(pady=(40, 10))

    frame_scroll = Frame(frame_passo2, bg="white")
    frame_scroll.pack(fill=BOTH, expand=True, padx=20, pady=10)
    canvas_scroll = Canvas(frame_scroll, bg="white", highlightthickness=0)
    scrollbar = Scrollbar(frame_scroll, orient="vertical", command=canvas_scroll.yview)
    scroll_interno = Frame(canvas_scroll, bg="white")
    scroll_interno.bind("<Configure>", lambda e: canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all")))
    canvas_scroll.create_window((0, 0), window=scroll_interno, anchor="nw", width=530)
    canvas_scroll.configure(yscrollcommand=scrollbar.set)
    canvas_scroll.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)
    def _on_mousewheel(event): canvas_scroll.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas_scroll.bind_all("<MouseWheel>", _on_mousewheel)

    rodape_p2 = Frame(frame_passo2, bg="white")
    rodape_p2.pack(fill=X, pady=30, padx=30)
    BotaoArredondado(rodape_p2, text="🡄 Voltar", bg_color=cor_vermelha, fg_color="white", font=("Nunito", 16, "bold"), command=lambda: mostrar_frame(frame_passo1), width=150, height=55, radius=15).pack(side=LEFT)
    BotaoArredondado(rodape_p2, text="Confirmar ➔", bg_color=cor_verde, fg_color="white", font=("Nunito", 18, "bold"), command=ir_para_data_hora, width=200, height=55, radius=15).pack(side=RIGHT)


    # --- PASSO 3: DATA E HORA ---
    frame_passo3 = Frame(janela, bg="white")
    Label(frame_passo3, text="Selecione a Data\ne horario", font=("Nunito", 28, "bold"), bg="white", fg=cor_verde_escuro, justify=CENTER).pack(pady=(40, 20))

    form_container = Frame(frame_passo3, bg="white")
    form_container.pack(fill=BOTH, expand=True, padx=30)

    # Carrossel Horizontal de Datas
    Label(form_container, text="Data do Atendimento:", font=("Nunito", 18, "bold"), bg="white", fg=cor_verde_escuro).pack(anchor=W, pady=(10, 5))
    
    frame_scroll_data = Frame(form_container, bg="white")
    frame_scroll_data.pack(fill=X, pady=(0, 20))
    canvas_data = Canvas(frame_scroll_data, bg="white", highlightthickness=0, height=120)
    scrollbar_data = Scrollbar(frame_scroll_data, orient="horizontal", command=canvas_data.xview)
    scroll_data_interno = Frame(canvas_data, bg="white")
    scroll_data_interno.bind("<Configure>", lambda e: canvas_data.configure(scrollregion=canvas_data.bbox("all")))
    canvas_data.create_window((0, 0), window=scroll_data_interno, anchor="nw")
    canvas_data.configure(xscrollcommand=scrollbar_data.set)
    canvas_data.pack(fill=X)
    scrollbar_data.pack(fill=X)

    # Grid de Horários
    Label(form_container, text="Horario:", font=("Nunito", 18, "bold"), bg="white", fg=cor_verde_escuro).pack(anchor=W, pady=(10, 5))
    grid_horarios = Frame(form_container, bg="white")
    grid_horarios.pack(anchor=W)

    # Rodapé do Passo 3
    rodape_p3 = Frame(frame_passo3, bg="white")
    rodape_p3.pack(fill=X, pady=30, padx=30)
    BotaoArredondado(rodape_p3, text="🡄 Voltar", bg_color=cor_vermelha, fg_color="white", font=("Nunito", 16, "bold"), command=lambda: mostrar_frame(frame_passo2), width=150, height=55, radius=15).pack(side=LEFT)
    BotaoArredondado(rodape_p3, text="Confirmar ➔", bg_color=cor_verde, fg_color="white", font=("Nunito", 18, "bold"), command=confirmar_pedido, width=200, height=55, radius=15).pack(side=RIGHT)


    # --- PASSO 4: TICKET FINAL ---
    frame_passo4 = Frame(janela, bg="white")
    Label(frame_passo4, text="✔ Pedido Finalizado!", font=("Nunito", 26, "bold"), bg="white", fg=cor_verde).pack(pady=(60, 20))
    Label(frame_passo4, text="Guarde seu número de chamada:", font=("Nunito", 14), bg="white", fg="gray").pack()
    lbl_num_ticket = Label(frame_passo4, text="#0000", font=("Nunito", 70, "bold"), bg="white", fg="black")
    lbl_num_ticket.pack(pady=20)

    caixa_recibo = Frame(frame_passo4, bg="#f9f9f9", highlightbackground="#cccccc", highlightthickness=2, padx=20, pady=20)
    caixa_recibo.pack(fill=X, padx=50, pady=20)
    lbl_resumo_ticket = Label(caixa_recibo, text="Resumo...", font=("Nunito", 16), bg="#f9f9f9", fg="black", justify=LEFT)
    lbl_resumo_ticket.pack(anchor=W)

    BotaoArredondado(frame_passo4, text="NOVO ATENDIMENTO", bg_color="#333333", fg_color="white", font=("Nunito", 16, "bold"), command=fechar_programa, height=60).pack(fill=X, padx=50, side=BOTTOM, pady=40)

    mostrar_frame(frame_passo1)
    if not root: janela.mainloop()

if __name__ == "__main__":
    iniciar_pdv("123.456.789-00")