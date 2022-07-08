from django.db import models


class User(models.Model):
    # Model to save all the User details
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
    # Model to save all the Questions uploaded by User
    Q_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    question = models.CharField(max_length=5000)
    op1 = models.CharField(max_length=500)
    op2 = models.CharField(max_length=500)
    op3 = models.CharField(max_length=500)
    op4 = models.CharField(max_length=500)

    # No. of Votes Given to options
    vop1 = models.IntegerField(default=0)
    vop2 = models.IntegerField(default=0)
    vop3 = models.IntegerField(default=0)
    vop4 = models.IntegerField(default=0)

    def __str__(self):
        return str(self.Q_id)


class Votes(models.Model):
    # Model to save that which user has voted which Question
    v_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    Q_id = models.IntegerField()
