import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém o token do GitHub da variável de ambiente
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Verifica se o token foi carregado corretamente
if not GITHUB_TOKEN:
    raise Exception("GitHub token not found. Please check your .env file.")

# Definindo cabeçalhos para a requisição GraphQL
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json"
}

# Query GraphQL para buscar os 1000 repositórios Java mais populares
def get_repositories(after_cursor=None):
    query = """
    query($language: String!, $first: Int!, $after: String) {
      search(query: $language, type: REPOSITORY, first: $first, after: $after) {
        repositoryCount
        pageInfo {
          endCursor
          hasNextPage
        }
        edges {
          node {
            ... on Repository {
              nameWithOwner
              stargazerCount
              createdAt
              url
              releases {
                totalCount
              }
              primaryLanguage {
                name
              }
            }
          }
        }
      }
    }
    """

    variables = {
        "language": "language:Java",
        "first": 50,
        "after": after_cursor
    }

    response = requests.post(
        "https://api.github.com/graphql", 
        headers=headers, 
        json={"query": query, "variables": variables}
    )

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed with status code {response.status_code}: {response.content}")

# Função para coletar os dados dos repositórios
def collect_data():
    repositories_data = []
    has_next_page = True
    after_cursor = None

    while has_next_page and len(repositories_data) < 1000:
        result = get_repositories(after_cursor)
        repos = result["data"]["search"]["edges"]

        for repo in repos:
            node = repo["node"]
            created_at = datetime.strptime(node["createdAt"], "%Y-%m-%dT%H:%M:%SZ")
            age_in_years = ((datetime.now() - created_at).days / 365).__round__(2)

            repositories_data.append({
                "name": node["nameWithOwner"],
                "stars": node["stargazerCount"],
                "age_in_years": age_in_years,
                "releases": node["releases"]["totalCount"],
                "primary_language": node["primaryLanguage"]["name"] if node["primaryLanguage"] else None,
                "url": node["url"],
                "processed": False

            })

        after_cursor = result["data"]["search"]["pageInfo"]["endCursor"]
        has_next_page = result["data"]["search"]["pageInfo"]["hasNextPage"]

        print(f"Collected {len(repositories_data)} repositories so far...")

    return repositories_data

# Salvando os dados em um arquivo CSV
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_file_path = os.path.join(project_root, 'data', 'repos.csv')

def save_to_csv(data):
    df = pd.DataFrame(data)
    df.to_csv(csv_file_path, index=False)
    print("Data saved to src/data/repos.csv")

# Executa a coleta e salva os dados
data = collect_data()
save_to_csv(data)

