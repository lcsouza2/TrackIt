DROP TABLE IF EXISTS usuario;
DROP TABLE IF EXISTS categoria;
DROP TABLE IF EXISTS despesa;
DROP TABLE IF EXISTS parcelamento;
DROP TABLE IF EXISTS pagamento;

CREATE TABLE IF NOT EXISTS usuario(
    id_user      INTEGER   PRIMARY KEY   AUTOINCREMENT,
    email        VARCHAR(100)   NOT NULL,
    username     VARCHAR(30)    NOT NULL,
    senha_hash   VARCHAR(255)   NOT NULL,

    CONSTRAINT uq_usuario
        UNIQUE(email)
);

CREATE TABLE IF NOT EXISTS categoria(
    id_categoria        INTEGER   PRIMARY KEY   AUTOINCREMENT,
    id_user_categoria   INTEGER        NOT NULL,
    nome_categoria      VARCHAR(20)    NOT NULL,
    cor_categoria       CHAR(7)        NOT NULL,

    CONSTRAINT uq_categoria
        UNIQUE(id_user_categoria, nome_categoria, cor_categoria),
    CONSTRAINT fk_categoria_usuario
        FOREIGN KEY(id_user_categoria)
        REFERENCES usuario(id_user)
);

CREATE TABLE IF NOT EXISTS despesa(
    id_despesa             INTEGER   PRIMARY KEY   AUTOINCREMENT,
    id_categoria_despesa   INTEGER         NOT NULL,
    id_user_despesa        INTEGER         NOT NULL,
    data_despesa           DATE            NOT NULL,
    valor_despesa          NUMERIC(10,2)   NOT NULL,
    obs_despesa            VARCHAR(100)    NOT NULL,

    CONSTRAINT uq_despesa
        UNIQUE(id_categoria_despesa, id_user_despesa, data_despesa, valor_despesa, obs_despesa),
    
    CONSTRAINT fk_despesa_categoria
        FOREIGN KEY(id_categoria_despesa)
        REFERENCES categoria(id_categoria),

    CONSTRAINT fk_despesa_usuario
        FOREIGN KEY(id_user_despesa)
        REFERENCES usuario(id_user)
);

CREATE TABLE IF NOT EXISTS parcelamento(
    id_parcelamento             INTEGER   PRIMARY KEY   AUTOINCREMENT,
    id_categoria_parcelamento   INTEGER         NOT NULL,
    id_user_parcelamento        INTEGER         NOT NULL,
    obs_parcelamento            VARCHAR(100)    NOT NULL,
    qtd_parcelas                INTEGER         NOT NULL,
    valor_parcelas              NUMERIC(10,2)   NOT NULL,
    porcent_juros               NUMERIC(4,3)        NULL,
    valor_total_parcelamento    NUMERIC(10,2)   NOT NULL,
    data_inicio_parcelamento    DATE            NOT NULL,
    
    CONSTRAINT uq_parcelamento
        UNIQUE(data_inicio_parcelamento, valor_total_parcelamento, qtd_parcelas),

    CONSTRAINT fk_parcelamento_categoria
        FOREIGN KEY(id_categoria_parcelamento)
        REFERENCES categoria(id_categoria),
    
    CONSTRAINT fk_parcelamento_user
        FOREIGN KEY(id_user_parcelamento)
        REFERENCES usuario(id_user)
);

CREATE TABLE IF NOT EXISTS pagamento(
    id_pagamento                INTEGER   PRIMARY KEY   AUTOINCREMENT,
    id_user_pagamento           INTEGER         NOT NULL,
    id_despesa_pagamento        INTEGER             NULL,
    id_parcelamento_pagamento   INTEGER             NULL,
    obs_pagamento               VARCHAR(100)    NOT NULL,
    valor_pagamento             NUMERIC(10,2)   NOT NULL,
    data_pagamento              DATE            NOT NULL,

    CONSTRAINT uq_pagamento
        UNIQUE(id_user_pagamento, obs_pagamento, valor_pagamento, data_pagamento),

    CONSTRAINT fk_pagamento_usuario
        FOREIGN KEY(id_user_pagamento)
        REFERENCES usuario(id_user),
    
    CONSTRAINT fk_pagamento_despesa
        FOREIGN KEY(id_despesa_pagamento)
        REFERENCES despesa(id_despesa),
    
    CONSTRAINT fk_pagamento_parcelamento
        FOREIGN KEY(id_parcelamento_pagamento)
        REFERENCES parcelamento(id_parcelamento)
);

