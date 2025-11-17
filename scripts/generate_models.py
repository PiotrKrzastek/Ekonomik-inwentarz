from dotenv import load_dotenv
import os
import subprocess

load_dotenv('../.env')

SCHEMA = 'public'

OUTFILE = f'../app/models/autogen/{SCHEMA}.py'

USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

decision = input("UWAGA. Wszystkie modele automatycznie wygenerowane zostaną nadpisane! Jeśli chcesz kontynuować wpisz 'ok': ")
if decision.lower() == 'ok':
    print(f'Generuję plik modeli dla schematu {SCHEMA}')
    subprocess.run(['sqlacodegen', DATABASE_URL, '--schema', SCHEMA, '--outfile', OUTFILE], check=True)
