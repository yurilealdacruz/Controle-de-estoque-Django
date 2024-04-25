from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from estoque.settings import MEDIA_URL, MEDIA_ROOT

from . import views

urlpatterns = [
    path('accounts/profile/', views.profile, name='profile'),
    path('cadastro_login/', views.cadastro_login, name='cadastro_login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("", views.index, name="index"),
    path("editar_estoque/<int:item_id>/", views.editar_estoque, name="editar_estoque"),
    path('buscar/', views.buscar_item, name='buscar_item'),  # URL para a view de busca
] + static(MEDIA_URL, document_root=MEDIA_ROOT)