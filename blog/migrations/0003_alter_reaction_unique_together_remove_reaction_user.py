# Generated by Django 4.2.6 on 2024-02-16 00:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_reaction'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='reaction',
            unique_together={('post', 'comment')},
        ),
        migrations.RemoveField(
            model_name='reaction',
            name='user',
        ),
    ]
