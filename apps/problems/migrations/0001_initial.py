# Generated by Django 5.2.1 on 2025-05-11 23:48

import django.db.models.deletion
import problems.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Branch",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField()),
                ("description", models.TextField(blank=True, null=True)),
            ],
            options={
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.CreateModel(
            name="Source",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField()),
                ("shortname", models.TextField(blank=True, null=True)),
                ("subtitle", models.TextField(blank=True, null=True)),
                (
                    "problem_count",
                    models.PositiveSmallIntegerField(blank=True, null=True),
                ),
                ("description", models.TextField(blank=True, null=True)),
                ("publish_date", models.DateField(blank=True, null=True)),
                ("url", models.URLField(blank=True, null=True)),
            ],
            options={
                "ordering": ["parent", "name"],
            },
        ),
        migrations.CreateModel(
            name="SourceGroup",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField()),
                ("description", models.TextField(blank=True, null=True)),
                ("url", models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Technique",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField()),
                ("description", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="Type",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField()),
                ("description", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Problem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("problem_text", models.TextField()),
                ("answer_text", models.TextField()),
                ("pub_date", models.DateField(blank=True, null=True)),
                ("number", models.PositiveSmallIntegerField()),
                (
                    "categories",
                    models.ManyToManyField(
                        blank=True, related_name="problems", to="problems.branch"
                    ),
                ),
                (
                    "contributor",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "source",
                    models.ForeignKey(
                        default=problems.models.Source.get_default_pk,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="problems",
                        to="problems.source",
                    ),
                ),
                (
                    "types",
                    models.ManyToManyField(
                        blank=True, related_name="problems", to="problems.type"
                    ),
                ),
            ],
            options={
                "unique_together": {("source", "number")},
            },
        ),
        migrations.AddField(
            model_name="source",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sources",
                to="problems.sourcegroup",
            ),
        ),
        migrations.CreateModel(
            name="Solution",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("solution_text", models.TextField()),
                (
                    "problem",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="solutions",
                        to="problems.problem",
                    ),
                ),
                (
                    "techniques",
                    models.ManyToManyField(
                        blank=True, related_name="solutions", to="problems.technique"
                    ),
                ),
            ],
        ),
        migrations.AlterUniqueTogether(
            name="source",
            unique_together={("parent", "shortname", "subtitle")},
        ),
    ]
