from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.IntegerField()
    password = models.CharField(max_length=50)
    questions = models.IntegerField()
    def __str__(self):
        return str(self.user_id) + " " + str(self.username)

class Question(models.Model):
    Q_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    question = models.CharField(max_length=5000)
    op1 = models.CharField(max_length=500)
    op2 = models.CharField(max_length=500)
    op3 = models.CharField(max_length=500)
    op4 = models.CharField(max_length=500)
    # Correct Option
    op0 = models.CharField(max_length=500)

    def __str__(self):
        return str(self.Q_id)


class Votes(models.Model):
    v_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    Q_id = models.IntegerField()
