from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from estoque.settings import MEDIA_URL, MEDIA_ROOT

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('cadastro_login/', views.cadastro_login, name='cadastro_login'),
    path('accounts/profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path("editar_estoque/<int:item_id>/", views.editar_estoque, name="editar_estoque"),
    path('adicionar_estoque/<int:dado_id>/', views.adicionar_estoque, name='adicionar_estoque'),
    path('historico_retiradas/', views.historico_retiradas, name='historico_retiradas'),
    path('buscar/', views.buscar_item, name='buscar_item'),  # URL para a view de busca
] + static(MEDIA_URL, document_root=MEDIA_ROOT)