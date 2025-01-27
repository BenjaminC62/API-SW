import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)

URL = "https://summonerswar.fandom.com/wiki/Monster_Collection"

category_ids = ['Fire', 'Water', 'Wind', 'Light', 'Dark']

monsters = {category_id: [] for category_id in category_ids}

def get_monster_details(monster_url):
    response = requests.get(monster_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    details = {}

    # On cherche la balise <b> avec le mot Species
    species_tag = soup.find('b', string='Type:')
    # On recup la valeur du td ou ya la balise b dedans
    if species_tag:
        # Récupérer la valeur du <td> qui contient la balise <b> avec 'Type:'
        species_value = species_tag.find_parent('tr').find('td').text.strip()

        # Enlever le premier mot 'Type:' et ne garder que la valeur (par exemple 'Support')
        details['type'] = species_value.split(' ', 1)[-1]
    else:
        details['type'] = 'Unknown'

    # Recherche des balises <a> qui contiennent des liens vers les images
    image_tags = [tag for tag in soup.find_all('a', {'class': 'image'}) if 'href' in tag.attrs]

    # On s'assure de ne pas prendre les images d'élément comme "Fire", "Water", etc.
    non_eveille_image = None
    eveille_image = None

    for tag in image_tags:
        image_url = tag['href']

        if image_url.startswith('/'):
            image_url = 'https://summonerswar.fandom.com' + image_url

        if 'Icon' in image_url and 'Element' not in image_url:
            if not non_eveille_image:
                non_eveille_image = image_url
            elif not eveille_image:
                eveille_image = image_url

    details['image_url_non_eveille'] = non_eveille_image
    details['image_url_eveille'] = eveille_image if eveille_image else None

    print(f"Image URL non éveillé: {details['image_url_non_eveille']}")
    if eveille_image:
        print(f"Image URL éveillé: {details['image_url_eveille']}")
    else:
        print("Pas d'image éveillée disponible")

    return details


response = requests.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')

# Pour chaque catégorie, je mets un # de la catégorie sur l'URL
for category_id in category_ids:
    category_url = f"{URL}#{category_id}"
    print(f"Scraping category: {category_url}")
    category_response = requests.get(category_url)
    category_soup = BeautifulSoup(category_response.content, 'html.parser')

    # On cherche la balise <a> avec l'élément title pour récupérer le nom du monstre
    for a in category_soup.find_all('a', href=True):
        if '/wiki/' in a['href'] and 'title' in a.attrs:
            monster_name = a['title']
            monster_url = a['href']

            if category_id.lower() in monster_name.lower():
                # Récupérer les détails du monstre
                details = get_monster_details(f"https://summonerswar.fandom.com{monster_url}")

                monsters[category_id].append({
                    "name": monster_name,
                    "details_url": f"https://summonerswar.fandom.com{monster_url}",
                    "details": details  # Ajouter les détails récupérés
                })

for category, monsters_list in monsters.items():
    print(f"Category: {category}")
    for monster in monsters_list:
        print(f"Name: {monster['name']}, URL: {monster['details_url']}")
        print(f"Details: {monster['details']}")

print(f"Total monsters: {sum(len(monsters_list) for monsters_list in monsters.values())}")


@app.route('/api/monsters', methods=['GET'])
def get_monster_list():
    return jsonify(monsters)


if __name__ == '__main__':
    app.run(debug=True)
