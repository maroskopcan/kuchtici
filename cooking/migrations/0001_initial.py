# Generated by Django 4.1.2 on 2022-10-16 07:21

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rec_title', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('rating', models.DecimalField(decimal_places=0, max_digits=3)),
                ('process', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReceiptRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('text', models.TextField()),
                ('receipt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='cooking.receipt')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_ratings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=5)),
                ('unit', models.CharField(max_length=16)),
                ('ingr_name', models.CharField(max_length=64)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=6)),
                ('rec_id', models.ManyToManyField(related_name='receipts', to='cooking.receipt')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(blank=True, max_length=64)),
                ('category_id', models.ManyToManyField(related_name='category', to='cooking.receipt')),
            ],
        ),
    ]
