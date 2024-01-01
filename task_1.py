import csv
import json
import random
import sys
import logging
from functools import wraps

logging.basicConfig(filename='error.log', level=logging.ERROR)

def save_to_json(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result_data = []

        with open(args[0], mode='r', newline='') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                try:
                    a, b, c = map(int, row)
                    roots = func(a, b, c)
                    result_data.append({
                        "a": a,
                        "b": b,
                        "c": c,
                        "roots": roots
                    })
                except Exception as e:
                    logging.error(f"An error occurred while processing the input data: {e}")

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
    try:
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
    except Exception as e:
        logging.error(f"An error occurred while finding the roots: {e}")
        return None

if len(sys.argv) == 3:
    input_file = sys.argv[1]
    rows = int(sys.argv[2])
    generate_csv_file(input_file, rows)
    find_roots(input_file)
else:
    print("Usage: python script_name.py input_file.csv number_of_rows")

with open("results.json", 'r') as f:
    data = json.load(f)

if 100 <= len(data) <= 1000:
    print(True)
else:
    print(f"Количество строк в файле не находится в диапазоне от 100 до 1000.")

print(len(data) == rows)