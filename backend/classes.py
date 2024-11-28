"""Módulo com classes inicializadoras dos widgets tkinter"""

#pylint: disable= import-error, unused-argument

import tkinter as tk
from tkinter import ttk
import backend.database as db

class MainPage(tk.Tk):
    """Página inicial da aplicação"""
    def __init__(self, *, title: str, geometry: str):
        super().__init__()
        self.geometry(geometry)
        self.title(title)

        self["background"] = "#212529"


class Frame(tk.Frame):
    """Cria e posiciona um frame"""
    def __init__(
        self,
        *,
        root,
        largura:float,
        altura:float,
        ancora:str="center",
        posx:float=0.5,
        posy:float=0.5
        ):


        super().__init__(root)

        self["background"] = "#343A40"

        self.place(
            anchor=ancora, # type: ignore
            relx=posx,
            rely=posy,
            relheight=altura,
            relwidth=largura
            )


class Entry(ttk.Entry):
    """Cria um entry na raiz especificada"""
    def __init__(
        self,
        *,
        root,
        placeholder:str,
        largura:float,
        altura_px:int=25,
        posx:float=0.5,
        posy:float=0.5,
        ancora="center"
        ):

        super().__init__(root)

        self.placeholder = placeholder


        self["foreground"] = "#6C757D"
        self["justify"] = "center"

        self.insert(0, self.placeholder)

        self.bind("<FocusIn>", self.focus_in)
        self.bind("<FocusOut>", self.focus_out)


        self.place(
            anchor=ancora, # type: ignore
            relx=posx,
            rely=posy,
            relwidth=largura,
            height=altura_px
            )


    def focus_in(self, event):
        """Ação quando o widget toma foco"""
        if self.get() == self.placeholder:
            self.delete(0, "end")
            self["foreground"] = "Black"
            self["justify"] = "left"


    def focus_out(self, event):
        """Ação quando o widget perde o foco"""
        if not self.get().strip():
            self["foreground"] = "#6C757D"
            self["justify"] = "center"
            self.insert(0, self.placeholder)

class Button(tk.Button):
    """Cria um botão na aplicação"""

    def __init__(
        self,
        *,
        root,
        text,
        command,
        posy:float,
        posx:float=0.5,
        largura:float=0.8,
        ancora:str="center"
        ):


        super().__init__(root)
        self["text"] = text
        self["command"] = command

        self["foreground"] = "Light Gray"
        self["background"] = "#495057"
        self["activebackground"] = "#212529"
        self["activeforeground"] = "#CED4DA"
        self["relief"] = "flat"

        self.place(rely=posy, relx=posx, relwidth=largura, anchor=ancora) # type: ignore

class Table(ttk.Treeview):
    """Cria uma tabela na aplicação"""
    def __init__(
        self,
        *,
        root,
        colunas:tuple,
        tamanho_colunas:tuple,
        largura:float,
        altura:float,
        ancora:str="center",
        posx:float=0.5,
        posy:float=0.5,
        ):


        super().__init__(root, show="headings", columns=colunas)

        self.columns = colunas
        self.wid_col = tamanho_colunas

        for index, name in enumerate(self.columns):
            self.heading(name, text=name, anchor="center")
            self.column(name, width=self.wid_col[index], anchor="center")

        self.place(anchor=ancora, relx=posx, rely=posy, relheight=altura, relwidth=largura) #type: ignore


    def populate(self, table:str, filters:dict|None):
        """
        Popula a tabela
        Parametros:
            table: Tabela do banco de dados a ser consultada
            filters: filtros a usar no banco (caso haja)
        """
        for i in self.get_children():
            self.delete(i)

        if not filters:
            for i in db.select_from(table):
                self.insert("", "end", values=i)
        else:
            for i in db.select_from(table, filters):
                self.insert("", "end", values=i)


class Combobox(ttk.Combobox):
    """Cria um combobox na aplicação"""
    def __init__(
        self,
        *,
        root,
        valores:list,
        placeholder:str,
        largura:float,
        ancora:str="center",
        posx:float=0.5,
        posy:float=0.5,
        ):

        super().__init__(
            master=root,
            values=valores,
            justify="center"
            )

        self.placeholder = placeholder
        self.set(placeholder)

        self.place(anchor=ancora, relwidth=largura, relx=posx, rely=posy) #type: ignore
