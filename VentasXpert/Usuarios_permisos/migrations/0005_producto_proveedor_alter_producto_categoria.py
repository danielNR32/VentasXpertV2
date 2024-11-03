# Generated by Django 5.1.1 on 2024-11-02 21:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios_permisos', '0004_alter_producto_options_alter_producto_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='proveedor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Usuarios_permisos.proveedor'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Usuarios_permisos.categoria'),
        ),
    ]
