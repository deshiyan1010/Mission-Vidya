import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","donate.settings")

import django 
django.setup()

import pandas as pd
from apply_main.models import State,Subdistrict,District

csv = pd.read_csv("final.csv")
sc = 0
print(csv.describe())
for x in csv["State Name"].unique():
    state = State.objects.create(name=str(x))
    state.save()
    sc+=1
    sd = 0
    for y in csv[csv["State Name"]==str(x)]["District Name"].unique():
        dist = District.objects.create(name=str(y),state=state)
        dist.save()
        sd+=1
        print("District Counter: ",sd," State Counter: ",sc)
        for z in csv[(csv["State Name"]==str(x)) & (csv["District Name"]==str(y))]["Subdistrict Name"]:
            subdis = Subdistrict.objects.create(name=str(z),district=dist)
            subdis.save()
print(csv.head())