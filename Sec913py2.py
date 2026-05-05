products = [
    {"name": "Laptop", "price": 70000},
    {"name":"Mobile", "price": 20000},
    {"name":"Tablet", "price": 30000},
    {"name":"Headphones", "price": 2000}
]

min_price = int(input("Enter the minimum price: "))
max_price = int(input("Enter the maximum price: "))

filtered = [p for p in products if min_price <= p["price"] <= max_price]


sorted_products = sorted(filtered, key=lambda x: x["price"])

for p in sorted_products:
    print(p["name"], ":", p["price"])