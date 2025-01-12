# Generated by Django 3.2.16 on 2025-01-11 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_post_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('created_at', 'text'), 'verbose_name': 'комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AddField(
            model_name='comment',
            name='is_published',
            field=models.BooleanField(default=True, help_text='Снимите галочку, чтобы скрыть модель.', verbose_name='Опубликовано'),
        ),
        migrations.AlterField(
            model_name='category',
            name='is_published',
            field=models.BooleanField(default=True, help_text='Снимите галочку, чтобы скрыть модель.', verbose_name='Опубликовано'),
        ),
        migrations.AlterField(
            model_name='location',
            name='is_published',
            field=models.BooleanField(default=True, help_text='Снимите галочку, чтобы скрыть модель.', verbose_name='Опубликовано'),
        ),
        migrations.AlterField(
            model_name='post',
            name='is_published',
            field=models.BooleanField(default=True, help_text='Снимите галочку, чтобы скрыть модель.', verbose_name='Опубликовано'),
        ),
    ]
