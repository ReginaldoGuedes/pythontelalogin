import customtkinter as ctk
from tkinter import  *
import sqlite3
from tkinter import messagebox


class BackEnd():  
        def conecta_db(self):
            self.conn = sqlite3.connect('appCad.db')
            self.cursor = self.conn.cursor()
            print('banco conectado...')
        
        def desconecta_db(self):
            self.conn.close()
            print('banco desconectado X')

        def criar_tabela(self):
            self.conecta_db()
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios(
                Id INTEGER PRYMARY KEY AUTO INCREMENT,
                Username TEXT NOT NULL,
                Email TEXT NOT NULL,
                Senha TEXT NOT NULL,
                Confirmar_Senha TEXT NOT NULL
            )""")
            self.conn.commit()
            print('tabela criada com sucesso...')
            self.desconecta_db()

        def cadastrar_usuario(self):
            self.username_cadastro = self.username_cadastro_entry.get()
            self.email_cadastro = self.email_cadastro_entry.get()
            self.senha_cadastro = self.senha_cadastro_entry.get()
            self.confirmar_senha_cadastro = self.confirmar_senha_cadastro_entry.get()

            self.conecta_db()

            self.cursor.execute("""
                INSERT INTO Usuarios(
                Username, Email, Senha, Confirmar_Senha)
                VALUES (?, ?, ?, ?)""", (self.username_cadastro, self.email_cadastro, self.senha_cadastro, self.confirmar_senha_cadastro))
            
            try:
                if(self.username_cadastro == '' or self.email_cadastro == '' or self.senha_cadastro == '' or self.confirmar_senha_cadastro == ''):
                     messagebox(title= 'Sitema de Login', message = 'ERRO! Preencha todos os campos!')

                elif(len(self.username_cadastro) < 4):
                     messagebox.showwarning(title='Sistema de Login', message = 'Sua senha deve conter no mínimo 4 caracteres.')

                elif(len(self.senha_cadastro) < 4):
                     messagebox.showwarning(title='Sistema de Login', message = 'Sua senha deve conter no mínimo 4 digitos.')

                elif(self.senha_cadastro != self.confirmar_senha_cadastro):
                     messagebox.showerror(title='Sistema de Login', message='ERRO! As senhas dever ser iguais')

                else:
                     self.conn.commit()
                     messagebox.showinfo(title='Sistema de Login', message=f'Parabéns, {self.username_cadastro}\n Seja bem-vindo(a)')
                     self.desconecta_db()
                     self.limpa_entry_cadastro()
                     
            except:
                """messagebox.showinfo(title='Sistema de Login', message='Erro ao preencher seu cadastro\nTente novamente.')
                self.desconecta_db()
                self.limpa_entry_login()"""
                pass
                

        def verifica_login(self):
             self.username_login = self.username_login_entry.get()
             self.senha_login = self.senha_login_entry.get()
             self.limpa_entry_login()

             self.conecta_db()

             self.cursor.execute("""
             SELECT * FROM Usuarios WHERE (Username = ? AND Senha = ?)""", 
             (self.username_login, self.senha_login))

#-------este comando faz a leitura e verificação na tabela usuarios 
             self.verificar_dados = self.cursor.fetchone()

             try:
                  if(self.username_cadastro == '' or self.email_cadastro == '' or self.senha_cadastro == '' or self.confirmar_senha_cadastro == ''):
                     messagebox(title= 'Sitema de Login', message = 'ERRO! Preencha todos os campos!')

                  elif(self.username_login in self.verificar_dados and self.senha_login in self.verificar_dados):
                       messagebox.showinfo(title='Sistema de Login', message=f'Parabéns, {self.username_login}\nAcesso Liberado!')
                       self.desconecta_db()
                       self.limpa_entry_login()
             except:
                  messagebox.showerror(title='Sistema de Login', message='ERRO!\n Usuário ou Senha Incorretos.')
                  self.desconecta_db()


             

#-------este comando limpa os dados na tela 
        def limpa_entry_cadastro(self):
                self.username_cadastro_entry.delete(0, END)
                self.email_cadastro_entry.delete(0, END)
                self.senha_cadastro_entry.delete(0, END)
                self.confirmar_senha_entry.delete(0, END)

        def limpa_entry_login(self):
                self.username_login_entry.delete(0, END)
                self.senha_login_entry.delete(0, END)

#-------Criando Classe da Aplicacao inicial do app 
class App(ctk.CTk, BackEnd):
    def __init__(self):
        super().__init__()
        self.configuracoes_da_janela()
        self.tela_login()
        self.criar_tabela()
#-------criando a Janela do Sistema  
    def configuracoes_da_janela(self):
        self.geometry('700x400')
        self.title('Sistema de Acesso')
        self.resizable(False,False)

#-------criando Tela de Login e Logotipo
    def tela_login(self):
        self.img = PhotoImage(file='logo.png')
        self.lb_img = ctk.CTkLabel(self, text=None, image=self.img)
        self.lb_img.grid(row=1, column=0, padx=30)

#-------criando Titulo interno da tela
        self.title = ctk.CTkLabel(self, text='Faça seu login ou cadastre-se \nem nossa plataforma.', font=("Roboto bold", 14))
        self.title.grid(row=0, column=0, pady=20)

#-------criando Titulo externo cabeçalho
        self.frame_login = ctk.CTkFrame(self, width=350, height=380)
        self.frame_login.place(x=350, y=10)

#-------criando widgets mensagem no formulário
        self.lb_title = ctk.CTkLabel(self.frame_login, text='Faça seu Login', font=("Roboto bold", 22))
        self.lb_title.grid(row=0, column=0, padx=10, pady=10)

#-------criando entrada de login e senha
        self.username_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Usuário", font=("Roboto bold", 14), corner_radius=15, border_color='#1866a5')
        self.username_login_entry.grid(row=1, column=0, padx=10, pady=10)

        self.senha_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Senha", font=("Roboto bold", 14), corner_radius=15, show='*', border_color='#1866a5')
        self.senha_login_entry.grid(row=2, column=0, padx=5, pady=10)

#-------criando checkbox
        self.ver_senha = ctk.CTkCheckBox(self.frame_login, text="Clique para ver a Senha", font=("Roboto bold", 12), corner_radius=10)
        self.ver_senha.grid(row=3, column=0, padx=10, pady=10)

#-------criando botão Login
        self.btn_login = ctk.CTkButton(self.frame_login, width=300, text="Login".upper(), font=("Roboto bold", 14), corner_radius=15, command=self.verifica_login)
        self.btn_login.grid(row=4, column=0, padx=10, pady=10)

#-------criando widgets mensagem no formulário
        self.span = ctk.CTkLabel(self.frame_login, text="Criar Uma Conta Agora".upper(), font=("Century Gothic bold", 10), corner_radius=15)
        self.span.grid(row=5, column=0, padx=10, pady=10)

#-------criando botão cadastrar e chamando tela de cadastro
        self.btn_cadastro = ctk.CTkButton(self.frame_login, width=300, fg_color='green', hover_color='#050',text="Cadastrar".upper(), font=("Roboto bold", 14), corner_radius=15, command=self.tela_de_cadastro)
        self.btn_cadastro.grid(row=6, column=0, padx=10, pady=10)

#-------criando tela de cadastro---------------

    def tela_de_cadastro(self):
#-------Sobrepondo tela de login
        self.frame_login.place_forget()

#-------criando Titulo externo cabeçalho
        self.frame_cadastro = ctk.CTkFrame(self, width=350, height=380)
        self.frame_cadastro.place(x=350, y=10)

#-------criando Titulo ixterno cabeçalho
        self.lb_title = ctk.CTkLabel(self.frame_cadastro, text='Cadastre-se', font=("Roboto bold", 22))
        self.lb_title.grid(row=0, column=0, padx=10 ,pady=5)

#-------criando entrada de cadastro
        self.username_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Usuário", font=("Roboto bold", 14), corner_radius=15, border_color='#1866a5')
        self.username_cadastro_entry.grid(row=1, column=0, padx=10, pady=5)

        self.email_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="E-mail", font=("Roboto bold", 14), corner_radius=15, border_color='#1866a5')
        self.email_cadastro_entry.grid(row=2, column=0, padx=10, pady=5)

        self.senha_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Senha", font=("Roboto bold", 14), corner_radius=15, show='*', border_color='#1866a5')
        self.senha_cadastro_entry.grid(row=3, column=0, padx=10, pady=5)

        self.confirmar_senha_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Confirmar Senha", font=("Roboto bold", 14), corner_radius=15, show='*', border_color='#1866a5')
        self.confirmar_senha_cadastro_entry.grid(row=4, column=0, padx=10, pady=5)

#-------criando checkbox
        self.ver_senha = ctk.CTkCheckBox(self.frame_cadastro, text="Clique para ver a Senha", font=("Roboto bold", 12), corner_radius=10)
        self.ver_senha.grid(row=5, column=0, pady=5)

#-------criando botão cadastrar
        self.btn_cadastrar_user = ctk.CTkButton(self.frame_cadastro, width=300, fg_color='green', hover_color='#050',text="Cadastrar".upper(), font=("Roboto bold", 14), corner_radius=15, command=self.cadastrar_usuario)
        self.btn_cadastrar_user.grid(row=6, column=0, padx=10, pady=5)

#-------criando botão voltar a tela principal
        self.btn_back = ctk.CTkButton(self.frame_cadastro, width=300, text="Voltar ao Login".upper(), font=("Roboto bold", 10), corner_radius=15, fg_color='#444', hover_color='#333', command=self.tela_login)
        self.btn_back.grid(row=7, column=0, padx=10, pady=10)     

if __name__ == '__main__':
    app = App()
    app.mainloop()
