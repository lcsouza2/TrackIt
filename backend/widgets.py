"""Módulo com classes inicializadoras dos widgets tkinter"""

#pylint: disable= import-error, unused-argument

import tkinter.messagebox as mbx
import tkinter as tk
from tkinter import ttk
from typing import  Callable, Literal
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
        root:tk.Tk | tk.Toplevel,
        largura:float,
        altura:float,
        ancora:str="center",
        posx:float=0.5,
        posy:float=0.5,
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


class Text(tk.Label):
    def __init__(
        self, 
        *, 
        root, 
        text:str, 
        text_color:str="#CED4DA",
        font_size:int=11,
        justificar:Literal["left", "center", "right"]="center",
        hyperlink_func:Callable | None,
        posy:float, 
        posx:float=0.5, 
        ancora="center"
        ):
        
        
        self.str_var = tk.StringVar(value=text)
                
                
        super().__init__(
            root, 
            textvariable=self.str_var, 
            justify=justificar, 
            background=root["background"],
            foreground=text_color,
            font=("TkDefaultFont", font_size)
            )
        
        
        if hyperlink_func:
            self.bind("<Button-1>", hyperlink_func)
    
    
        self.place(relx=posx, rely=posy, anchor=ancora) #type: ignore
        
        
class Entry(ttk.Entry):
    """Cria um entry na raiz especificada"""
    def __init__(
        self,
        *,
        root:tk.Tk|tk.Frame|ttk.Frame,
        placeholder:str,
        on_update_text:str,
        posy:float,
        posx:float=0.5,
        altura_px:int=25,
        largura:float=0.8,
        ancora="center"
        ):

        
        super().__init__(root)
                
        self.placeholder = placeholder
        
        self["foreground"] = "#6C757D"
        self["justify"] = "center"

        self.insert(0, self.placeholder)

        self.bind("<FocusIn>", self.focus_in, add="+")
        self.bind("<FocusOut>", self.focus_out, add="+")
        self.bind("<FocusOut>", lambda x: self.set(on_update_text), add="+")
        
        self.place(
            anchor=ancora, # type: ignore
            relx=posx,
            rely=posy,
            relwidth=largura,
            height=altura_px
            )
    
    def set(self, base_text:str):
        """Atualiza o valor do widget para o especificado"""
        text = self.get()
        
        if text and text not in (self.placeholder, base_text) and base_text not in text:
            self["justify"] = "center"
            self.delete(0, "end")
            self.insert(0, base_text+text)

    
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
    
    def get_formated(self):
        """Retorna o conteúdo digitado pelo usuário formatado"""
        return self.get().split(":")[-1].strip()


class Combobox(ttk.Combobox):
    """Cria um combobox na aplicação"""
    def __init__(
        self,
        *,
        root:tk.Tk|tk.Frame|ttk.Frame,
        valores:list | tuple,
        placeholder:str,
        on_update_text:str,
        posy:float,
        posx:float=0.5,
        ancora:str="center",
        largura:float=0.8,
        ):


        super().__init__(
            master=root,
            values=valores,
            justify="center",
            )

        self.placeholder = placeholder
        self.set(placeholder)

        self.bind("<<ComboboxSelected>>", lambda x: self.set(on_update_text + self.get()))
        
        self.place(anchor=ancora, relwidth=largura, relx=posx, rely=posy) #type: ignore

    def get_formated(self):
        """Retorna o conteúdo digitado pelo usuário formatado"""
        return self.get().split(":")[-1].strip()

class Button(tk.Button):
    """Cria um botão na aplicação"""

    def __init__(
        self,
        *,
        root:tk.Tk|tk.Frame|ttk.Frame,
        text:str,
        command:Callable|None,
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
        root:tk.Tk|tk.Frame|ttk.Frame,
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

    def get_selection(self, not_null:bool=True):
        if not_null:
            selection = {}
            
            for key, value in self.set(self.selection()).items(): #type:ignore
                if not value:
                    mbx.showerror("Erro!", "Não foi selecionada nenhuma linha na tabela")
                    raise Exception("Não foi selecionada uma linha da tabela")
                selection.update({key: value})
            return selection
        return self.set(self.selection()) #type:ignore 
        
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
            for i in sorted(db.select_from(table)):
                self.insert("", "end", values=i)
        else:
            for i in sorted(db.select_from(table, filters)):
                self.insert("", "end", values=i)


