# 🏥 Sistema de Autoatendimento - Clínica Legal

Um sistema de Ponto de Venda (PDV) e Totem de Autoatendimento focado em clínicas médicas, desenvolvido inteiramente em Python. O projeto tem como objetivo proporcionar uma experiência de usuário (UX) fluida e moderna, permitindo que os pacientes agendem consultas e exames de forma autônoma, rápida e intuitiva.

## 🚀 Funcionalidades

* **Autenticação Segura:** Tela de login com validação estrutural de CPF e limitação automática de caracteres.
* **Interface Moderna (UI):** Componentes visuais desenhados do zero com `Canvas`, apresentando botões arredondados, campos de busca em formato de pílula ("pill design") e feedback visual tátil (mudança de cor ao clicar).
* **Agendamento Interativo:**
  * Divisão clara entre **Exames** e **Consultas**.
  * Grade de seleção (Grid) com ícones personalizados para cada especialidade médica.
  * Tabela de preços dinâmica, utilizando como base a média de valores de clínicas populares do estado do Pará.
  * Busca inteligente em tempo real.
* **Calendário Fixo Integrado:** Seleção de datas e horários em layout de calendário moderno (sem barras de rolagem nativas feias), destacando os dias úteis.
* **Sistema de Confirmação:** Tela de resumo exibindo o profissional/exame, data, horário e valor total antes da efetivação do agendamento.
* **Geração de Ticket:** Emissão de um ticket numerado sequencialmente com o resumo do pedido para o paciente acompanhar o atendimento.
* **Gestão do Paciente (Meus Agendamentos):** 
  * Histórico de pedidos salvos no banco de dados.
  * Funcionalidade para cancelar consultas ativas.
  * Opção de reimprimir o ticket físico/digital.

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**: Linguagem base do projeto.
* **Tkinter**: Biblioteca padrão do Python para a construção da Interface Gráfica de Usuário (GUI).
* **SQLite3**: Banco de dados relacional nativo para armazenamento das sessões e dos agendamentos locais (`banco_pedidos.db`).
* **Pillow (PIL)**: Manipulação e redimensionamento assíncrono (LANCZOS) dos ícones e logotipos da interface.
* **PyInstaller**: Utilizado para empacotar o código-fonte em um executável autônomo (`.exe`) para Windows.

## 📁 Estrutura do Projeto

```text
Projeto-RAD-em-Python-Clinica-Medica/
│
├── Assets/                 # Imagens, Ícones e Logotipos da aplicação
│   ├── Logo/               # Ícones (.ico) e logo principal
│   ├── exames/             # Ícones representativos de exames
│   └── consultas/          # Ícones de especialidades médicas
│
├── banco_pedidos.db        # Banco de dados SQLite (gerado automaticamente)
├── tela_login.py           # Ponto de entrada e autenticação do paciente
├── tela_servicos.py        # Core do sistema (Carrossel, Calendário, Tickets)
└── README.md               # Documentação do projeto