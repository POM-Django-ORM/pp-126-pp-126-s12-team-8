# Generated by Django 4.1 on 2025-03-25 23:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('author', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Unknown', max_length=128)),
                ('description', models.TextField()),
                ('count', models.IntegerField(default=10)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='author.author')),
            ],
        ),
    ]
