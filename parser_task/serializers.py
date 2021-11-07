from rest_framework import serializers


class AbstractSerializer(serializers.ModelSerializer):
    flag_without_connection = False

    def to_internal_value(self, data):
        self.flag_without_connection = False

        obj = self.Meta.model.objects.filter(**{self.Meta.code_field: data[self.Meta.code_field]})
        if obj.exists():
            self.instance = obj[0]
        else:
            self.instance = None

        # занесение в связные поля модели объекты связных моделей
        for (key, value) in data.items():
            if not value:
                data[key] = None
            if self.Meta.foreign_key_fields is None:
                continue
            if key not in self.Meta.foreign_key_fields.keys():
                continue
            connection = self.Meta.foreign_key_fields[key]
            if data[connection[2]]:
                connection_value = connection[0].objects.filter(**{connection[1]: data[connection[2]]})
                if connection_value:
                    data[key] = connection_value[0].id
                else:
                    data[key] = None
                    self.flag_without_connection = True
            else:
                data[key] = None

        data = super().to_internal_value(data)

        return data

    class Meta:
        model = None
        fields = None
        extra_kwargs = None
        code_field = None
        foreign_key_fields = None


def serializer_factory(mod, list_fields=None, extra_keywords=None, field_code=None, dict_foreign_key_fields=None,
                       serializer=None):
    """ Создает серериализатор для указанной модели
    :param serializer:
    :param mod: модель для которой создается сериализатор
    :param dict_foreign_key_fields:
    :param field_code:
    :param extra_keywords:
    :param list_fields:
    :return serializer: сериализатор для указанной модели
    """
    # if serializer is not None:
    #     if not issubclass(serializer, AbstractSerializer):
    #         serializer = AbstractSerializer
    if serializer is None:
        serializer = AbstractSerializer

    class Meta:
        model = mod
        if list_fields is not None:
            fields = list_fields
        else:
            fields = '__all__'
        if extra_keywords is not None:
            extra_kwargs = extra_keywords
        code_field = field_code
        foreign_key_fields = dict_foreign_key_fields
    serializer.Meta = Meta

    return serializer
