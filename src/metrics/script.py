import os
import json
import numpy as np
import subprocess
import csv
import shutil

# raiz do projeto
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def read_csv():
    csv_file_path = os.path.join(project_root, 'data', 'repos.csv')
    
    # Remove o arquivo de resultados anteriores, se existir
    output_file = os.path.join(project_root, 'data', 'metrics_results.csv')
    if os.path.isfile(output_file):
        os.remove(output_file)

    if not os.path.isfile(csv_file_path):
        print(f"File not found: {csv_file_path}")
        return
    
    # Lê o arquivo CSV de repositórios e processa cada URL
    with open(csv_file_path, mode='r') as f:
        reader = csv.DictReader(f)    
        for row in reader:
            url = row.get('url')
            if url:
                process_repo(url)

def process_repo(repo):
    ck_jar_path = os.path.join(project_root, 'metrics', 'ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar')
    output_file = os.path.join(project_root, 'data', 'metrics_results.csv')
    write_header = not os.path.isfile(output_file) 

    try:
        # Remove o diretório /tmp/repo se ele existir e recria
        if os.path.exists('/tmp/repo'):
            shutil.rmtree('/tmp/repo')
        os.makedirs('/tmp/repo')

        # Clona o repositório
        subprocess.run(["git", "clone", repo, "--filter=blob:none", "/tmp/repo"], check=True)

        # Executa o comando Java para análise
        java_command = f"java -jar {ck_jar_path} /tmp/repo false 0 false /tmp/"
        print(f"Running command: {java_command}")
        subprocess.run(java_command, shell=True, check=True)

        # Converte CSV para JSON
        print(f"Converting CSV to JSON... ")
        os.system("csv-to-json /tmp/class.csv /tmp/class.json")

        # Processa o arquivo JSON
        with open('/tmp/class.json') as file:
            data = json.load(file)

        # Dados para debug
        # print(f"JSON Data: {data}")

        attributes = {
            'repo_url': repo,
            'dit': 0,
            'loc': 0,
            'cbo:mean': 0.0,
            'cbo:median': 0.0,
            'cbo:std': 0.0,
            'lcom*:mean': 0.0,
            'lcom*:median': 0.0,
            'lcom*:std': 0.0
        }
        
        # listas temporárias para calcular métricas
        cbo_values = []
        lcom_values = []

        for d in data:
            loc_value = d.get('loc')
            cbo_value = d.get('cbo')
            lcom_value = d.get('lcom*')
            dit_value = d.get('dit')

            if loc_value and loc_value != 'NaN':
                attributes['loc'] += float(loc_value)
            if cbo_value and cbo_value != 'NaN':
                cbo_values.append(float(cbo_value))
            if lcom_value and lcom_value != 'NaN':
                lcom_values.append(float(lcom_value))
            if dit_value and dit_value != 'NaN':
                attributes['dit'] = max(attributes['dit'], float(dit_value))

        # Cálculo das métricas
        if cbo_values:
            attributes['cbo:mean'] = np.mean(cbo_values)
            attributes['cbo:median'] = np.median(cbo_values)
            attributes['cbo:std'] = np.std(cbo_values)

        if lcom_values:
            attributes['lcom*:mean'] = np.mean(lcom_values)
            attributes['lcom*:median'] = np.median(lcom_values)
            attributes['lcom*:std'] = np.std(lcom_values)

        # Salva o resultado em um arquivo CSV
        with open(output_file, 'a', newline='') as csvfile:
            fieldnames = attributes.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            if write_header:
                writer.writeheader()
                
            writer.writerow(attributes)
        
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while processing {repo}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

read_csv()
