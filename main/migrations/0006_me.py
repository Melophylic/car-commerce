# Generated by Django 4.2.16 on 2024-09-18 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_delete_person_remove_product_kelas_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Me',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(default='Muhammad Nadzim Tahara', max_length=255)),
                ('npm', models.CharField(default='2306275430', max_length=255)),
                ('kelas', models.CharField(default='PBP C 2024', max_length=255)),
            ],
        ),
    ]
