import urllib.request, json

url = "https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=d4ec995fe57eb20540e34ceaa70350df"

resposta = urllib.request.urlopen(url)

dados = resposta.read()

jsondata = json.loads(dados)
print(jsondata['results'])