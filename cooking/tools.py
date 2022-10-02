import json
from .models import Receipt, Ingredients
from decimal import Decimal

with open('receipts.json', 'rb') as fp:
    receipts_load = json.load(fp)

for rl in receipts_load:

    for item in rl[3][0]:
        p += item
    r = Receipt(rec_title=item[0], author='WEB', rating=5, process=p)
    r.save()

    for item in rl[2]:
        i1 = item[2]
        i2 = item[0]
        if i2 == "":
            i2 = 0
        else:
            i2 = Decimal(i2)
        i3 = item[1]
        i = Ingredients(ingr_name=i1, quantity=i2, unit=i3, price=0)
        i.save()
        i.rec_id.add(r)




