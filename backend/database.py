"""Módulo para gerenciamento do banco de dados"""

from typing import Literal
import sqlite3
import psycopg2

def connect(sgdb:Literal['PostgreSQL', 'SQLite']):
    """
    Função:
        Conecta ao banco de dados
    Parameters:
        sgdb: SGDB a se conectar, podendo ser Postgre ou SQLite
    Retorna:
        Conexão e cursor

    """
    if sgdb == 'PostgreSQL':
        conn = psycopg2.connect(
            dbname="Villagers",
            host="localhost",
            user="postgres",
            password="bd"
            )
    else:
        conn = sqlite3.connect("Villagers.db")

    cur = conn.cursor()
    return conn, cur

def insert_into(table:str, data:dict):
    """
        Insere dados no banco de dados
        Args:
            table: tabela destino
            data: dicionário especificando os dados no formato {coluna : valor}
    """
    conn, cur = connect('PostgreSQL')

    columns = ", ".join(key for key in data.keys()) #Especifica colunas da tabela com base no dicionário

    values = tuple(data.values()) #Tupla com os valores de cada coluna
    
    query = f"INSERT INTO {table}({columns}) VALUES {values}"  #Query a ser executada no db

    cur.execute(query) #Executa a query no db

    conn.commit()
    conn.close()

def select_from(table:str, filters:dict={}):

    """
        Seleciona os dados no banco de dados
        Args:
            table: tabela a ser consultada
            filters: dicionário com as condições de filtragem no formato {coluna : valor}
        Retorna:
            Linhas encontradas segundo os filtros
    """

    conn, cur = connect('PostgreSQL')

    if not filters:
        data = cur.execute(f"""SELECT * FROM {table}""") #Seleciona todos os dados da tabela 
        data = cur.fetchall() #Retorna um tupla com todos os dados encontrados na query executada
        conn.close()
        return data

    else:
        columns = [key for key in filters.keys()]
        values = tuple(filters.values())

        base_query = f"SELECT * FROM {table} WHERE "

        where_clause = []

        for index, column in enumerate(columns):
            where_clause.append(
                column + f" LIKE '%{values[index]}%'"
                if not values[index].isdigit()
                else column + f" = {values[index]}"
                )

        parameters = " AND ".join(where_clause)

        data = cur.execute(base_query + parameters)

        data = cur.fetchall()
        return data

def update_data(table:str, data:dict, filters:dict):
    """Conecta ao banco de dados e atualiza um dado específico

    Args:
        table (str): tabela com o dado a ser alterado
        data (dict): dado novo,
        filters (dict): dado antigo que será alterado
    """

    con, cur = connect('PostgreSQL')

    base_query = f"UPDATE {table}" #Começo da query

    update_columns = [] # Lista com as colunas a serem alteradas

    for column, value in data.items():
        update_columns.append(
            " = ".join(
                [column, f"'{value}'"
                if not value.isdigit()
                else value]
                )
            ) #Adiciona na lista as colunas que serão alteradas e os seus valores

    set_query =" SET " + ", ".join(update_columns) #Constroi a query SET com os valores da lista de colunas

    parameters = [] #Lista com os itens de filtragem

    for column, value in filters.items():
        parameters.append(" = ".join([column, f"'{value.strip()}'" if not value.isdigit() else value])) #Adiciona os filtros a lista

    where_query = " WHERE " + " AND ".join(parameters) #Constroi a query de filtros

    cur.execute(base_query + set_query + where_query)
    con.commit()
    con.close()

def delete_data(table:str, data:dict):
    """
    Função:
        Remove dados do banco de dados
    Parametros:
        table: Tabela do banco de dados
        data: dicionário com os dados para remover
    """

    con, cur = connect('PostgreSQL')

    base_query = f"DELETE FROM {table}"

    parameters = []

    for column, value in data.items():
        parameters.append(" = ".join([column, f"'{value}'" if not value.isdigit() else value])) #Adiciona os filtros a lista

    where_query = " WHERE " + " AND ".join(parameters) #Constroi a query de filtros

    cur.execute(base_query + where_query)
    con.commit()
    con.close()
