# Generated by Django 4.2.3 on 2024-01-02 07:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reg', '0006_ebcjiasushouyijilu_fanhuan_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name_plural': '用户列表'},
        ),
        migrations.AlterModelTableComment(
            name='customuser',
            table_comment='用户列表',
        ),
    ]
