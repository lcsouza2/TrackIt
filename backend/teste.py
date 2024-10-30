import datetime
import calendar
import sqlite3
import utils

import time
import categories


with sqlite3.connect(utils.DB_ROUTE) as connection:
        cursor = connection.cursor()

        cursor.executescript(
            """
                DROP TABLE IF EXISTS pagamento;
                
                CREATE TABLE pagamento(
                    id_pagamento                INTEGER   PRIMARY KEY   AUTOINCREMENT,
                    id_user_pagamento           INTEGER         NOT NULL,
                    id_despesa_pagamento        INTEGER             NULL,
                    id_parcelamento_pagamento   INTEGER             NULL,
                    numero_parcela              INTEGER             NULL,
                    obs_pagamento               VARCHAR(100)    NOT NULL,
                    valor_pagamento             NUMERIC(10,2)   NOT NULL,

                    CONSTRAINT uq_despesa
                        UNIQUE(id_despesa_pagamento, obs_pagamento, valor_pagamento),
                        
                    CONSTRAINT uq_parcelamento
                        UNIQUE(id_parcelamento_pagamento, numero_parcela)
                        );
            """
            
        )

        result = cursor.fetchone()
        
        print(result)