# Generated by Django 5.2.1 on 2025-05-21 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("problems", "0009_historicalsolution"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalproblem",
            name="problem_text",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="problem",
            name="problem_text",
            field=models.TextField(blank=True, null=True),
        ),
    ]
