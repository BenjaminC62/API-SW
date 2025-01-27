import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)

URL = "https://summonerswar.fandom.com/wiki/Monster_Collection"

category_ids = ['Fire', 'Water', 'Wind', 'Light', 'Dark']

monsters = {category_id: [] for category_id in category_ids}

# La requête pour scrapper la page
response = requests.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')

# Pour chaque catégorie, je mets un # de la catégorie sur l'URL
for category_id in category_ids:
    category_url = f"{URL}#{category_id}"
    print(f"Scraping category: {category_url}")
    category_response = requests.get(category_url)
    category_soup = BeautifulSoup(category_response.content, 'html.parser')

    # On cherche la balise <a> avec l'élement title pour récupérer le nom du monstre
    for a in category_soup.find_all('a', href=True):
        if '/wiki/' in a['href'] and 'title' in a.attrs:
            monster_name = a['title']
            monster_url = a['href']

            if category_id.lower() in monster_name.lower():
                monsters[category_id].append({
                    "name": monster_name,
                    "details_url": f"https://summonerswar.fandom.com{monster_url}"
                })

for category, monsters_list in monsters.items():
    print(f"Category: {category}")
    for monster in monsters_list:
        print(f"Name: {monster['name']}, URL: {monster['details_url']}")

print(f"Total monsters: {sum(len(monsters_list) for monsters_list in monsters.values())}")

@app.route('/api/monsters', methods=['GET'])
def get_monster_list():
    return jsonify(monsters)

if __name__ == '__main__':
    app.run(debug=True)
