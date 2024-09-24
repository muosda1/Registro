import tkinter as tk
import datetime
from tkinter import messagebox
from tkcalendar import DateEntry
from validate_docbr import CPF
from backend import ChurchDatabase
import visualizar_db

class ChurchApp:
    def __init__(self, main_window, member_id=None):
        self.root = main_window
        self.root.title("Registrar Novo Membro" if not member_id else "Editar Membro")
        self.member_id = member_id

        width = 1020
        height = 350

        self.root.geometry(f"{width}x{height}")
        self.root.resizable(True, True)
        self.center_window(width, height)

        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        self.vcmd_cpf = (self.root.register(self.validate_cpf_input), '%P')

        self.labels = ["Full Name", "CPF", "Birth Date", "Sexo", "Street", "Number", "Neighborhood", "City", "State",
                       "Country", "CEP", "Phone", "Email", "Marital Status", "Entry Form", "Children Var", "Children Entry",
                       "Profession", "Entry Date"]

        self.entries = {}
        self.error_labels = {}
        dados_membro ={}

        # Primeira seção - Dados Obrigatórios

        tk.Label(self.root, text="Nome Completo").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.full_name_entry = tk.Entry(self.root, width=30)
        self.full_name_entry.grid(row=0, column=2, padx=10, pady=5, sticky="w")

        self.root.grid_columnconfigure(1, minsize=2)
        self.root.grid_columnconfigure(3, minsize=2)

        tk.Label(self.root, text="CPF").grid(row=0, column=4, padx=10, pady=5, sticky="w")
        self.cpf_entry = tk.Entry(self.root, validate="key", validatecommand=self.vcmd_cpf, width=15)
        self.cpf_entry.bind("<FocusOut>", self.check_cpf)
        self.cpf_entry.grid(row=0, column=6, padx=(0,0), pady=5, sticky="w")

        self.root.grid_columnconfigure(5, minsize=1)
        self.root.grid_columnconfigure(7, minsize=1)

        self.error_labels["CPF"] = tk.Label(self.root, text="", fg="red")
        self.error_labels["CPF"].grid(row=1, column=6, padx=0, pady=0, sticky="nw")

        tk.Label(self.root, text="Data de Nascimento").grid(row=0, column=8, padx=(0, 5), pady=5, sticky="w")
        today = datetime.date.today()
        self.birth_date_entry = DateEntry(self.root, date_pattern="dd-mm-yyyy", width=12, maxdate=today)
        self.birth_date_entry.grid(row=0, column=10, padx=(0, 0), pady=5, sticky="w")
        self.birth_date_entry.bind("<FocusOut>", self.format_date_entry)
        self.birth_date_entry.bind("<Return>", self.format_date_entry)
        self.birth_date_entry.delete(0, "end")

        if self.member_id and 'Birth Date' in dados_membro:
            self.birth_date_entry.set_date(dados_membro['Birth Date'])

        self.root.grid_columnconfigure(9, minsize=1)
        self.root.grid_columnconfigure(11, minsize=1)

        tk.Label(self.root, text="Sexo").grid(row=0, column=12, padx=(0, 0), pady=5, sticky="w")
        self.sex_var = tk.StringVar(value="Selecione")
        self.sex_entry = tk.OptionMenu(self.root, self.sex_var, "Masculino", "Feminino")
        self.sex_entry.grid(row=0, column=13, padx=(0, 0), pady=5, sticky="w")

        if self.member_id and 'Sex' in dados_membro:
            self.sex_var.set(dados_membro['Sex'])

        self.root.grid_columnconfigure(13, weight=0, minsize=0)

        # Linha cinza para separar as seções
        canvas = tk.Canvas(self.root, height=2, bg="#AAAAAA", bd=0, highlightthickness=0)
        canvas.grid(row=2, column=0, columnspan=15, sticky="ew", pady=10)

        # Segunda seção - Dados Necessários (não obrigatórios)
        tk.Label(self.root, text="Rua").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.street_entry = tk.Entry(self.root, width=20)
        self.street_entry.grid(row=3, column=2, padx=10, pady=5, sticky="w")

        self.root.grid_columnconfigure(1, minsize=2)
        self.root.grid_columnconfigure(3, minsize=2)

        tk.Label(self.root, text="Número").grid(row=3, column=4, padx=10, pady=5, sticky="w")
        self.number_entry = tk.Entry(self.root, width=10)
        self.number_entry.grid(row=3, column=6, padx=0, pady=5, sticky="w")

        self.root.grid_columnconfigure(5, minsize=2)
        self.root.grid_columnconfigure(7, minsize=2)

        tk.Label(self.root, text="Bairro").grid(row=3, column=8, padx=0, pady=5, sticky="w")
        self.neighborhood_entry = tk.Entry(self.root, width=15)
        self.neighborhood_entry.grid(row=3, column=10, padx=0, pady=5, sticky="w")

        self.root.grid_columnconfigure(9, minsize=2)
        self.root.grid_columnconfigure(11, minsize=2)

        tk.Label(self.root, text="Cidade").grid(row=3, column=12, padx=0, pady=5, sticky="w")
        self.city_entry = tk.Entry(self.root, width=15)
        self.city_entry.grid(row=3, column=13, padx=0, pady=5, sticky="w")

        self.root.grid_columnconfigure(13, minsize=2)

        tk.Label(self.root, text="Estado").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.state_entry = tk.Entry(self.root, width=10)
        self.state_entry.grid(row=4, column=2, padx=10, pady=5, sticky="w")

        self.root.grid_columnconfigure(1, minsize=2)
        self.root.grid_columnconfigure(3, minsize=2)

        tk.Label(self.root, text="País").grid(row=4, column=4, padx=10, pady=5, sticky="w")
        self.country_entry = tk.Entry(self.root, width=15)
        self.country_entry.grid(row=4, column=6, padx=0, pady=5, sticky="w")

        self.root.grid_columnconfigure(5, minsize=2)
        self.root.grid_columnconfigure(7, minsize=2)

        tk.Label(self.root, text="CEP").grid(row=4, column=8, padx=0, pady=5, sticky="w")
        self.cep_entry = tk.Entry(self.root, width=10)
        self.cep_entry.grid(row=4, column=10, padx=0, pady=5, sticky="w")

        self.root.grid_columnconfigure(9, minsize=2)
        self.root.grid_columnconfigure(11, minsize=2)

        tk.Label(self.root, text="Telefone").grid(row=4, column=12, padx=1, pady=5, sticky="w")
        self.phone_entry = tk.Entry(self.root, width=15)
        self.phone_entry.grid(row=4, column=13, padx=0, pady=5, sticky="w")

        self.root.grid_columnconfigure(13, minsize=2)

        tk.Label(self.root, text="Email").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.email_entry = tk.Entry(self.root, width=25)
        self.email_entry.grid(row=5, column=2, padx=10, pady=5, sticky="w")

        self.root.grid_columnconfigure(1, minsize=2)

        # Linha cinza para separar as seções
        canvas = tk.Canvas(self.root, height=2, bg="#AAAAAA", bd=0, highlightthickness=0)
        canvas.grid(row=6, column=0, columnspan=15, sticky="ew", pady=10)

        # Terceira seção - Dados Pessoais
        tk.Label(self.root, text="Estado Civil").grid(row=7, column=0, padx=10, pady=5, sticky='w')
        marital_status_options = ["Solteiro(a)", "Casado(a)", "Separado(a)", "Divorciado(a)", "Viúvo(a)"]
        self.marital_status_var = tk.StringVar(value="Selecione")
        self.marital_status_entry = tk.OptionMenu(self.root, self.marital_status_var, *marital_status_options)
        self.marital_status_entry.grid(row=7, column=2, padx=10, pady=5, sticky='w')

        if self.member_id and 'Marital Status' in dados_membro:
            self.marital_status_var.set(dados_membro['Marital Status'])

        self.root.grid_columnconfigure(1, minsize=2)
        self.root.grid_columnconfigure(3, minsize=2)

        tk.Label(self.root, text="Filhos").grid(row=7, column=4, padx=10, pady=5, sticky='w')

        # Variável para controle "Sim" ou "Não" sobre filhos
        self.children_var = tk.StringVar(value="Não")
        filhos_frame = tk.Frame(self.root)
        filhos_frame.grid(row=7, column=5, columnspan=3, sticky='w')

        # Botão de rádio para "Não"
        children_no = tk.Radiobutton(filhos_frame, text="Não", variable=self.children_var, value="no",
                                     command=self.toggle_children_entry)
        children_no.pack(side='left')

        # Botão de rádio para "Sim"
        children_yes = tk.Radiobutton(filhos_frame, text="Sim", variable=self.children_var, value="yes",
                                      command=self.toggle_children_entry)
        children_yes.pack(side='left', padx=(10, 0))

        # Entrada para a quantidade de filhos, que será mostrada somente quando "Sim" for selecionado
        self.children_entry = tk.Entry(filhos_frame, width=2)
        self.children_entry.pack(side='left', padx=(10, 0))
        self.children_entry.pack_forget()  # Esconder inicialmente

        # Preencher dados do membro existente, se disponível
        if self.member_id and 'Children' in dados_membro:
            if dados_membro['Children'] == "Sim":
                self.children_var.set("yes")  # Marca o botão de rádio para "Sim"
                self.children_entry.pack(side='left', padx=(10, 0))  # Mostra o campo de quantidade de filhos
                self.children_entry.delete(0, tk.END)
                self.children_entry.insert(0, dados_membro.get('Children Entry', ''))  # Preenche a quantidade de filhos
            else:
                self.children_var.set("no")  # Marca o botão de rádio para "Não"
                self.children_entry.pack_forget()  # Esconde o campo de quantidade de filhos

        tk.Label(self.root, text="Profissão").grid(row=7, column=8, padx=0, pady=5, sticky='w')
        self.profession_entry = tk.Entry(self.root, width=20)
        self.profession_entry.grid(row=7, column=10, padx=0, pady=5, sticky='w')

        self.root.grid_columnconfigure(9, minsize=2)
        self.root.grid_columnconfigure(11, minsize=2)

        tk.Label(self.root, text="Forma de Entrada").grid(row=7, column=12, padx=0, pady=5, sticky='w')
        self.entry_form_var = tk.StringVar(value="Selecione")
        self.entry_form_entry = tk.OptionMenu(self.root, self.entry_form_var, "Batismo", "Aclamação", "Carta")
        self.entry_form_entry.grid(row=7, column=13, padx=0, pady=5, sticky='w')

        if self.member_id and 'Entry Form' in dados_membro:
            self.entry_form_var.set(dados_membro['Entry Form'])

        self.root.grid_columnconfigure(13, minsize=2)

        tk.Label(self.root, text="Data de Entrada").grid(row=8, column=0, padx=10, pady=5, sticky='w')
        today = datetime.date.today()
        self.entry_date_entry = DateEntry(self.root, date_pattern="dd-mm-yyyy", width=12, maxdate=today)
        self.entry_date_entry.grid(row=8, column=2, padx=10, pady=5, sticky='w')
        self.entry_date_entry.bind("<FocusOut>", self.format_entry_date)
        self.entry_date_entry.bind("<Return>", self.format_entry_date)
        self.entry_date_entry.delete(0, "end")

        if self.member_id and 'Entry Date' in dados_membro:
            self.entry_date_entry.set_date(dados_membro['Entry Date'])  # Usa o formato adequado da biblioteca

        self.root.grid_columnconfigure(1, minsize=2)

        canvas = tk.Canvas(self.root, height=2, bg="#AAAAAA", bd=0, highlightthickness=0)
        canvas.grid(row=9, column=0, columnspan=15, sticky="ew", pady=10)

        # Botão de "Salvar"
        save_button = tk.Button(self.root, text="Salvar", command=self.save_member)
        save_button.grid(row=10, column=4, columnspan=1, padx=10, pady=10, sticky='w')

        # Botão de "Visualizar DB"
        view_db_button = tk.Button(self.root, text="Visualizar Banco de Dados", command=self.iniciar_visualizacao_db)
        view_db_button.grid(row=10, column=6, columnspan=1, padx=10, pady=10, sticky='w')

        # Botão de "Sair"
        exit_button = tk.Button(self.root, text="Sair", command=self.exit_app)
        exit_button.grid(row=10, column=8, columnspan=1, padx=10, pady=10, sticky='w')

        self.entries = {
            'Full Name': self.full_name_entry,
            'CPF': self.cpf_entry,
            'Birth Date': self.birth_date_entry,
            'Sex': self.sex_entry,
            'Street': self.street_entry,
            'Number': self.number_entry,
            'Neighborhood': self.neighborhood_entry,
            'City': self.city_entry,
            'State': self.state_entry,
            'Country': self.country_entry,
            'CEP': self.cep_entry,
            'Phone': self.phone_entry,
            'Email': self.email_entry,
            'Marital Status': self.marital_status_entry,
            'Entry Form': self.entry_form_entry,
            'Children Var': self.children_var,
            'Children Entry': self.children_entry,
            'Profession': self.profession_entry,
            'Entry Date': self.entry_date_entry
        }

        if self.member_id:
            self.carregar_dados_membro()

    def carregar_dados_membro(self):
        db = ChurchDatabase(main_window=self.root)
        info = db.fetch_member_info_by_id(self.member_id)

        if info:
            dados_membro = {
                'Full Name': info[1],
                'CPF': info[2],
                'Birth Date': info[3],
                'Sex': info[4],
                'Street': info[5],
                'Number': info[6],
                'Neighborhood': info[7],
                'City': info[8],
                'State': info[9],
                'Country': info[10],
                'CEP': info[11],
                'Phone': info[12],
                'Email': info[13],
                'Marital Status': info[14],
                'Children Var': info[15],
                'Children Entry': info[16],
                'Profession': info[17],
                'Entry Form': info[18],
                'Entry Date': info[19]
            }

            for campo, valor in dados_membro.items():
                if campo in self.entries:
                    entry = self.entries[campo]

                    if isinstance(entry, tk.Entry):
                        entry.delete(0, tk.END)
                        entry.insert(0, valor)


            self.sex_var.set(dados_membro['Sex'])
            self.marital_status_var.set(dados_membro['Marital Status'])
            self.entry_form_var.set(dados_membro['Entry Form'])

            if dados_membro['Children Var'] == "yes":
                self.children_var.set("yes")
                self.children_entry.delete(0, tk.END)
                self.children_entry.insert(0, dados_membro['Children Entry'])
            elif dados_membro['Children Var'] == "desconhecido" or not dados_membro['Children Var']:
                self.children_var.set("desconhecido")
                self.children_entry.delete(0, tk.END)
            else:
                self.children_var.set("no")
                self.children_entry.delete(0, tk.END)

            if dados_membro['Birth Date']:
                self.birth_date_entry.set_date(dados_membro['Birth Date'])
            if dados_membro['Entry Date']:
                self.entry_date_entry.set_date(dados_membro['Entry Date'])

        else:
            messagebox.showerror("Erro", "Não foi possível carregar os dados do membro.")

        db.close()

    def validate_cpf_input(self, cpf):
        if len(cpf) == 0:
            self.entries["CPF"].config(highlightthickness=0)
            self.error_labels["CPF"].config(text="")
            return True

        if not cpf.isdigit() or len(cpf) > 11:
            return False

        return True

    def validate_cpf(self, cpf):
        cpf_validator = CPF()
        return cpf_validator.validate(cpf)

    def check_cpf(self, event):
        cpf = self.entries["CPF"].get().replace(".", "").replace("-", "")  # Remove pontos e traços

        # Se o campo CPF estiver vazio
        if len(cpf) == 0:
            self.error_labels["CPF"].config(text="")
            self.entries["CPF"].config(highlightthickness=0)
            return

        # Verifica se o CPF tem 11 dígitos e se é válido
        elif len(cpf) != 11 or not self.validate_cpf(cpf):
            self.entries["CPF"].config(highlightbackground="red", highlightcolor="red", highlightthickness=2)
            self.error_labels["CPF"].config(text="CPF inválido.")
        else:
            self.entries["CPF"].config(highlightthickness=0)
            self.error_labels["CPF"].config(text="")

    def format_date_entry(self, event):
        date_input = self.birth_date_entry.get().replace("-", "").strip()
        if len(date_input) == 8:
            formatted_date = f"{date_input[:2]}-{date_input[2:4]}-{date_input[4:]}"
            self.birth_date_entry.delete(0, "end")
            self.birth_date_entry.insert(0, formatted_date)
        else:
            print("Data inválida ou incompleta")

    def format_entry_date(self, event):
        date_input = self.entry_date_entry.get().replace("-", "").strip()
        if len(date_input) == 8:
            formatted_date = f"{date_input[:2]}-{date_input[2:4]}-{date_input[4:]}"
            self.entry_date_entry.delete(0, "end")
            self.entry_date_entry.insert(0, formatted_date)
        else:
            print("Data inválida ou incompleta")

    def toggle_children_entry(self):
        if self.children_var.get() == "yes":
            self.children_entry.pack(side='left', padx=(10, 0))
        else:
            self.children_entry.pack_forget()
            self.children_entry.delete(0, tk.END)

    def save_member(self):
        full_name = self.entries["Full Name"].get().upper()
        cpf = self.entries["CPF"].get()
        birth_date = self.entries["Birth Date"].get()
        sex = self.sex_var.get()
        street = self.entries["Street"].get()
        number = self.entries["Number"].get()
        neighborhood = self.entries["Neighborhood"].get()
        city = self.entries["City"].get()
        state = self.entries["State"].get()
        country = self.entries["Country"].get()
        cep = self.entries["CEP"].get()
        phone = self.entries["Phone"].get()
        email = self.entries["Email"].get()
        marital_status = self.marital_status_var.get()
        entry_form = self.entry_form_var.get()
        children_var = self.children_var.get()
        if not children_var:
            children_var = "desconhecido"
            children_entry = ""
        elif children_var == 'yes':
            children_entry = self.children_entry.get()
        else:
            children_var = "Não"
            children_entry = ""
        profession = self.entries["Profession"].get()
        entry_date = self.entries["Entry Date"].get()

        if not full_name or not cpf or not birth_date or sex == "Selecione":
            messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")
            return

        if not self.validate_cpf(cpf):
            messagebox.showerror("Erro", "Por favor, verifique o CPF e tente novamente.")
            return

        db = ChurchDatabase(main_window=self.root)

        try:
            if self.member_id:
                # Atualizar membro existente
                db.update_member(self.member_id, full_name, cpf, birth_date, sex, street, number, neighborhood, city,
                                 state, country, cep, phone, email, marital_status, children_var, children_entry,
                                 profession,
                                 entry_form, entry_date)
                messagebox.showinfo("Sucesso", "Membro atualizado com sucesso.")

                self.member_id = None
                self.root.title("Registrar Novo Membro")

            else:
                # Salvar novo membro
                db.save_member(full_name, cpf, birth_date, sex, street, number, neighborhood, city, state, country, cep,
                               phone, email, marital_status, children_var, children_entry, profession, entry_form,
                               entry_date)
                messagebox.showinfo("Sucesso", "Membro salvo com sucesso.")

            self.clear_entries()

        except ValueError as e:
            messagebox.showerror("Erro", str(e))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar o membro: {e}")
        finally:
            db.close()

    def clear_entries(self):
        for entry in self.entries.values():
            if isinstance(entry, tk.Entry):
                entry.delete(0, tk.END)
            elif isinstance(entry, DateEntry):
                entry.delete(0, tk.END)
            elif isinstance(entry, tk.OptionMenu):
                entry.setvar(entry.cget("textvariable"), "Selecione")

        self.children_var.set("desconhecido")
        self.children_entry.pack_forget()
        self.children_entry.delete(0, tk.END)
        self.sex_var.set("Selecione")
        self.marital_status_var.set("Selecione")
        self.entry_form_var.set("Selecione")
        self.entries["Birth Date"].delete(0, tk.END)
        self.entries["Entry Date"].delete(0, tk.END)

    def iniciar_visualizacao_db(self):
        self.root.withdraw()
        visualizar_db.iniciar_visualizacao_db()

    def exit_app(self):
        if messagebox.askyesno("Sair", "Deseja fechar o aplicativo?"):
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChurchApp(root)
    root.mainloop()

# Feito Por Murilo Abreu