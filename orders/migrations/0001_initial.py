# Generated by Django 4.2.7 on 2023-11-29 14:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('county', models.CharField(max_length=100)),
                ('deliveryPoint', models.CharField(max_length=150)),
                ('deliveryPoint2', models.CharField(blank=True, max_length=150)),
                ('phone', models.CharField(blank=True, max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('total_paid', models.IntegerField()),
                ('price', models.IntegerField(default=1)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('order_key', models.CharField(max_length=200)),
                ('billing_status', models.BooleanField(default=False)),
                ('email', models.CharField(blank=True, max_length=150)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_product', to='store.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
