# Generated by Django 2.0.5 on 2018-06-04 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feedback_app', '0002_auto_20180604_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='error',
            name='source_file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedback_app.SourceFile'),
        ),
    ]
