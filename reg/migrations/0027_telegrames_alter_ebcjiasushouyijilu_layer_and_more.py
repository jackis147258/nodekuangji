# Generated by Django 4.2.3 on 2024-07-03 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reg', '0026_alter_paytoken_options_alter_paytoken_table_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='telegrames',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, '未生效'), (1, '已生效')], db_comment='0 未生效,1已生效', default=0)),
                ('cTime', models.IntegerField(blank=True, db_comment='操作时间', default=0, null=True)),
                ('uTime', models.IntegerField(blank=True, db_comment='更新时间', default=0, null=True)),
                ('TelUserId', models.CharField(blank=True, db_comment='task备注', max_length=255, null=True, verbose_name='备注')),
                ('TelUserName', models.CharField(blank=True, db_comment='task备注', max_length=255, null=True, verbose_name='备注')),
                ('TelUserText', models.CharField(blank=True, db_comment='task备注', max_length=255, null=True, verbose_name='备注')),
                ('Remark', models.CharField(blank=True, db_comment='task备注', max_length=255, null=True, verbose_name='备注')),
            ],
        ),
        migrations.AlterField(
            model_name='ebcjiasushouyijilu',
            name='Layer',
            field=models.IntegerField(blank=True, db_comment='0充值 1 代数 2 层数 3 #提现到账 日志 4.购买燃料包  11.得到奖金池', default=0, null=True, verbose_name='类型'),
        ),
        migrations.AlterField(
            model_name='paytoken',
            name='status',
            field=models.IntegerField(choices=[(0, '未生效'), (1, '返还'), (2, 'hash验证失败'), (3, 'hash验证成功')], db_comment='0 未生效,1,返回hash ,2 hash验证失败,3hash验证成功', default=0),
        ),
    ]
