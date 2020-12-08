"""Módulo de conexão com a base de dados

Esse módulo é responsável pela conexão com uma base de dados da EMAp-FGV,
referente ao trabalho da A2 de Linguagens de Programação. Para o funcionamento
do mesmo, é requerido que se tenha instalado no ambiente de instalação do
python os pacotes 'pyodbc' e 'pandas'. Os drivers do Microsoft ODBC 17 para
SQL Server. Após a execução do script, a conexão é fechada.

O módulo pode ser importado, e contém as seguintes variáveis:
    
    * server - objeto do tipo (str) que contém o endereço do server
    * database - objeto do tipo (str) que contém o nome da base de dados
    * username - objeto do tipo (str) que contém o usuário de acesso
    * passowrd - objeto do tipo (str) que contém a senha de acesso
    * driver - objeto do tipo (str) que contém o driver utilizado na conexão
    * initialCatalog - objeto do tipo (str) que contém o início da conexão
    * conn - objeto do tipo (pyodbc.Connection) responsável por efetivar a
    conexão, utilizando as variáveis na string de conexão
    * data_ufc - objeto do tipo (pandas.core.frame.DataFrame) que representa a
    base de dados de lutas do UFC.
    * data_fifa - objeto do tipo (pandas.core.frame.DataFrame) que representa a
    base de dados dos jogadores presentes no jogo FIFA 19.
"""

import pyodbc
import pandas as pd

server = "fgv-db-server.database.windows.net"
database = "fgv-db"
username = "student"
password = "@dsInf123"
driver = "{ODBC Driver 17 for SQL Server}"
initialCatalog = "fgv-db";

conn = pyodbc.connect("DRIVER="+driver
                      + ";SERVER="+server
                      + ";Initial Catalog ="+initialCatalog
                      + ";PORT=1433;"
                      "DATABASE="+database
                      +";UID="+username
                      +";PWD="+password)

data_ufc = pd.read_sql("SELECT * FROM ufc.ufc_master", conn)

data_fifa = pd.read_sql("SELECT * FROM fifa.fifa_players", conn)

conn.close()