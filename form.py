import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import csv

class OrdemServico:
    def __init__(self, nome, numero, recebimento, direcionado_para, direcionamento, prazo_recebimento, prazo_devolucao):
        self.nome = nome
        self.numero = numero
        self.recebimento = recebimento
        self.direcionado_para = direcionado_para
        self.direcionamento = direcionamento
        self.prazo_recebimento = prazo_recebimento
        self.prazo_devolucao = prazo_devolucao
        self.entrega = None

    def entregar(self):
        self.entrega = datetime.now()

class GerenciadorOrdensServico:
    def __init__(self):
        self.ordens_servico = []

    def inserir_ordem_servico(self, ordem_servico):
        self.ordens_servico.append(ordem_servico)

    def ordens_servico_pendentes(self):
        return [ordem for ordem in self.ordens_servico if ordem.entrega is None] 
    
    def ordens_servico_concluidas(self):
        return [ordem for ordem in self.ordens_servico if ordem.entrega is not None]

def salvar_ordens_servico(filename, ordens_servico):
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(["Ordem", "Número da Ordem", "Recebimento", "Direcionado para", "Direcionamento", "Prazo Recebimento", "Prazo Devolução", "Entrega"])
            for ordem in ordens_servico:
                # Formatando as datas para o formato desejado
                recebimento = ordem.recebimento.strftime("%d/%m/%Y %H:%M")
                prazo_recebimento = ordem.prazo_recebimento.strftime("%d/%m/%Y")
                prazo_devolucao = ordem.prazo_devolucao.strftime("%d/%m/%Y")
                entrega = ordem.entrega.strftime("%d/%m/%Y %H:%M") if ordem.entrega is not None else ""
                writer.writerow([ordem.nome, ordem.numero, recebimento, ordem.direcionado_para, ordem.direcionamento, prazo_recebimento, prazo_devolucao, entrega])
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar arquivo: FECHE O ARQUIVO EXCEL: ordens_servico.")


def carregar_ordens_servico(filename):
    ordens_servico = []
    try:
        with open(filename, mode='r') as file:
            reader = csv.reader(file, delimiter=';')
            next(reader)  # Pular o cabeçalho
            
            for row in reader:
                if len(row) == 8:  
                    nome, numero, recebimento, direcionado_para, direcionamento, prazo_recebimento, prazo_devolucao, entrega = row
                    if prazo_recebimento and prazo_devolucao:
                        # Convertendo as datas do formato do arquivo para o formato Python
                        recebimento = datetime.strptime(recebimento, "%d/%m/%Y %H:%M")
                        prazo_recebimento = datetime.strptime(prazo_recebimento, "%d/%m/%Y").date()
                        prazo_devolucao = datetime.strptime(prazo_devolucao, "%d/%m/%Y").date()
                        entrega = datetime.strptime(entrega, "%d/%m/%Y %H:%M") if entrega else None
                        ordem = OrdemServico(nome, numero, recebimento, direcionado_para, direcionamento, prazo_recebimento, prazo_devolucao)
                        ordem.entrega = entrega
                        ordens_servico.append(ordem)
                else:
                    print(f"A linha não tem o número correto de valores: {row}")
    except FileNotFoundError:
        return []
    return ordens_servico


def inserir_ordem():
    nome = entry_nome.get()
    numero = entry_numero.get()
    direcionado_para = entry_direcionado_para.get()
    prazo_recebimento = entry_prazo_recebimento.get()
    prazo_devolucao = entry_prazo_devolucao.get()

    if not all([nome, numero, direcionado_para, prazo_recebimento, prazo_devolucao]):
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
        return
    
    try:
        prazo_recebimento = datetime.strptime(prazo_recebimento, "%d/%m/%Y").date()
        prazo_devolucao = datetime.strptime(prazo_devolucao, "%d/%m/%Y").date()
    except ValueError:
        messagebox.showerror("Erro", "Formato de data inválido. Use o formato dd/mm/aaaa.")
        return
    
    
    nova_ordem = OrdemServico(nome, numero, datetime.now(), direcionado_para, datetime.now(), prazo_recebimento, prazo_devolucao)
    gerenciador.inserir_ordem_servico(nova_ordem)
    salvar_ordens_servico("ordens_servico.csv", gerenciador.ordens_servico)

    for label in labels_ordens:
        label.destroy()  # Remove o label da interface gráfica
    for botao in botoes_recebido:
        botao.destroy()  # Remove o botão da interface gráfica
    lista_ordens.delete(0, tk.END)

    # Limpar os campos de entrada e atualizar a lista de ordens pendentes na interface
    entry_nome.delete(0, tk.END)
    entry_numero.delete(0, tk.END)
    entry_direcionado_para.delete(0, tk.END)
    entry_prazo_recebimento.delete(0, tk.END)
    entry_prazo_devolucao.delete(0, tk.END)

    listar_ordens_pendentes()
    messagebox.showinfo("Sucesso", "Ordem de Serviço inserida com sucesso!")

def marcar_recebido(ordem):
    ordem.entregar()
    salvar_ordens_servico("ordens_servico.csv", gerenciador.ordens_servico)
    listar_ordens_concluidas()
    listar_ordens_pendentes()
    messagebox.showinfo("Sucesso", "Ordem de Serviço marcada como recebida!")
    

def listar_ordens_pendentes():
    global labels_ordens  # Declare a lista global para armazenar os labels
    global botoes_recebido  # Declare a lista global para armazenar os botões
    global button_pendentes, button_concluidas
    
    button_pendentes.config(state=tk.DISABLED)
    button_concluidas.config(state=tk.NORMAL)

    lista_ordens.delete(0, tk.END)

    y_position = 190  

    labels_ordens = []
    botoes_recebido = []

    for botao in botoes_recebido:
        botao.destroy()  
    lista_ordens.delete(0, tk.END)

    if labels_ordens:
        for label in labels_ordens:
            label.destroy()  
        labels_ordens = []  
    if botoes_recebido:
        for botao in botoes_recebido:
            botao.destroy()  
        botoes_recebido = []  

    lista_ordens.delete(0, tk.END)  

    for ordem in gerenciador.ordens_servico_pendentes():
        text = f"{ordem.nome} N°{ordem.numero} - Com: {ordem.direcionado_para}  - Prazo: {ordem.prazo_recebimento.strftime('%d/%m/%Y')}"

        # Criar um Label para o texto
        label_ordem = tk.Label(root, text=text)
        label_ordem.place(x=80, y=y_position+10)  # Defina as coordenadas x e y desejadas para o texto
        labels_ordens.append(label_ordem)  # Adicione o label à lista de labels

        # Criar botão para cada ordem
        botao_recebido = tk.Button(root, text="Recebido", command=lambda o=ordem: marcar_recebido(o))
        botao_recebido.place(x=10, y=y_position+8)  # Defina as coordenadas x e y desejadas para o botão
        botoes_recebido.append(botao_recebido)  # Adicione o botão à lista de botões

        # Ajuste a posição y para o próximo texto e botão
        y_position += 40  # Ajuste a posição y conforme necessário para separar os elementos

def listar_ordens_concluidas():
    global labels_ordens
    global botoes_recebido
    global button_pendentes, button_concluidas
    
    button_pendentes.config(state=tk.NORMAL)
    button_concluidas.config(state=tk.DISABLED)
    
    for label in labels_ordens:
        label.destroy()  # Remove o label da interface gráfica
    for botao in botoes_recebido:
        botao.destroy()  # Remove o botão da interface gráfica
    lista_ordens.delete(0, tk.END)

    ordens_concluidas = sorted(gerenciador.ordens_servico_concluidas(), key=lambda x: x.entrega, reverse=True)

    for ordem in ordens_concluidas:
        lista_ordens.insert(tk.END, f"{ordem.nome} N°{ordem.numero} - Resolvido Por: {ordem.direcionado_para} - Data de Entrega: {ordem.entrega.strftime('%d/%m/%Y')}")

# Configuração da interface
root = tk.Tk()
root.title("Gerenciador de Ordens de Serviço")

# Widgets

label_dev = tk.Label(root, text="Feito por: Higor Vital Lopo", font=("Helvetica", 8, "italic"))

label_nome = tk.Label(root, text="Nome da Ordem:")
entry_nome = tk.Entry(root)

label_numero = tk.Label(root, text="Número da Ordem:")
entry_numero = tk.Entry(root)

label_direcionado_para = tk.Label(root, text="Direcionado para:")
entry_direcionado_para = tk.Entry(root)

label_prazo_recebimento = tk.Label(root, text="Prazo de Recebimento (dd/mm/aaaa):")
entry_prazo_recebimento = tk.Entry(root)

label_prazo_devolucao = tk.Label(root, text="Prazo de Devolução (dd/mm/aaaa):")
entry_prazo_devolucao = tk.Entry(root)

button_inserir = tk.Button(root, text="Inserir Ordem de Serviço", command=inserir_ordem)

label_selecionar = tk.Label(root, text="Selecionar Opção:")
button_pendentes = tk.Button(root, text="Listar Ordens de Serviço Pendentes", command=listar_ordens_pendentes, state=tk.DISABLED)
button_concluidas = tk.Button(root, text="Listar Ordens de Serviço Concluídas", command=listar_ordens_concluidas)

lista_ordens = tk.Listbox(root, width=100, height=20)

# Layout

label_dev.grid(row=8, column=0, sticky="w")

label_nome.grid(row=0, column=0, sticky="e")
entry_nome.grid(row=0, column=1)

label_numero.grid(row=1, column=0, sticky="e")
entry_numero.grid(row=1, column=1)

label_direcionado_para.grid(row=2, column=0, sticky="e")
entry_direcionado_para.grid(row=2, column=1)

label_prazo_recebimento.grid(row=3, column=0, sticky="e")
entry_prazo_recebimento.grid(row=3, column=1)

label_prazo_devolucao.grid(row=4, column=0, sticky="e")
entry_prazo_devolucao.grid(row=4, column=1)

button_inserir.grid(row=5, columnspan=2) 
label_selecionar.grid(row=6, column=0, sticky="e")
button_pendentes.grid(row=6, column=1, sticky="w")
button_concluidas.grid(row=8, column=1, sticky="w")

lista_ordens.grid(row=10, columnspan=2)

# Instanciando o gerenciador
gerenciador = GerenciadorOrdensServico()

# Carregar ordens de serviço do arquivo CSV
gerenciador.ordens_servico = carregar_ordens_servico("ordens_servico.csv")


listar_ordens_pendentes()
# Rodando a aplicação
root.mainloop() 
