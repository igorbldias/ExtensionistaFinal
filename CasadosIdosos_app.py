import tkinter as tk
from tkinter import messagebox
import sqlite3
import os

# Apaga banco existente para recriar do zero (opcional)
if os.path.exists('idosos.db'):
    os.remove('idosos.db')

# Cria novo banco com a coluna "atividades"
conn = sqlite3.connect('idosos.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    idade INTEGER,
    altura REAL,
    peso REAL,
    agua REAL,
    atividades INTEGER
)
''')
conn.commit()

def salvar_dados():
    nome = entry_nome.get().strip()
    idade = entry_idade.get().strip()
    altura = entry_altura.get().strip()
    peso = entry_peso.get().strip()
    agua = entry_agua.get().strip()
    atividades = entry_atividades.get().strip()

    if not nome or not idade or not altura or not peso or not agua or not atividades:
        messagebox.showwarning("Erro", "Por favor, preencha todos os campos")
        return
    
    try:
        idade_i = int(idade)
        altura_f = float(altura)
        peso_f = float(peso)
        agua_f = float(agua)  # Agora em litros
        atividades_i = int(atividades)
    except ValueError:
        messagebox.showerror("Erro", "Idade, Altura, Peso, Água e Atividades devem ser números válidos")
        return

    cursor.execute('INSERT INTO usuarios (nome, idade, altura, peso, agua, atividades) VALUES (?, ?, ?, ?, ?, ?)',
                   (nome, idade_i, altura_f, peso_f, agua_f, atividades_i))
    conn.commit()

    msg = ""
    if atividades_i >= 5 and agua_f >= 4:
        msg = "APITO VERDE - Metas atingidas!"
        cor_msg = "green"
    else:
        msg = "NÃO APITO - Metas não atingidas: "
        cor_msg = "red"
        campos_faltando = []
        if atividades_i < 5:
            campos_faltando.append("Quantidade de Atividades")
        if agua_f < 4:
            campos_faltando.append("Consumo de Água")
        msg += ", ".join(campos_faltando)
    
    label_status.config(text=msg, fg=cor_msg)

    limpar_campos()
    atualizar_lista()

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_idade.delete(0, tk.END)
    entry_altura.delete(0, tk.END)
    entry_peso.delete(0, tk.END)
    entry_agua.delete(0, tk.END)
    entry_atividades.delete(0, tk.END)

def atualizar_lista():
    lista_usuarios.delete(0, tk.END)
    cursor.execute('SELECT nome, idade, altura, peso, agua, atividades FROM usuarios')
    for row in cursor.fetchall():
        lista_usuarios.insert(tk.END, f"{row[0]} - {row[1]} anos, Altura: {row[2]} cm, Peso: {row[3]} kg, Água: {row[4]} litros, Atividades: {row[5]}")

app = tk.Tk()
app.title("Cadastro e Controle Saúde Idosos")

tk.Label(app, text="Nome").grid(row=0, column=0)
tk.Label(app, text="Idade").grid(row=1, column=0)
tk.Label(app, text="Altura (cm)").grid(row=2, column=0)
tk.Label(app, text="Peso (kg)").grid(row=3, column=0)
tk.Label(app, text="Consumo água (litros)").grid(row=4, column=0)
tk.Label(app, text="Quantidade de Atividades").grid(row=5, column=0)

entry_nome = tk.Entry(app)
entry_idade = tk.Entry(app)
entry_altura = tk.Entry(app)
entry_peso = tk.Entry(app)
entry_agua = tk.Entry(app)
entry_atividades = tk.Entry(app)

entry_nome.grid(row=0, column=1)
entry_idade.grid(row=1, column=1)
entry_altura.grid(row=2, column=1)
entry_peso.grid(row=3, column=1)
entry_agua.grid(row=4, column=1)
entry_atividades.grid(row=5, column=1)

btn_salvar = tk.Button(app, text="Salvar", command=salvar_dados)
btn_limpar = tk.Button(app, text="Limpar Campos", command=limpar_campos)
btn_atualizar = tk.Button(app, text="Atualizar Lista", command=atualizar_lista)

btn_salvar.grid(row=6, column=0, pady=5)
btn_limpar.grid(row=6, column=1, pady=5)
btn_atualizar.grid(row=7, column=0, columnspan=2, pady=5)

label_status = tk.Label(app, text="", font=("Arial", 12))
label_status.grid(row=8, column=0, columnspan=2, pady=10)

lista_usuarios = tk.Listbox(app, width=80)
lista_usuarios.grid(row=9, column=0, columnspan=2, pady=10)

atualizar_lista()

app.mainloop()

conn.close()




