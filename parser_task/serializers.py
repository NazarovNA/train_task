from rest_framework import serializers


def serializer_factory(mod):
    """ Создает серериализатор для указанной модели
    :param mod: модель для которой создается сериализатор
    :return AbstractSerializer: сериализатор для указанной модели
    """

    class AbstractSerializer(serializers.ModelSerializer):
        class Meta:
            model = mod
            fields = '__all__'

    return AbstractSerializer
