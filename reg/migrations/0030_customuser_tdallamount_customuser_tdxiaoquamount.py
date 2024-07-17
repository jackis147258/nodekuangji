# Generated by Django 4.2.3 on 2024-07-15 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reg', '0029_ebcjiasushouyijilu_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='TDallAmount',
            field=models.FloatField(blank=True, db_comment='团队总值', default=0, null=True, verbose_name='团队总值'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='TDxiaoQuAmount',
            field=models.FloatField(blank=True, db_comment='团队小区总值', default=0, null=True, verbose_name='团队小区总值'),
        ),
    ]
