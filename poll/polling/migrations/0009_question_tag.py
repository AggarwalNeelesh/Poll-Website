# Generated by Django 4.0.5 on 2023-08-27 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polling', '0008_alter_question_user_id_alter_votes_q_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='tag',
            field=models.CharField(default='All', max_length=100),
        ),
    ]
