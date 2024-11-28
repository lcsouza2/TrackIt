DROP TABLE IF EXISTS usuario;
DROP TABLE IF EXISTS categoria;
DROP TABLE IF EXISTS compra;
DROP TABLE IF EXISTS parcelamento;
DROP TABLE IF EXISTS parcelas;

CREATE TABLE IF NOT EXISTS usuario(
    username      VARCHAR(30)    NOT NULL,
    email         VARCHAR(100)   NOT NULL,
    plano_usado   INTEGER        NOT NULL,
    moeda         CHAR(3)        NOT NULL,
    senha_hash    VARCHAR(255)   NOT NULL,

    CONSTRAINT pk_usuario
        PRIMARY KEY(username)
);

CREATE TABLE IF NOT EXISTS categoria(
    username         VARCHAR(30)        NOT NULL,
    nome_categoria   VARCHAR(40)    NOT NULL,
    descricao        VARCHAR(100)   NOT NULL,
    cor_categoria    CHAR(7)        NOT NULL,

    CONSTRAINT pk_categoria
        PRIMARY KEY(username, nome_categoria),

    CONSTRAINT fk_categoria_usuario
        FOREIGN KEY(username)
        REFERENCES usuario(username)
);

CREATE TABLE IF NOT EXISTS compra(
    username          VARCHAR(30)     NOT NULL,
    nome_categoria    VARCHAR(40)     NOT NULL,
    titulo_compra     VARCHAR(30)     NOT NULL,
    obs_compra        VARCHAR(100)    NOT NULL,
    data_compra       DATE            NOT NULL,
    repeticao_dias    INTEGER         NOT NULL,
    valor_compra      NUMERIC(10,2)   NOT NULL,
    pago              INTEGER         NOT NULL,

    CONSTRAINT pk_compra
        PRIMARY KEY(username, nome_categoria, titulo_compra),
    
    CONSTRAINT fk_despesa_categoria
        FOREIGN KEY(username, nome_categoria)
        REFERENCES categoria(username, nome_categoria)
);

CREATE TABLE IF NOT EXISTS parcelamento(
    username              VARCHAR(30)   NOT NULL,
    nome_categoria        VARCHAR(40)   NOT NULL,
    titulo_parcelamento   VARCHAR(30)   NOT NULL,
    obs_parcelamento      VARCHAR(100)   NOT NULL,
    qtd_parcelas          INTEGER        NOT NULL,
    valor_parcelas        NUMERIC(10,2)   NOT NULL,
    data_inicio           DATE            NOT NULL,
    porc_juros            NUMERIC(6,2)    NULL,
    periodo_juros         CHAR(2)         NULL,

    CONSTRAINT pk_parcelamento
        PRIMARY KEY(username, nome_categoria, titulo_parcelamento)

    CONSTRAINT fk_parcelamento_categoria
        FOREIGN KEY(username, nome_categoria)
        REFERENCES categoria(username, nome_categoria)
);

CREATE TABLE IF NOT EXISTS parcelas(
    num_parcela   INTEGER   NOT NULL,
    titulo_parcelamento   VARCHAR(30)   NOT NULL,
    nome_categoria        VARCHAR(40)   NOT NULL,
    username              VARCHAR(70)   NOT NULL,
    pago                  INTEGER       NOT NULL,

    CONSTRAINT pk_parcelas
        PRIMARY KEY(num_parcela, titulo_parcelamento, nome_categoria, username)
);

