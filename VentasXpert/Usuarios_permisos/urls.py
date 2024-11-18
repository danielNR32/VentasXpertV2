from django.urls import path
from . import views

urlpatterns = [
    path('', views.usuarios_permisos_home, name='usuarios_permisos_home'),

    # URLs de usuarios
    path('usuarios/', views.users, name='usuarios'),
    path('usuarios/add/', views.add_user, name='add_user'),
    path('usuarios/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('usuarios/delete/<int:user_id>/', views.eliminar_usuario, name='delete_user'),
    path('usuarios/assign_role/<int:id_user>/', views.assign_role_to_user, name='assign_role_to_user'),
    # URLs de permisos
    path('permisos/', views.permissions, name='permisos'),
    path('permisos/add/', views.add_permission, name='add_permission'),
    path('permisos/edit/<int:permission_id>/', views.edit_permission, name='edit_permission'),
    path('permisos/delete/<int:permission_id>/', views.delete_permission, name='delete_permission'),

    # URLs de roles
    path('roles/', views.roles, name='roles'),
    path('roles/add/', views.add_role, name='add_role'),
    path('roles/edit/<int:role_id>/', views.edit_role, name='edit_role'),
    path('roles/delete/<int:role_id>/', views.delete_role, name='delete_role'),
    path('roles/get/<int:role_id>/', views.get_role_data, name='get_role_data'),

    # Logout
    path('logout/', views.logout_view, name='logout'),
]
