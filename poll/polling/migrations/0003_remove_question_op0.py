# Generated by Django 4.0.5 on 2022-07-08 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polling', '0002_question_vop1_question_vop2_question_vop3_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='op0',
        ),
    ]
