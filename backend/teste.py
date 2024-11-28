import sqlite3

def teste():

    connection = sqlite3.connect("backend/TrackIt.db")
    cursor = connection.cursor()

    cursor.executescript("""DROP TABLE categoria;  CREATE TABLE categoria(
    id_categoria        INTEGER   PRIMARY KEY   AUTOINCREMENT,
    id_user_categoria   INTEGER        NOT NULL,
    nome_categoria      VARCHAR(20)    NOT NULL,
    cor_categoria       VARCHAR(25)        NOT NULL,

    CONSTRAINT uq_categoria
        UNIQUE(id_user_categoria, nome_categoria, cor_categoria),
    CONSTRAINT fk_categoria_usuario
        FOREIGN KEY(id_user_categoria)
        REFERENCES usuario(id_user)
)""")


teste()