# Generated by Django 4.1.5 on 2023-02-02 18:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_comment"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment",
            options={"ordering": ["-id"]},
        ),
    ]
