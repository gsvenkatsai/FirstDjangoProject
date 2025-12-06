import json
import random
from datetime import datetime, timedelta
import uuid

# CONFIG
NUM_USERS = 200
COLLECTION_TITLES = [
    "Electronics","Smartphones","Laptops","Tablets","Accessories",
    "Home Appliances","Clothing","Footwear","Books","Sports & Fitness"
]

category_data = {
    "Electronics": [
        "4K TV", "Bluetooth Speaker", "Wireless Earbuds", "Soundbar", "Smartwatch",
        "DSLR Camera", "Power Bank", "Portable Projector", "Smart Home Hub", "Drone",
        "Action Camera", "Bluetooth Headphones", "Home Theater", "Gaming Console",
        "VR Headset", "Smart Light", "Fitness Tracker", "Security Camera",
        "Electric Scooter", "Streaming Device"
    ],
    "Smartphones": [
        "iPhone 15 Pro", "Samsung Galaxy S24", "Google Pixel 8", "OnePlus 12", "Xiaomi 14",
        "Asus ROG Phone 8", "Nothing Phone 2", "Motorola Edge 40", "Sony Xperia 5", "Oppo Find X6",
        "Vivo X100", "Realme GT 5", "Honor Magic 5", "Redmi Note 13", "Samsung A55",
        "iPhone SE", "Google Pixel 8a", "OnePlus Nord 3", "Xiaomi 13T", "Huawei P60"
    ],
    "Laptops": [
        "MacBook Pro 16", "Dell XPS 15", "HP Spectre x360", "Lenovo ThinkPad X1", "Asus ZenBook",
        "Acer Predator Helios", "Razer Blade 15", "Microsoft Surface Laptop 5", "LG Gram 17", "MSI Stealth 14",
        "MacBook Air M3", "HP Envy 14", "Acer Swift 5", "Lenovo Legion 7", "Asus TUF A15",
        "Dell G16", "MSI Creator Z16", "Framework Laptop", "Gigabyte Aero 16", "Huawei MateBook X Pro"
    ],
    "Tablets": [
        "iPad Pro 12.9", "Samsung Galaxy Tab S9", "Xiaomi Pad 6", "Lenovo Tab P12 Pro", "Microsoft Surface Pro 9",
        "Huawei MatePad Pro", "Amazon Fire HD 10", "Realme Pad 2", "OnePlus Pad", "Oppo Pad Air",
        "iPad Air 5", "Lenovo Yoga Tab 13", "Honor Pad 8", "TCL Tab 10", "Samsung Tab A9",
        "Xiaomi Pad SE", "iPad Mini 6", "Teclast M50", "Chuwi Hi10", "Alldocube iPlay 50"
    ],
    "Accessories": [
        "Wireless Charger", "USB-C Cable", "Laptop Stand", "Portable SSD", "Webcam",
        "Wireless Mouse", "Mechanical Keyboard", "Phone Case", "Tablet Cover", "Stylus Pen",
        "Gaming Headset", "Smart Plug", "Screen Protector", "Bluetooth Adapter", "Tripod Stand",
        "Car Mount", "LED Desk Lamp", "Memory Card", "External HDD", "Wireless Router"
    ],
    "Home Appliances": [
        "Air Conditioner", "Washing Machine", "Refrigerator", "Microwave Oven", "Air Purifier",
        "Coffee Maker", "Vacuum Cleaner", "Dishwasher", "Water Heater", "Blender",
        "Induction Cooktop", "Rice Cooker", "Toaster", "Electric Kettle", "Hair Dryer",
        "Iron Box", "Mixer Grinder", "Ceiling Fan", "Juicer"
    ],
    "Clothing": [
        "Men's T-Shirt", "Women's Dress", "Jeans", "Formal Shirt", "Jacket",
        "Sweatshirt", "Hoodie", "Shorts", "Skirt", "Kurta",
        "Saree", "Tracksuit", "Blazer", "Suit", "Crop Top",
        "Leggings", "Sweater", "Coat", "Scarf", "Polo Shirt"
    ],
    "Footwear": [
        "Running Shoes", "Sneakers", "Loafers", "Formal Shoes", "Sandals",
        "Flip Flops", "Boots", "Heels", "Slippers", "Crocs",
        "Sports Shoes", "Casual Shoes", "Ankle Boots", "Ballet Flats", "Clogs",
        "Dress Shoes", "Trail Running Shoes", "Leather Boots", "Slides", "Moccasins"
    ],
    "Books": [
        "The Alchemist", "Atomic Habits", "Sapiens", "The 48 Laws of Power", "The Psychology of Money",
        "The Subtle Art of Not Giving a F*ck", "Rich Dad Poor Dad", "Think and Grow Rich", "Educated", "Becoming",
        "The Silent Patient", "The Midnight Library", "Ikigai", "Can't Hurt Me", "1984",
        "Dune", "Harry Potter and the Sorcerer’s Stone", "To Kill a Mockingbird", "The Hobbit", "Pride and Prejudice"
    ],
    "Sports & Fitness": [
        "Yoga Mat", "Dumbbell Set", "Treadmill", "Exercise Bike", "Resistance Bands",
        "Skipping Rope", "Foam Roller", "Sports Bottle", "Gym Bag", "Smart Scale",
        "Pull-up Bar", "Massage Gun", "Cricket Bat", "Football", "Basketball",
        "Badminton Racket", "Tennis Racket", "Golf Clubs", "Hiking Backpack", "Camping Tent"
    ]
}

# Tags - NOTE: your current models.py doesn't include a Tag model or a "tags" M2M on Product.
# I include these 10 labels here, but to persist them into fixtures you must add a Tag model
# and a ManyToManyField on Product. See the note at the end.
TAG_LABELS = [
    "new-arrival","best-seller","discount","limited","popular",
    "eco-friendly","premium","budget","exclusive","trending"
]

# Begin building fixtures
fixtures = []

pk_counters = {
    'core.user': 1,
    'store.promotion': 1,
    'store.collection': 1,
    'store.product': 1,
    'store.customer': 1,
    'store.address': 1,
    'store.order': 1,
    'store.orderitem': 1,
    'store.cart': 1,
    'store.cartitem': 1,
    'store.review': 1,
}

# Helper to next pk
def next_pk(model_name):
    pk = pk_counters[model_name]
    pk_counters[model_name] += 1
    return pk

# 1) Users
from faker import Faker
fake = Faker()
for i in range(1, NUM_USERS + 1):
    pk = next_pk('core.user')
    first_name = fake.first_name()
    last_name = fake.last_name()
    username = (first_name + last_name + str(pk)).replace(' ', '').lower()
    fixtures.append({
        'model': 'core.user',
        'pk': pk,
        'fields': {
            'password': 'pbkdf2_sha256$260000$dummy$dummyhashdummy',
            'last_login': None,
            'is_superuser': False,
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'email': f'{username}@example.com',
            'is_staff': False,
            'is_active': True,
            'date_joined': datetime.utcnow().isoformat()
        }
    })

# 2) Promotions (6)
promo_texts = ["10% OFF", "15% OFF", "B1G1", "Clearance 20%", "Summer 5%", "Free Shipping"]
for text in promo_texts:
    pk = next_pk('store.promotion')
    fixtures.append({
        'model': 'store.promotion',
        'pk': pk,
        'fields': {'description': text, 'discount': float(random.choice([5,10,15,20]))}
    })

# 3) Collections (10)
collection_pks = {}
for title in COLLECTION_TITLES:
    pk = next_pk('store.collection')
    collection_pks[title] = pk
    fixtures.append({
        'model': 'store.collection',
        'pk': pk,
        'fields': {'title': title, 'featured_product': None}
    })

# 4) Products (20 per collection => 200)
product_entries = []
for title in COLLECTION_TITLES:
    items = category_data[title]
    coll_pk = collection_pks[title]
    for name in items:
        pk = next_pk('store.product')
        slug = name.lower().replace(' ', '-').replace("’","'")
        slug = ''.join(ch for ch in slug if ch.isalnum() or ch=='-')
        slug = f'{slug}-{pk}'
        price = round(random.uniform(50, 2000), 2)
        inventory = random.randint(0, 500)
        # random promotions assign
        prom_count = random.choice([0,0,1,1,2])
        promotions = random.sample(range(1, len(promo_texts)+1), k=prom_count) if prom_count>0 else []
        prod = {
            'model': 'store.product',
            'pk': pk,
            'fields': {
                'title': name,
                'slug': slug,
                'description': f'Dummy description for {name}',
                'unit_price': f'{price:.2f}',
                'inventory': inventory,
                'last_update': datetime.utcnow().isoformat(),
                'collection': coll_pk,
                'promotions': promotions
            }
        }
        product_entries.append(prod)
        fixtures.append(prod)

# Set featured_product for each collection to first product in that collection
prod_by_collection = {}
for p in product_entries:
    coll = p['fields']['collection']
    prod_by_collection.setdefault(coll, []).append(p['pk'])
for coll_pk, prod_list in prod_by_collection.items():
    # update corresponding collection fixture entry
    for entry in fixtures:
        if entry['model']=='store.collection' and entry['pk']==coll_pk:
            entry['fields']['featured_product'] = prod_list[0]
            break

# 5) Customers (one per user)
for user_pk in range(1, NUM_USERS+1):
    pk = next_pk('store.customer')
    fixtures.append({
        'model': 'store.customer',
        'pk': pk,
        'fields': {
            'user': user_pk,
            'phone': f'+91123456{user_pk:04d}',
            'birth_date': None,
            'membership': random.choice(['B','S','G'])
        }
    })

# 6) Addresses (one per customer)
for cust_pk in range(1, NUM_USERS+1):
    pk = next_pk('store.address')
    fixtures.append({
        'model': 'store.address',
        'pk': pk,
        'fields': {
            'zip': f'{400000 + (cust_pk % 1000)}',
            'street': f'{cust_pk} Sample Street',
            'city': random.choice(['Mumbai','Bengaluru','Chennai','Delhi','Kolkata','Hyderabad']),
            'customer': cust_pk
        }
    })

# 7) Orders & OrderItems: each user gets 2 orders; each order has 1+ distinct items
# We'll produce timestamps that are all different by incrementing seconds
start_time = datetime.utcnow() - timedelta(days=365)
order_time_increment = 0
for cust_pk in range(1, NUM_USERS+1):
    num_orders = random.choice([2,2,3])  # at least 2, sometimes 3
    for _ in range(num_orders):
        order_pk = next_pk('store.order')
        # unique timestamp per order
        placed_at = (start_time + timedelta(seconds=order_time_increment)).isoformat()
        order_time_increment += random.randint(1, 300)  # add 1..300 seconds
        fixtures.append({
            'model': 'store.order',
            'pk': order_pk,
            'fields': {
                'payment_status': random.choice(['P','C','F']),
                'placed_at': placed_at,
                'customer': cust_pk
            }
        })
        # create 1..4 distinct items per order
        num_items = random.randint(1,4)
        available_product_pks = list(range(1, len(product_entries)+1))
        items_for_order = random.sample(available_product_pks, k=num_items)
        for prod_pk in items_for_order:
            oi_pk = next_pk('store.orderitem')
            # find unit price from product_entries
            unit_price = next(p['fields']['unit_price'] for p in product_entries if p['pk']==prod_pk)
            fixtures.append({
                'model': 'store.orderitem',
                'pk': oi_pk,
                'fields': {
                    'order': order_pk,
                    'product': prod_pk,
                    'quantity': random.randint(1,5),
                    'unit_price': unit_price
                }
            })

# 8) Carts & CartItems - create carts for a subset of users
for cust_pk in range(1, NUM_USERS+1, 10):  # one cart per 10 users
    cart_pk = str(uuid.uuid4())
    # Note: Cart model uses UUID primary key; in fixtures the pk should be the uuid string
    fixtures.append({
        'model': 'store.cart',
        'pk': cart_pk,
        'fields': {
            'carted_at': (datetime.utcnow() - timedelta(days=random.randint(0,30))).isoformat()
        }
    })
    # add 1..3 cart items
    for _ in range(random.randint(1,3)):
        ci_pk = next_pk('store.cartitem')
        prod_pk = random.randint(1, len(product_entries))
        fixtures.append({
            'model': 'store.cartitem',
            'pk': ci_pk,
            'fields': {
                'cart': cart_pk,
                'product': prod_pk,
                'quantity': random.randint(1,3)
            }
        })

# 9) Reviews - create ~100 reviews across random products
for _ in range(100):
    rv_pk = next_pk('store.review')
    prod_pk = random.randint(1, len(product_entries))
    fixtures.append({
        'model': 'store.review',
        'pk': rv_pk,
        'fields': {
            'product': prod_pk,
            'name': f'Reviewer{rv_pk}',
            'description': f'This is a review for product {prod_pk}',
            'date': (datetime.utcnow() - timedelta(days=random.randint(0,365))).date().isoformat()
        }
    })

# Write fixtures.json
with open('fixtures.json','w',encoding='utf-8') as f:
    json.dump(fixtures, f, ensure_ascii=False, indent=2)

print('fixtures.json generated:')
print(f'  users: {NUM_USERS}')
print(f'  collections: {len(COLLECTION_TITLES)}')
print(f'  products: {len(product_entries)}')
print(f'  customers: {NUM_USERS}')
print(f'  orders: {pk_counters["store.order"]-1}')
print(f'  orderitems: {pk_counters["store.orderitem"]-1}')
print(f'  reviews: {pk_counters["store.review"]-1}')