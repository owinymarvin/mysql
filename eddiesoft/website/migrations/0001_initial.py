# Generated by Django 4.2.7 on 2023-11-07 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('branch_number', models.AutoField(primary_key=True, serialize=False)),
                ('telephone_number', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=255)),
                ('price', models.IntegerField(choices=[(1200, '1200'), (1500, '1500'), (1800, '1800'), (2000, '2000'), (2500, '2500'), (3000, '3000')])),
            ],
        ),
        migrations.CreateModel(
            name='Members',
            fields=[
                ('member_number', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('date_of_registration', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('staff_number', models.AutoField(primary_key=True, serialize=False)),
                ('staff_names', models.CharField(max_length=255)),
                ('salary', models.IntegerField()),
                ('position', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('catalog_number', models.AutoField(primary_key=True, serialize=False)),
                ('video_number', models.IntegerField(unique=True)),
                ('title', models.CharField(max_length=255)),
                ('actor', models.CharField(max_length=255)),
                ('director', models.CharField(max_length=255)),
                ('copies', models.IntegerField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.category')),
            ],
        ),
        migrations.CreateModel(
            name='RentedVideo',
            fields=[
                ('rental_number', models.AutoField(primary_key=True, serialize=False)),
                ('date_of_rent', models.DateField()),
                ('date_of_return', models.DateField()),
                ('catalog_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.video')),
                ('member_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.members')),
            ],
        ),
    ]
