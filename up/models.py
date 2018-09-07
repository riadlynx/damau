from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    occupation = models.CharField(max_length = 100)
    tel = models.CharField(max_length = 100,default="tel")
    company = models.CharField(max_length = 100,default="company")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.first_name + ' : '+ self.occupation
class Barrage(models.Model):
    name = models.CharField(max_length = 100)
    BV = models.CharField(max_length = 100,default="Bassin versant")
    P = models.CharField(max_length = 100,default="province")
    O = models.CharField(max_length = 100,default="oued")
    T = models.CharField(max_length = 100,default="type de barrages")
    CP = models.CharField(max_length = 100,default="Crue de projet")
    RN = models.CharField(max_length = 100,default="RN")
    PHE = models.CharField(max_length = 100,default="PHE")

    prof = models.ForeignKey(Profile, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
class Instrument(models.Model):
    name = models.CharField(max_length = 100)
    bar = models.ForeignKey(Barrage, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Fileup(models.Model):
    fich = models.FileField()
    inst = models.ForeignKey(Instrument, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return str(self.fich)
class Rapport(models.Model):
    prof = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date = models.DateField()
    fich = models.FileField()
    def __str__(self):
        return self.name+" le: "+str(self.date)

class todo(models.Model):
    prof = models.ForeignKey(Profile, on_delete=models.CASCADE)
    todo = models.TextField()
    date = models.DateField()
    def __str__(self):
        return self.todo+" Avant le: "+str(self.date)

