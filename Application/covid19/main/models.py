from django.db import models
import pandas as pd
# Create your models here.
df = pd.read_csv("https://opendata.arcgis.com/datasets/6ac5e325468c4cb9b905f1728d6fbf0f_0.csv?outSR=%7B%22latestWkid%22%3A3857%2C%22wkid%22%3A102100%7D")
hospital_names = df['NAME'].to_list()
hospital_names = [(name, name) for name in hospital_names]

class Ventilator(models.Model):
    id = models.AutoField(primary_key=True)
    hospital_name = models.CharField(choices=hospital_names, max_length=200, default='')
    ventilator_number = models.IntegerField()
