# Generated by Django 3.1 on 2020-08-04 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificado', '0004_auto_20200714_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificado',
            name='carga_horaria',
            field=models.CharField(max_length=100, verbose_name='Carga horária'),
        ),
    ]
