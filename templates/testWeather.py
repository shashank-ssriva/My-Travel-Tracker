import urllib.request, json 
mostvisiteddest = "Delhi"
with urllib.request.urlopen("https://api.weatherbit.io/v2.0/current?city=%s&key=c1c3dd1fde8649ac8ff1e2f2d40e16d9" %mostvisiteddest) as url:
    data = json.loads(url.read().decode())
    print(data['data'][0]['rh'])