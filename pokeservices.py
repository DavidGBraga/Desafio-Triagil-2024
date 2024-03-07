# Importação de bibliotecas
from flask import Flask, make_response, jsonify, request
import requests
import json
import os

app = Flask(__name__)

# Define o caminho para o arquivo JSON que armazena as equipes de Pokémon
TEAMS_FILE = os.path.join(os.path.dirname(__file__), "models/teams.json")

# Carrega os dados das equipes de Pokémon do arquivo JSON
with open("models/teams.json", "r") as f:
    teams = json.load(f)

# Inicializa um contador para IDs de equipe
team_id_counter = len(teams) + 1

# Rota para obter todas as equipes de Pokémon (GET /api/teams)
@app.route('/api/teams', methods=['GET'])
def get_teams():
    return make_response(
        jsonify(teams)
        )

# Rota para obter as equipes de um usuário específico (GET /api/teams/<user>)
@app.route('/api/teams/<string:user>', methods=['GET'])
def get_teams_user(user):
    # Filtra as equipes pertencentes ao usuário fornecido
    user_teams = [team for team in teams if team.get('owner') == user]
    if user_teams:
        return jsonify(user_teams)
    else:
        return jsonify({"error": "Usuário não encontrado"}), 404

# Rota para criar uma nova equipe de Pokémon (POST /api/teams)
@app.route("/api/teams", methods=["POST"])
def create_team():
  global team_id_counter
  team = request.get_json()
  # Verifica se os dados fornecidos são válidos
  if not team or "user" not in team or "team" not in team:
    return jsonify({"error": "Dados inválidos"}), 400

  valid_pokemons = []
  for pokemon_name in team["team"]:
    # Verifica se o Pokémon existe na PokeAPI
    url_pokemon = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    response = requests.get(url_pokemon)
    if response.status_code == 404:
      return jsonify({"error": f"Pokémon '{pokemon_name}' não encontrado"}), 400
    pokemon_data = response.json()
    # Adiciona informações do Pokémon válido à lista
    valid_pokemons.append({
      "id": pokemon_data["id"],
      "name": pokemon_data["name"],
      "weight": pokemon_data["weight"],
      "height": pokemon_data["height"],
    })    

  # Cria um novo time de Pokémon com um ID único
  novo_time = {
    "id": team_id_counter,
    "owner": team["user"],
    "team": valid_pokemons
    }   
  
  team_id_counter += 1
  
  # Adiciona o novo time ao arquivo JSON de equipes
  with open('models/teams.json', 'r') as file:
    data = json.load(file)

    data.append(novo_time)

  with open('models/teams.json', 'w') as file:
    json.dump(data, file, indent=4)

    return jsonify({"message": f"Time do {team['user']} criado com sucesso!"}), 200

# Executa o servidor Flask na porta 5000 e no host 'localhost'            
app.run(port=5000,host='localhost',debug=True)
