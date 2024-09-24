import tkinter as tk
from tkinter import messagebox
from backend import ChurchDatabase
import frontend

def mostrar_informacoes(nome, painel_info, root):
    for widget in painel_info.winfo_children():
        widget.destroy()

    db = ChurchDatabase(main_window=root)
    info = db.fetch_member_info(nome)

    if info:

        def safe_info(value):
            return value if value and value != "Selecione" else "Desconhecido"

        children_var = info[15].lower() if info[15] else "desconhecido"  # Normalizando e tratando vazio

        if children_var == "desconhecido":
            children_display = "Desconhecido"
        elif children_var == "yes":
            children_display = f"Sim, {info[16]}" if info[16] else "Sim"
        else:
            children_display = "Não"

        info_text = f"Nome: {safe_info(info[1])}\nCPF: {safe_info(info[2])}\nData de Nascimento: {safe_info(info[3])}\nSexo: {safe_info(info[4])}\n" \
                    f"Rua: {safe_info(info[5])}\nNúmero: {safe_info(info[6])}\nBairro: {safe_info(info[7])}\n" \
                    f"Cidade: {safe_info(info[8])}\nEstado: {safe_info(info[9])}\nPaís: {safe_info(info[10])}\n" \
                    f"CEP: {safe_info(info[11])}\nTelefone: {safe_info(info[12])}\nEmail: {safe_info(info[13])}\n" \
                    f"Estado Civil: {safe_info(info[14])}\n" \
                    f"Filhos: {('Sim, ' + str(safe_info(info[16]))) if info[15] == 'yes' else 'Não'}\n" \
                    f"Profissão: {safe_info(info[17])}\n" \
                    f"Forma de Entrada: {safe_info(info[18])}\n" \
                    f"Data de Entrada: {safe_info(info[19])}"

        info_label = tk.Label(painel_info, text=info_text, anchor='nw', justify='left', font=("Arial", 12))
        info_label.pack(fill='both', expand=True, padx=10, pady=10)

        # Botões de remover e editar
        btn_remover = tk.Button(painel_info, text="Remover Membro", command=lambda: remover_membro(info[0], root))
        btn_remover.pack(side="left", padx=10, pady=10)

        btn_editar = tk.Button(painel_info, text="Editar Informações", command=lambda: editar_membro(info[0], root))
        btn_editar.pack(side="left", padx=10, pady=10)
    else:
        info_text = "Informações não disponíveis"

def remover_membro(member_id, root):
    if messagebox.askyesno("Confirmação", "Tem certeza que deseja remover este membro?"):
        db = ChurchDatabase(main_window=root)
        db.cur.execute("DELETE FROM members WHERE id = ?", (member_id,))
        db.conn.commit()
        db.close()
        messagebox.showinfo("Sucesso", "Membro removido com sucesso!")
        root.destroy()
        iniciar_visualizacao_db()

def editar_membro(member_id, root):
    root.withdraw()
    nova_janela = tk.Toplevel(root)
    frontend.ChurchApp(nova_janela, member_id)

def adicionar_membro(janela_atual):
    janela_atual.withdraw()
    nova_janela = tk.Toplevel()
    frontend.ChurchApp(nova_janela)

def sair_aplicativo(janela_atual):
    if messagebox.askyesno("Confirmação", "Deseja fechar o aplicativo?"):
        janela_atual.quit()
        janela_atual.destroy()

def buscar_membros(event, lista_membros, nomes_originais, entry_busca):
    query = entry_busca.get().lower()
    lista_membros.delete(0, tk.END)

    for nome in nomes_originais:
        if query in nome[0].lower():
            lista_membros.insert(tk.END, nome[0].upper())

def iniciar_visualizacao_db():
    root = tk.Toplevel()
    root.title("Visualizar Banco de Dados")

    root.protocol("WM_DELETE_WINDOW", lambda: sair_aplicativo(root))

    # Definindo o tamanho da janela
    largura_janela = 1200
    altura_janela = 600

    # Centralizando a janela
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    posicao_x = (largura_tela // 2) - (largura_janela // 2)
    posicao_y = (altura_tela // 3) - (altura_janela // 3)
    root.geometry(f"{largura_janela}x{altura_janela}+{posicao_x}+{posicao_y}")

    db = ChurchDatabase(main_window=root)
    nomes_membros = sorted(db.fetch_all_members(), key=lambda x: x[0].upper())
    db.close()

    frame_botoes = tk.Frame(root)
    frame_botoes.pack(side="top", anchor="ne", padx=10, pady=10)

    btn_adicionar = tk.Button(frame_botoes, text="Adicionar Membro", command=lambda: adicionar_membro(root))
    btn_adicionar.pack(side="left", padx=5)

    btn_sair = tk.Button(frame_botoes, text="Sair", command=lambda: sair_aplicativo(root))
    btn_sair.pack(side="left", padx=5)

    frame_lista = tk.Frame(root)
    frame_lista.pack(side="left", fill="y", padx=10, pady=10)

    # Campo de busca
    entry_busca = tk.Entry(frame_lista)
    entry_busca.pack(fill="x", padx=5, pady=5)

    lista_membros = tk.Listbox(frame_lista, height=20, width=40)
    lista_membros.pack(fill="y", expand=True)

    for nome in nomes_membros:
        lista_membros.insert(tk.END, nome[0].upper())

    painel_info = tk.Frame(root, bg="white")
    painel_info.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    lista_membros.bind("<<ListboxSelect>>", lambda event: selecionar_membro(event, lista_membros, painel_info, root))

    # Função de busca
    entry_busca.bind("<KeyRelease>", lambda event: buscar_membros(event, lista_membros, nomes_membros, entry_busca))

    def ativar_busca(event):
        entry_busca.focus_set()

    root.bind("<Control-f>", ativar_busca)

def selecionar_membro(event, lista_membros, painel_info, root):
    try:
        nome_selecionado = lista_membros.get(lista_membros.curselection())
        mostrar_informacoes(nome_selecionado, painel_info, root)
    except tk.TclError:
        pass

# Feito Por Murilo Abreu