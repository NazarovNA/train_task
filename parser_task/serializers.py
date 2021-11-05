from rest_framework import serializers
from rest_framework.fields import empty


def serializer_factory(mod, json_fields, extra_keywords):
    """ Создает серериализатор для указанной модели
    :param kwargs: параметр extra_kwargs в Meta
    :param json_fields: параметр fields в Meta
    :param mod: модель для которой создается сериализатор
    :return AbstractSerializer: сериализатор для указанной модели
    """

    class AbstractSerializer(serializers.ModelSerializer):

        def __init__(self, model, code_field, instance=None, data=empty, foreign_key_fields=None, **kwargs):
            super().__init__(instance=instance, data=empty, **kwargs)
            if data is not empty:
                self.initial_data = data
            self.model = model  # self.Meta.model
            self.code_field = code_field
            self.foreign_key_fields = foreign_key_fields
            self.flag_without_connection = False

        def to_internal_value(self, data):
            self.flag_without_connection = False

            obj = self.model.objects.filter(**{self.code_field: data[self.code_field]})
            if obj.exists():
                self.instance = obj[0]
            else:
                self.instance = None

            # занесение в связные поля модели объекты связных моделей
            if self.foreign_key_fields:
                for (key, value) in data.items():
                    if key not in self.foreign_key_fields.keys():
                        continue
                    connection = self.foreign_key_fields[key]
                    if data[connection[2]]:
                        connection_value = connection[0].objects.filter(**{connection[1]: data[connection[2]]})
                        if connection_value:
                            data[key] = connection_value[0].id
                        else:
                            data[key] = None
                            self.flag_without_connection = True
                    else:
                        data[key] = None

            new_data = {}
            for (key, value) in data.items():
                if value:
                    new_data[key] = value
                else:
                    new_data[key] = None
            new_data = super().to_internal_value(new_data)
            return new_data

        class Meta:
            model = mod
            fields = json_fields
            extra_kwargs = extra_keywords

    return AbstractSerializer
