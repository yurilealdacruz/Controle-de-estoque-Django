from django.urls import path
from django.conf.urls.static import static
from estoque.settings import MEDIA_URL, MEDIA_ROOT

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('buscar/', views.buscar_item, name='buscar_item'),  # URL para a view de busca
] + static(MEDIA_URL, document_root=MEDIA_ROOT)