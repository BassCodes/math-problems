# Generated by Django 5.2.1 on 2025-05-14 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("problems", "0004_alter_branch_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="problem",
            name="has_answer",
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
