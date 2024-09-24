import tkinter as tk
from tkinter import messagebox
import visualizar_db
from frontend import ChurchApp

def validar_login():
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    if usuario == "admin" and senha == "senha123":
        abrir_segunda_tela()
    else:
        messagebox.showerror("Erro", "Usuário ou senha inválidos!")

def abrir_segunda_tela():
    root.withdraw()

    segunda_tela = tk.Toplevel(root)
    segunda_tela.title("Escolha uma Opção")
    center_window(segunda_tela, window_width, window_height, y_adjustment)

    label_opcoes = tk.Label(segunda_tela, text="Escolha o que deseja fazer:")
    label_opcoes.pack(pady=10)

    btn_banco_dados = tk.Button(segunda_tela, text="Acessar Banco de Dados", command=lambda: abrir_visualizar_db(segunda_tela))
    btn_banco_dados.pack(pady=5)

    btn_adicionar_membro = tk.Button(segunda_tela, text="Adicionar Novo Membro", command=lambda: abrir_frontend_interface(segunda_tela))
    btn_adicionar_membro.pack(pady=5)

    segunda_tela.protocol("WM_DELETE_WINDOW", lambda: fechar_todas_janelas(segunda_tela))  # Fecha ambas as janelas se a segunda for fechada

def abrir_visualizar_db(segunda_tela):
    segunda_tela.destroy()
    visualizar_db.iniciar_visualizacao_db()
    root.withdraw()

def abrir_frontend_interface(segunda_tela):
    segunda_tela.destroy()
    nova_janela = tk.Toplevel()
    ChurchApp(nova_janela)
    root.withdraw()

def center_window(window, width, height, y_offset=0):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2) + y_offset

    window.geometry(f"{width}x{height}+{x}+{y}")

def fechar_aplicacao():
    root.quit()
    root.destroy()

def fechar_todas_janelas(segunda_tela):
    segunda_tela.destroy()
    fechar_aplicacao()

root = tk.Tk()
root.title("Login e Senha")

window_width = 300
window_height = 180
y_adjustment = -40

center_window(root, window_width, window_height, y_adjustment)

frame_login = tk.Frame(root)
frame_login.pack(pady=20)

label_usuario = tk.Label(frame_login, text="Usuário:")
label_usuario.grid(row=0, column=0, padx=10, pady=5, sticky='e')
entry_usuario = tk.Entry(frame_login)
entry_usuario.grid(row=0, column=1, padx=10, pady=5)

label_senha = tk.Label(frame_login, text="Senha:")
label_senha.grid(row=1, column=0, padx=10, pady=5, sticky='e')
entry_senha = tk.Entry(frame_login, show="*")
entry_senha.grid(row=1, column=1, padx=10, pady=5)

btn_login = tk.Button(root, text="Login", command=validar_login)
btn_login.pack(pady=10)

root.protocol("WM_DELETE_WINDOW", fechar_aplicacao)
root.mainloop()

#Feito Por Murilo Abreu