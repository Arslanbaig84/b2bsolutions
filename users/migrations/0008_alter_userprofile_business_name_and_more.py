# Generated by Django 4.2.5 on 2024-10-20 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_userprofile_industry_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='business_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='industry_type',
            field=models.TextField(),
        ),
    ]