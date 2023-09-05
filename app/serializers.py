from rest_framework import serializers
from app.models import Categoria, Tarefa


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"


class TarefaSerializer(serializers.ModelSerializer):
    categoria = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Categoria.objects.all()
    )

    class Meta:
        model = Tarefa
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Substituir os IDs das categorias pelos objetos serializados das categorias
        data["categoria"] = CategoriaSerializer(
            instance.categoria.all(), many=True
        ).data

        return data
