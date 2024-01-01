import csv
import json
import random
from functools import wraps


def save_to_json(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result_data = []

        with open(args[0], mode='r', newline='') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                a, b, c = map(int, row)
                roots = func(a, b, c)
                result_data.append({
                    "a": a,
                    "b": b,
                    "c": c,
                    "roots": roots
                })

        with open('results.json', 'w') as json_file:
            json.dump(result_data, json_file, indent=4)

        return result_data

    return wrapper

def generate_csv_file(file_name, rows):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        for _ in range(rows):
            row = [random.randint(100, 999) for _ in range(3)]  # Генерируем три случайных числа
            writer.writerow(row)

@save_to_json
def find_roots(a, b, c):
    discriminant = b**2 - 4*a*c
    
    if discriminant > 0:
        root1 = (-b + (discriminant ** 0.5)) / (2*a)
        root2 = (-b - (discriminant ** 0.5)) / (2*a)
        return root1, root2
    elif discriminant == 0:
        root = -b / (2*a)
        return root
    else:
        return None

generate_csv_file("input_data.csv", 200)
find_roots("input_data.csv")

with open("results.json", 'r') as f:
    data = json.load(f)

if 100<=len(data)<=1000:
    print(True)
else:
    print(f"Количество строк в файле не находится в диапазоне от 100 до 1000.")

print(len(data)==200)