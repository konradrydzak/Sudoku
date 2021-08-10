import json
import urllib.request

with open('data.json', 'w') as json_file:
    json_file.write('{ "sudoku_boards_data_base": [ ')
    for i in range(100):
        with urllib.request.urlopen("http://www.cs.utep.edu/cheon/ws/sudoku/new/?size=9&?level=3") as url:
            data = json.loads(url.read().decode())
            json.dump(data, json_file)
        if i != 100 - 1:
            json_file.write(", ")
    json_file.write(" ] }")
