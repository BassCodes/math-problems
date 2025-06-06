# Generated by Django 5.2.1 on 2025-06-02 22:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("problems", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="DraftRef",
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
                ("draft_created", models.DateTimeField(auto_now=True)),
                ("draft_edited", models.DateTimeField(auto_now_add=True)),
                (
                    "draft_state",
                    models.CharField(
                        choices=[("DR", "Draft"), ("RE", "In Review")],
                        default="DR",
                        max_length=2,
                    ),
                ),
                ("forked_object_id", models.PositiveIntegerField(null=True)),
                (
                    "draft_owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "forked_content_type",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DraftSource",
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
                ("slug", models.SlugField(blank=True, null=True)),
                ("name", models.CharField(blank=True, max_length=128, null=True)),
                ("shortname", models.CharField(blank=True, max_length=40, null=True)),
                ("subtitle", models.CharField(blank=True, max_length=30, null=True)),
                (
                    "problem_count",
                    models.PositiveSmallIntegerField(blank=True, null=True),
                ),
                ("description", models.TextField(blank=True, null=True)),
                ("publish_date", models.DateField(blank=True, null=True)),
                ("url", models.URLField(blank=True, null=True)),
                (
                    "draft_ref",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="editor.draftref",
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="problems.sourcegroup",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DraftProblem",
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
                ("problem_text", models.TextField(blank=True, null=True)),
                ("has_answer", models.BooleanField(default=False)),
                ("answer_text", models.TextField(blank=True, null=True)),
                ("number", models.PositiveSmallIntegerField(blank=True, null=True)),
                (
                    "source",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="problems.source",
                    ),
                ),
                (
                    "draft_ref",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="editor.draftref",
                    ),
                ),
                (
                    "draft_source",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="editor.draftsource",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DraftSourceGroup",
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
                ("name", models.CharField(blank=True, max_length=128, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("url", models.URLField(blank=True, null=True)),
                (
                    "draft_ref",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="editor.draftref",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="draftsource",
            name="draft_parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="editor.draftsourcegroup",
            ),
        ),
        migrations.CreateModel(
            name="DraftSolution",
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
                    "draft_problem",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="editor.draftproblem",
                    ),
                ),
                (
                    "draft_ref",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="editor.draftref",
                    ),
                ),
                (
                    "problem",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="problems.problem",
                    ),
                ),
            ],
            options={
                "constraints": [
                    models.CheckConstraint(
                        condition=models.Q(
                            ("problem__isnull", False),
                            ("draft_problem__isnull", False),
                            _negated=True,
                        ),
                        name="draft_solution_no_problem_duplication",
                    )
                ],
            },
        ),
        migrations.AddConstraint(
            model_name="draftproblem",
            constraint=models.CheckConstraint(
                condition=models.Q(
                    ("source__isnull", False),
                    ("draft_source__isnull", False),
                    _negated=True,
                ),
                name="draft_problem_no_source_duplication",
            ),
        ),
        migrations.AddConstraint(
            model_name="draftsource",
            constraint=models.CheckConstraint(
                condition=models.Q(
                    ("parent__isnull", False),
                    ("draft_parent__isnull", False),
                    _negated=True,
                ),
                name="draft_source_no_parent_duplication",
            ),
        ),
    ]
