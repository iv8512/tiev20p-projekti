import os, json

def list_files():
    for path, folders, files in os.walk("maps"):
        break
    return files

for file in list_files():
    print(file)
    with open(f"maps/{file}") as data:
        data = json.load(data)
    new_data = {"Map": []}
    for column_data in data["Map"]:
        new_column = []
        for block in column_data:
            match block:
                case 0:
                    new_column.append("None")
                case 1:
                    new_column.append("Wall")
                case 2:
                    new_column.append("Player")
                case 3:
                    new_column.append("Apple")
        new_data["Map"].append(new_column)
    with open(f"maps/{file}", "w") as file:
        json.dump(new_data, file, indent=4)
