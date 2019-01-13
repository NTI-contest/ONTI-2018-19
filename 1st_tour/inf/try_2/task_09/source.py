import sys
from collections import defaultdict

def parse_inventory(inventory_text):
    inventory = defaultdict(int)
    for line in inventory_text.splitlines():
        words = line.split()
        if len(words) >= 2:
            title, quantity = ' '.join(words[:-1]), int(words[-1])
            inventory[title] += quantity
    return inventory

dataset = sys.stdin.read()

inventory_text, queries = [part.strip() for part in dataset.split('QUERIES')]
inventory = parse_inventory(inventory_text)

for item in queries.splitlines():
    print(inventory[item]) 