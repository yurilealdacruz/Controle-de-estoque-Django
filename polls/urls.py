from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from estoque.settings import MEDIA_URL, MEDIA_ROOT
from .views import adicionar_item_almo

from . import views

urlpatterns = [
    path("estoque/", views.index, name="index"),
    path("estoqueat/", views.estoqueat, name="estoqueat"), 
    path("estoquealmo/", views.estoquealmo, name="estoquealmo"), 
    path('cadastro_login/', views.cadastro_login, name='cadastro_login'),

    path('', views.profile, name='profile'),

    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

    path('loginat/', auth_views.LoginView.as_view(template_name='templatesat/registration/login.html'), name='loginat'),

    path('adicionar_estoque/<int:dado_id>/', views.adicionar_estoque, name='adicionar_estoque'),
    path('adicionar_estoque_at/<int:dado_id>/', views.adicionar_estoqueat, name='adicionar_estoque_at'),
    path('adicionar_estoque_almo/<int:dado_id>/', views.adicionar_estoquealmo, name='adicionar_estoque_almo'),

    path("editar_estoque/<int:item_id>/", views.editar_estoque, name="editar_estoque"),
    path("editar_estoqueat/<int:item_id>/", views.editar_estoqueat, name="editar_estoqueat"),
    path("retirar_estoquealmo/<int:item_id>/", views.retirar_estoquealmo, name="retirar_estoquealmo"),

    path('historico_retiradas/', views.historico_retiradas, name='historico_retiradas'),
    path('historico_retiradasat/', views.historico_retiradasAT, name='historico_retiradasat'),
    path('historico_retiradasalmo/', views.historico_retiradasAlmo, name='historico_retiradasalmo'),

    path('historico_retiradas_grafico/', views.historico_retiradas_grafico, name='historico_retiradas_grafico'),
    path('historico_retiradas_grafico_at/', views.historico_retiradas_grafico_at, name='historico_retiradas_grafico_at'),
    path('historico_retiradas_grafico_almo/', views.historico_retiradas_grafico_almo, name='historico_retiradas_grafico_almo'),

    path('buscar/', views.buscar_item, name='buscar_item'),  # URL para a view de busca
    path('buscarat/', views.buscar_itemAT, name='buscar_item_at'),  # URL para a view de busca
    path('buscaralmo/', views.buscar_itemAlmo, name='buscar_item_almo'),  # URL para a view de busca

    path('mostrar_grafico/', views.mostrar_grafico, name='mostrar_grafico'),
    path('logout/', views.realizar_logout, name='logout'),

    path('adicionar_item/', views.adicionar_item, name='adicionar_item'),
    path('adicionar_item_almo/', views.adicionar_item_almo, name='adicionar_item_almo'),
    path('adicionar_item_at/', views.adicionar_item_at, name='adicionar_item_at'),

    path('editar_estoquealmo/<int:item_id>/', views.editar_estoquealmo, name='editar_estoquealmo'),
    
] + static(MEDIA_URL, document_root=MEDIA_ROOT)