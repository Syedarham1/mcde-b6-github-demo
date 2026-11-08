import csv

def reconcile_inventory(inv_path, mov_path, updated_path, rejected_path):
  
    inventory = {}
    with open(inv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            inventory[row['sku']] = {
                'name': row['name'],
                'quantity': int(row['quantity'])
            }

    rejected = []
    with open(mov_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sku = row['sku']
            m_type = row['type'].upper()
            try:
                units = int(row['units'])
            except ValueError:
                rejected.append({**row, 'reason': 'Invalid units format'})
                continue

            if sku not in inventory:
                rejected.append({**row, 'reason': 'Unknown SKU'})
                continue
            if units <= 0:
                rejected.append({**row, 'reason': 'Non-positive units'})
                continue

            if m_type == 'IN':
                inventory[sku]['quantity'] += units
            elif m_type == 'OUT':
                if inventory[sku]['quantity'] < units:
                    rejected.append({**row, 'reason': 'Insufficient stock'})
                else:
                    inventory[sku]['quantity'] -= units
            else:
                rejected.append({**row, 'reason': 'Invalid movement type'})

    with open(updated_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['sku', 'name', 'quantity'])
        writer.writeheader()
        for sku, data in inventory.items():
            writer.writerow({'sku': sku, 'name': data['name'], 'quantity': data['quantity']})

    with open(rejected_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['sku', 'type', 'units', 'reason'])
        writer.writeheader()
        for row in rejected:
            writer.writerow(row)