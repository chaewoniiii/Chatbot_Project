# Generated by Django 3.2.5 on 2022-06-06 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TrainData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intent', models.CharField(max_length=128)),
                ('ner', models.CharField(max_length=128)),
                ('query', models.TextField(blank=True)),
                ('answer', models.TextField(blank=True)),
                ('answer_add', models.CharField(max_length=32)),
                ('stage', models.IntegerField(default=0)),
                ('stage_change', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='UserChatData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.TextField(blank=True)),
                ('ai_intent', models.CharField(max_length=128)),
                ('ai_ner', models.CharField(max_length=128)),
                ('ad_intent', models.CharField(max_length=128)),
                ('ad_ner', models.CharField(max_length=128)),
                ('trian_num', models.IntegerField(default=0)),
                ('on_train', models.BooleanField(default=True)),
                ('reg_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]