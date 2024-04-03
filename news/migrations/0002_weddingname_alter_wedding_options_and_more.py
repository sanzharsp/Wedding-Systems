# Generated by Django 4.0.5 on 2023-06-03 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeddingName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Чей праздник?')),
                ('description', models.TextField(verbose_name='Описание')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата записи в базу данных')),
                ('WeddingDate', models.DateTimeField(verbose_name='Дата праздника')),
            ],
            options={
                'verbose_name': 'праздник',
                'verbose_name_plural': 'Праздники',
                'ordering': ['created_at'],
            },
        ),
        migrations.AlterModelOptions(
            name='wedding',
            options={'ordering': ['created_at'], 'verbose_name': 'приглашение', 'verbose_name_plural': 'приглашение'},
        ),
        migrations.AlterField(
            model_name='wedding',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата заявкий'),
        ),
        migrations.AddField(
            model_name='wedding',
            name='WeddingName',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='related_orders', to='news.weddingname', verbose_name='Чей праздник'),
            preserve_default=False,
        ),
    ]
