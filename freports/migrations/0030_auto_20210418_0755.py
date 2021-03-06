# Generated by Django 3.1.8 on 2021-04-18 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freports', '0029_auto_20210410_0816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='number',
            field=models.IntegerField(verbose_name='Номер провадження'),
        ),
        migrations.AlterField(
            model_name='report',
            name='number_year',
            field=models.CharField(max_length=128, null=True, verbose_name='Рік реєстрації'),
        ),
        migrations.AlterField(
            model_name='reportevents',
            name='subspecies',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Підвид події'),
        ),
        migrations.AlterField(
            model_name='research',
            name='number',
            field=models.IntegerField(verbose_name='Номер провадження'),
        ),
        migrations.AlterField(
            model_name='research',
            name='number_year',
            field=models.CharField(max_length=128, null=True, verbose_name='Рік реєстрації'),
        ),
    ]
