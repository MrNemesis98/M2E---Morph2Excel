import json

term = input()

# Lade die englische Flexionsdatei von Wiki_Morph
with open("data/wiki_morph.json", "r", encoding="utf-8") as f:
    entries_list = json.load(f)

for x in range(len(entries_list)):

    for key, value in entries_list[x].items():

        if key == "Word":
            if value == term:
                
                print(entries_list[x])
