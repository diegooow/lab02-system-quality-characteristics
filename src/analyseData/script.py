import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# Definir o caminho raiz do projeto
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Definir o caminho para o arquivo CSV
csv_file_path = os.path.join(project_root, 'data', 'metrics_results.csv')

# Definir a pasta para salvar os gráficos
output_dir = os.path.join(project_root, 'data', 'plots')
os.makedirs(output_dir, exist_ok=True)

# Carregar o CSV
df = pd.read_csv(csv_file_path)

# Verificar as primeiras linhas para garantir que os dados foram carregados corretamente
print("Primeiras linhas do DataFrame:")
print(df.head())

# Verificar se todas as linguagens são Java
unique_languages = df['primary_language'].unique()
print(f"\nLinguagens únicas no DataFrame: {unique_languages}")

# Definir as métricas de qualidade
quality_metrics = ['cbo:mean', 'cbo:median', 'cbo:std', 'lcom*:mean', 'lcom*:median', 'lcom*:std']

# Preencher valores nulos com a média da coluna (se houver)
df[quality_metrics] = df[quality_metrics].fillna(df[quality_metrics].mean())

# Agregar as métricas de qualidade em uma única pontuação (quality_score)
# Aqui, estamos calculando a média das métricas de qualidade
df['quality_score'] = df[quality_metrics].mean(axis=1)

# Função para calcular e imprimir correlações com p-valores
def calcular_correlacoes(df, variavel, metrics):
    print(f"\n### Correlações com {variavel} ###")
    for metric in metrics:
        corr_value, p_value = pearsonr(df[variavel], df[metric])
        print(f"Correlação entre {variavel} e {metric}: {corr_value:.2f} (p-valor: {p_value:.4f})")

# Calcular correlações com p-valores
calcular_correlacoes(df, 'stars', ['quality_score'])
calcular_correlacoes(df, 'age_in_years', ['quality_score'])
calcular_correlacoes(df, 'releases', ['quality_score'])
calcular_correlacoes(df, 'loc', ['quality_score'])

# Adicionar Estatísticas Descritivas
print("\n### Estatísticas Descritivas da Pontuação de Qualidade ###")
print(df['quality_score'].describe())

# Função para gerar e salvar scatter plots usando Pandas
def save_scatter_plot(df, x, y, title, name):
    ax = df.plot.scatter(x=x, y=y, title=title, figsize=(8,6))
    plt.tight_layout()
    scatter_path = os.path.join(output_dir, name)
    plt.savefig(scatter_path)
    plt.close()
    print(f"Gráfico de dispersão salvo em: {scatter_path}")

# Gerar e salvar os gráficos de dispersão para cada RQ
# RQ01: Relação entre popularidade (stars) e qualidade
save_scatter_plot(df, 'quality_score', 'stars', 'Popularidade vs Qualidade', 'scatter_popularity_quality.png')

# RQ02: Relação entre maturidade (age_in_years) e qualidade
save_scatter_plot(df, 'quality_score', 'age_in_years', 'Maturidade vs Qualidade', 'scatter_maturity_quality.png')

# RQ03: Relação entre atividade (releases) e qualidade
save_scatter_plot(df, 'quality_score', 'releases', 'Atividade vs Qualidade', 'scatter_activity_quality.png')

# RQ04: Relação entre tamanho (loc) e qualidade
save_scatter_plot(df, 'quality_score', 'loc', 'Tamanho vs Qualidade', 'scatter_size_quality.png')
