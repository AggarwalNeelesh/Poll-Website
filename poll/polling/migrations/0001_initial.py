# Generated by Django 4.0.5 on 2022-07-06 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('Q_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField()),
                ('question', models.CharField(max_length=5000)),
                ('op1', models.CharField(max_length=500)),
                ('op2', models.CharField(max_length=500)),
                ('op3', models.CharField(max_length=500)),
                ('op4', models.CharField(max_length=500)),
                ('op0', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.IntegerField()),
                ('password', models.CharField(max_length=50)),
                ('questions', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Votes',
            fields=[
                ('v_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField()),
                ('Q_id', models.IntegerField()),
            ],
        ),
    ]
