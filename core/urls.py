from django.contrib import admin
from django.urls import path, include
from app.views import CategoriaViewSet, TarefaViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("tarefa", TarefaViewSet, basename="tarefa")
router.register("categoria", CategoriaViewSet, basename="categoria")

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include(router.urls))
]
