from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from app.serializers import CategoriaSerializer, TarefaSerializer
from app.models import Categoria, Tarefa
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.utils import timezone


# Create your views here.
class CategoriaViewSet(ViewSet):
    def list(self, request, *args, **kwargs):
        categorias = Categoria.objects.all().order_by("name")
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = CategoriaSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "sucesso", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"message": "Alguns campos estão faltando"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class TarefaViewSet(ViewSet):
    def check_expired(self):
        for tarefa in Tarefa.objects.all():
            if tarefa.data_entrega < timezone.now():
                tarefa.expired = True
                tarefa.save()

    def create(self, request, *args, **kwargs):
        categorias_names = request.data.get("categoria", [])
        if not categorias_names:
            return Response(
                {"message": "Categoria não fornecida"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        categorias_ids = []
        for categoria_name in categorias_names:
            categoria, created = Categoria.objects.get_or_create(name=categoria_name)
            categorias_ids.append(categoria.id)

        new_data = request.data.copy()
        new_data["categoria"] = categorias_ids

        serializer = TarefaSerializer(data=new_data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "sucesso", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def list(self, request, *args, **kwargs):
        self.check_expired()
        tarefa = Tarefa.objects.all().order_by("name")
        serializer = TarefaSerializer(tarefa, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            self.check_expired()
            tarefa = Tarefa.objects.get(pk=pk)
            serializer = TarefaSerializer(tarefa)
            return Response(serializer.data)
        except Tarefa.DoesNotExist:
            return Response(
                {"message": "Tarefa não encontrada"}, status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=["post"], url_path="toggle_finished")
    def toggle_finished(self, request, pk=None):
        try:
            tarefa = Tarefa.objects.get(pk=pk)
            tarefa.finalizada = not tarefa.finalizada
            tarefa.save()
            serializer = TarefaSerializer(tarefa)
            return Response(
                {"message": "Tarefa atualizada", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Tarefa.DoesNotExist:
            return Response(
                {"message": "Tarefa não encontrada"}, status=status.HTTP_404_NOT_FOUND
            )

    @action(
        detail=False, methods=["get"], url_path="categoria/(?P<categoria_escolhida>\w+)"
    )
    def get_by_category(self, request, categoria_escolhida):
        categoria = Categoria.objects.get(name=categoria_escolhida)
        tarefas = Tarefa.objects.filter(categoria=categoria)
        serializer = TarefaSerializer(tarefas, many=True)
        return Response(serializer.data)
