from JWGL import FuckJWGL

import json
with open("config.json", "r") as file:
    data = json.load(file)
    print(FuckJWGL({
        "username": data["username"],
        "password": data["password"]
    }).fuck_the_teaching_evaluation())
