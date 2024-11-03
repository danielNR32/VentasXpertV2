# Generated by Django 5.1.1 on 2024-11-02 23:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios_permisos', '0005_producto_proveedor_alter_producto_categoria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='proveedor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Usuarios_permisos.proveedor'),
        ),
    ]
