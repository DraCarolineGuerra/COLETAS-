import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# carregar os dados
try:
    dados = pd.read_csv('BANCO DE DADOS.csv', encoding='latin1')
    dados.columns = dados.columns.str.strip()
    if 'CONTEÚDO' not in dados.columns:
        dados['CONTEÚDO'] = ''
except Exception as e:
    messagebox.showerror("Erro", f"Erro ao carregar o banco de dados:\n{e}")
    dados = pd.DataFrame(columns=['EXAMES', 'CÓDIGO', 'PRAZO', 'TUBO', 'CUIDADOS ESPECIAIS', 'LABORATÓRIO', 'CONTEÚDO'])

# Função busca
def buscar_exame(event=None):
    termo = entry_busca.get().strip().lower()

    if not termo:
        messagebox.showinfo("Aviso", "Por favor, insira um termo para busca.")
        return

    try:
        resultados = dados[dados['EXAMES'].fillna('').str.lower().str.contains(termo) | 
                         dados['CONTEÚDO'].fillna('').str.lower().str.contains(termo)]
        listbox_resultados.delete(0, tk.END)

        if not resultados.empty:
            for _, row in resultados.iterrows():
                listbox_resultados.insert(tk.END, row['EXAMES'])
        else:
            listbox_resultados.insert(tk.END, "Nenhum resultado encontrado.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro na busca:\n{e}")

def limpar_busca():
    entry_busca.delete(0, tk.END)
    listbox_resultados.delete(0, tk.END)
    for widget in frame_detalhes.winfo_children():
        widget.destroy()
    label_placeholder.config(text="Selecione um exame para ver os detalhes", fg="gray")

# detalhes do exame
def mostrar_detalhes(event):
    try:
        selection = listbox_resultados.curselection()
        if not selection:
            return
            
        selecionado = listbox_resultados.get(selection)
        resultado = dados[dados['EXAMES'].fillna('') == selecionado]
        
        for widget in frame_detalhes.winfo_children():
            widget.destroy()
            
        if not resultado.empty:
            row = resultado.iloc[0]
            
            label_titulo = tk.Label(frame_detalhes, text=row['EXAMES'], font=("Helvetica", 14, "bold"), 
                                  bg="#f5f0fa", fg="#4b0082", anchor="w")
            label_titulo.pack(fill="x", pady=(0, 10), padx=10)
            
            def criar_caixa(titulo, valor, icone):
                if pd.notna(valor) and str(valor).strip():
                    frame = tk.Frame(frame_detalhes, 
                                    bg="#f8f5ff",
                                    bd=1, 
                                    relief="groove",
                                    highlightbackground="#d8bfd8",
                                    highlightthickness=2,
                                    padx=10,
                                    pady=5)
                    frame.pack(fill="x", pady=5, padx=5)
                    
                    label_icone = tk.Label(frame, 
                                         text=icone, 
                                         font=("Arial", 12), 
                                         bg="#f8f5ff",
                                         fg="#9370db")
                    label_icone.pack(side="left", padx=(0, 10))
                    
                    frame_texto = tk.Frame(frame, bg="#f8f5ff")
                    frame_texto.pack(side="left", fill="x", expand=True)
                    
                    tk.Label(frame_texto, 
                            text=titulo, 
                            font=("Helvetica", 10, "bold"), 
                            bg="#f8f5ff", 
                            fg="#4B0082",
                            anchor="w").pack(anchor="w")
                    
                    tk.Label(frame_texto, 
                            text=valor, 
                            font=("Helvetica", 10), 
                            bg="#f8f5ff", 
                            fg="#6a5acd",
                            anchor="w", 
                            wraplength=300, 
                            justify="left").pack(anchor="w", fill="x")
            
            criar_caixa("Código:", row['CÓDIGO'], "🔢")
            criar_caixa("Prazo:", row['PRAZO'], "📅")
            criar_caixa("Tubo:", row['TUBO'], "💉")
            criar_caixa("Cuidados Especiais:", row['CUIDADOS ESPECIAIS'], "⚠️")
            criar_caixa("Laboratório:", row['LABORATÓRIO'], "🏥")
            criar_caixa("Conteúdo:", row['CONTEÚDO'], "📝")
            
    except Exception as e:
        print(f"Erro ao mostrar detalhes: {e}")

# Função ajuda
def exibir_ajuda():
    ajuda_msg = "Para problemas no programa, entre em contato:\n\n" \
               "Email: caroline.guerra@veros.vet\n" \
               "Telefone: (11) 98449-8741"
    messagebox.showinfo("Ajuda", ajuda_msg)

root = tk.Tk()
root.title("Coleta+ 🐾")
root.geometry("800x700")
root.configure(bg="#f5f0fa")

root.option_add("*Listbox*Font", ("Helvetica", 11))
root.option_add("*Listbox*Background", "white")
root.option_add("*Listbox*Foreground", "#4B0082")
root.option_add("*Listbox*selectBackground", "#8a2be2")
root.option_add("*Listbox*selectForeground", "white")

# estilo
style = ttk.Style()
style.configure("TButton", 
               font=("Helvetica", 11),
               background="#9370db",
               foreground="#4B0082",
               padding=6)

style.map("TButton",
          background=[("active", "#8a2be2")],
          foreground=[("active", "white")])

style.configure("TEntry", 
               font=("Helvetica", 12),
               fieldbackground="#eee6ff",
               foreground="#4B0082",
               padding=8,
               bordercolor="#9370db",
               lightcolor="#9370db",
               darkcolor="#9370db")

style.map("TEntry",
          fieldbackground=[("focus", "white")])

try:
    logo = Image.open("logo_hospital.png")
    logo = logo.resize((80, 80), Image.LANCZOS)
    logo = ImageTk.PhotoImage(logo)
    logo_label = tk.Label(root, image=logo, bg="#f5f0fa")
    logo_label.image = logo
    logo_label.pack(pady=10)
except Exception as e:
    print(f"Erro ao carregar logo: {e}")
    logo_label = tk.Label(root, text="Coleta+", font=("Helvetica", 20, "bold"), 
                        bg="#f5f0fa", fg="#4b0082")
    logo_label.pack(pady=10)

frame_principal = tk.Frame(root, bg="#f5f0fa")
frame_principal.pack(fill="both", expand=True, padx=20, pady=10)

# busca
frame_busca = tk.Frame(frame_principal, bg="#f5f0fa")
frame_busca.pack(fill="x", pady=10)

def on_entry_focus_in(event):
    event.widget.configure(background="#eee6ff")

def on_entry_focus_out(event):
    event.widget.configure(background="white")

entry_busca = ttk.Entry(frame_busca, font=("Helvetica", 12))
entry_busca.pack(side="left", fill="x", expand=True, padx=(0, 10))
entry_busca.bind("<Return>", buscar_exame)
entry_busca.bind("<FocusIn>", on_entry_focus_in)
entry_busca.bind("<FocusOut>", on_entry_focus_out)

# Botões
btn_buscar = ttk.Button(frame_busca, text="🔍 Buscar", command=buscar_exame)
btn_buscar.pack(side="left", padx=(0, 5))

btn_limpar = ttk.Button(frame_busca, text="🧹 Limpar", command=limpar_busca)
btn_limpar.pack(side="left")

frame_conteudo = tk.Frame(frame_principal, bg="#f5f0fa")
frame_conteudo.pack(fill="both", expand=True)

# resultados
frame_lista = tk.Frame(frame_conteudo, bg="#f5f0fa", width=300)
frame_lista.pack(side="left", fill="y", padx=(0, 10))

scrollbar_lista = tk.Scrollbar(frame_lista)
scrollbar_lista.pack(side="right", fill="y")

listbox_resultados = tk.Listbox(frame_lista, font=("Helvetica", 11), width=40, 
                              yscrollcommand=scrollbar_lista.set, bg="white",
                              selectbackground="#9370db", selectforeground="white")
listbox_resultados.pack(fill="both", expand=True)
scrollbar_lista.config(command=listbox_resultados.yview)
listbox_resultados.bind("<<ListboxSelect>>", mostrar_detalhes)

# detalhes
frame_detalhes_container = tk.Frame(frame_conteudo, bg="#f5f0fa")
frame_detalhes_container.pack(side="right", fill="both", expand=True)

frame_detalhes_borda = tk.Frame(frame_detalhes_container, bg="#e6e6fa", 
                              bd=0, relief="solid", padx=1, pady=1)
frame_detalhes_borda.pack(fill="both", expand=True)

frame_interno = tk.Frame(frame_detalhes_borda, bg="#f5f0fa", padx=10, pady=10)
frame_interno.pack(fill="both", expand=True)

# Barra de rolagem que deu erro mil vezes
canvas = tk.Canvas(frame_interno, bg="#f5f0fa", highlightthickness=0)
scrollbar = ttk.Scrollbar(frame_interno, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#f5f0fa")

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
frame_detalhes = scrollable_frame

label_placeholder = tk.Label(frame_detalhes, text="Selecione um exame para ver os detalhes", 
                           font=("Helvetica", 11), fg="gray", bg="#f5f0fa")
label_placeholder.pack(expand=True, pady=50)

button_ajuda = ttk.Button(root, text="ℹ️ Ajuda", command=exibir_ajuda)
button_ajuda.pack(pady=10)

# Eu querendo biscoito
frame_rodape = tk.Frame(root, bg="#4B0082")
frame_rodape.pack(side="bottom", fill="x", pady=(10, 0))

label_ano = tk.Label(frame_rodape, 
                    text="© 2025 Coleta+ | Desenvolvido por Caroline Guerra 🐾", 
                    font=("Helvetica", 9, "italic"), 
                    fg="white",
                    bg="#4B0082",
                    padx=10,
                    pady=5)
label_ano.pack()

root.update_idletasks()
root.minsize(700, 600)
root.maxsize(1000, 800)

# tooltips
def criar_tooltip(widget, texto):
    tooltip = tk.Toplevel(widget)
    tooltip.withdraw()
    tooltip.wm_overrideredirect(True)
    
    label = tk.Label(tooltip, 
                    text=texto, 
                    bg="#ffffe0", 
                    relief="solid", 
                    borderwidth=1)
    label.pack()
    
    def enter(event):
        x, y, _, _ = widget.bbox("insert")
        x += widget.winfo_rootx() + 25
        y += widget.winfo_rooty() + 25
        tooltip.wm_geometry(f"+{x}+{y}")
        tooltip.deiconify()
    
    def leave(event):
        tooltip.withdraw()
    
    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)

criar_tooltip(btn_buscar, "Buscar exames no banco de dados")
criar_tooltip(btn_limpar, "Limpar busca e resultados")
criar_tooltip(button_ajuda, "Obter ajuda sobre o sistema")

def on_listbox_enter(e):
    listbox_resultados.config(bg="#f5f0fa")

def on_listbox_leave(e):
    listbox_resultados.config(bg="white")

listbox_resultados.bind("<Enter>", on_listbox_enter)
listbox_resultados.bind("<Leave>", on_listbox_leave)

root.mainloop()
