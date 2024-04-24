import os
from datetime import datetime, timedelta
from random import randint

repo_link = "https://github.com/Faccin27/keylogger-KeystrokeToDiscord.git"  # Substitua isso pelo link do seu repositório

os.system("git init")
os.system("git remote add origin " + repo_link)

data_inicial = datetime.now() - timedelta(days=30)

for i in range(1, 61):  
    data = data_inicial + timedelta(days=randint(0, 29))
    data_str = data.strftime('%Y-%m-%d %H:%M:%S')  # Formato correto da data

    os.system(f"git commit --date=\"{data_str}\" -m 'commit'")  # Utilizando f-string para inserir a data formatada

os.system("git push -u origin main")  # Ajuste o nome do branch conforme necessário
