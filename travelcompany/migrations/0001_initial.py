# Generated by Django 4.2.2 on 2023-07-03 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Places',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='pics')),
                ('place', models.CharField(max_length=25)),
                ('desc', models.TextField()),
                ('price', models.IntegerField()),
            ],
        ),
    ]