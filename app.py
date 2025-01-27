import requests
from bs4 import BeautifulSoup

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
        img_url = img_tag['src']

        monsters.append({
            "name": name,
            "details_url": details_url,
            "image_url": img_url
        })

# Afficher les résultats
for monster in monsters:
    print(monster)

print(len(monsters))

