import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request

app = Flask(__name__)

BASE_URL = "https://summonerswar.fandom.com"

URL = "https://summonerswar.fandom.com/wiki/Monster_Collection#Fire"

# La requete pour scrapper la page
response = requests.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')

monsters = []

# Je récupère les informations des monstres
for row in soup.select('table tr'):
    link_tag = row.find('a')
    img_tag = row.find('img')

    # Si les balises sont trouvées, je récupère les informations
    if link_tag and img_tag:
        name = link_tag['title']
        details_url = BASE_URL + link_tag['href']

        monsters.append({
            "name": name,
            "details_url": details_url,
        })

# Afficher les résultats
for monster in monsters:
    print(monster)

print(len(monsters))

@app.route('/api/monsters', methods=['GET'])
def get_monster_list():
    return jsonify(monsters)


if __name__ == '__main__':
    app.run(debug=True)
