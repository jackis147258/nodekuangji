# Generated by Django 4.2.3 on 2023-10-05 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0034_t_quantify1_token_price_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='t_trade',
            name='tradeHash',
            field=models.CharField(blank=True, db_comment='hash值', max_length=255, null=True, verbose_name='hash值'),
        ),
        migrations.AlterField(
            model_name='dengluinfo',
            name='type',
            field=models.SmallIntegerField(blank=True, choices=[(1, '普通post'), (2, 'post')], db_comment=' 普通post', default=1, null=True, verbose_name='普通post'),
        ),
        migrations.AlterField(
            model_name='t_task',
            name='status',
            field=models.IntegerField(choices=[(0, '停止'), (1, '正常')], db_comment='0 停止,正常', default=1),
        ),
        migrations.AlterField(
            model_name='t_tokenaddr',
            name='status',
            field=models.IntegerField(choices=[(0, '停止'), (1, '正常')], db_comment='0 停止,正常', default=1),
        ),
        migrations.AlterField(
            model_name='t_tokenaddrbak',
            name='status',
            field=models.IntegerField(choices=[(0, '停止'), (1, '正常')], db_comment='0 停止,正常', default=1),
        ),
        migrations.AlterField(
            model_name='t_trade',
            name='status',
            field=models.IntegerField(choices=[(0, '停止'), (1, '正常')], db_comment='0 停止,正常', default=1),
        ),
        migrations.AlterField(
            model_name='t_trade',
            name='tradeStatus',
            field=models.IntegerField(choices=[(0, '买'), (2, 'Approved'), (1, '卖')], db_comment='交易状态', default=1, verbose_name='0 停止,正常'),
        ),
        migrations.AlterField(
            model_name='tcsearch',
            name='paiXu',
            field=models.SmallIntegerField(blank=True, choices=[(3, '利润'), (2, '开始时间'), (4, 'ROI'), (1, '存在时间')], default=1, null=True, verbose_name='排序'),
        ),
        migrations.AlterField(
            model_name='tcsearch',
            name='raceTime',
            field=models.CharField(blank=True, choices=[('86400', '1天'), ('604800', '1周'), ('172800', '2天'), ('57600', '16小时'), ('43200', '12小时')], db_comment='raceTime比赛时间', default='86400', max_length=50, null=True, verbose_name='比赛时间'),
        ),
        migrations.AlterField(
            model_name='tcsport',
            name='type',
            field=models.SmallIntegerField(blank=True, choices=[(1, '体育类'), (2, '电竞类')], db_comment=' 比赛类型', default=1, null=True, verbose_name='比赛类型'),
        ),
        migrations.AlterField(
            model_name='webinfo',
            name='type',
            field=models.SmallIntegerField(blank=True, choices=[(1, '企业站'), (2, '功能站')], db_comment=' 类型', default=1, null=True, verbose_name='类型'),
        ),
    ]
