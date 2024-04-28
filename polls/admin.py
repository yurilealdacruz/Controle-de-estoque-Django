from django.contrib import admin
from polls import models
from simple_history.admin import SimpleHistoryAdmin #pip install django-simple-history



#@admin.register(models.Estoque)
class EstoqueAdmin(SimpleHistoryAdmin):
    list_display = 'id', 'nome', 'estoque', 'retirada', 'sala_laboratorio'
    ordering = 'id',
    # list_filter = 'created_date',
    search_fields = 'id', 'nome',
    list_per_page = 20
    list_max_show_all = 200
    list_editable = 'retirada', 'sala_laboratorio',
    list_display_links = 'id', 'nome',
    history_list_display = ["retirada", 'sala_laboratorio']


admin.site.register(models.Estoque, EstoqueAdmin)

