from django.db import models

# Create your models here.
class Login(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    type=models.CharField(max_length=100)



class User(models.Model):
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    gender=models.CharField(max_length=10)
    email=models.CharField(max_length=100)
    phno=models.BigIntegerField()
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)

class Category(models.Model):
    cat_name=models.CharField(max_length=100)
    # photo=models.CharField(max_length=100)

class Preference(models.Model):
    name=models.CharField(max_length=100)
    CATEGORY=models.ForeignKey(Category,on_delete=models.CASCADE)
    USER=models.ForeignKey(User,on_delete=models.CASCADE)

class News(models.Model):
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=500)
    photo=models.CharField(max_length=100)
    date=models.DateField()
    CATEGORY=models.ForeignKey(Category,on_delete=models.CASCADE)

class Review(models.Model):
    review=models.CharField(max_length=100)
    date=models.DateField()
    USER=models.ForeignKey(User,on_delete=models.CASCADE)




