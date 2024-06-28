import requests
from bs4 import BeautifulSoup


def obtener_proxies():
    url = "https://free-proxy-list.net/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    proxy_list = []

    for row in soup.find("table", {"id": "proxylisttable"}).find_all("tr")[1:]:
        cols = row.find_all("td")
        if cols[4].text == "elite proxy":  # Filtrar proxies anónimos
            proxy = f"{cols[0].text}:{cols[1].text}"
            proxy_list.append(proxy)

    return proxy_list


# Obtener la lista de proxies
proxies = obtener_proxies()
print(proxies)
