import copy

from rest_framework import serializers


class ParseApiSerializer(serializers.ModelSerializer):
    """
    Потомок ModelSerializer, который для связей вместо первичного ключа позволяет использовать любые
    другие поля связной модели, позволяющие определить уникальный элемент. Так же позволяет производить замену (меппинг)
    значений полей по заданным соответствиям. Расширенные возможности реализованны только для десериализаии.

    Расширенные возможности описываются через опцию:
    extend_extra_kwargs: использование аналогично extra_kwargs.
    {'Поле json':
        {
        'foreign_model': 'Модель в которой ищем (на которую ссылаемся)',
        'foreign_model_lookup_field':'Поле по которому ищем',
        'values_map': {'Какое значение': 'На какое заменяем'}
        }
    }
    """

    def to_internal_value(self, data):
        """
        Переопределение метода родителя, реализующего особенности десериализации для данного класса.
        """
        model = copy.deepcopy(getattr(self.Meta, 'model', None))
        extra_kwargs = self.Meta.extra_kwargs
        extend_extra_kwargs = self.Meta.extend_extra_kwargs

        for (json_field, json_value) in data.items():
            if json_value == '':
                data[json_field] = None
                continue
            if json_field not in extend_extra_kwargs.keys():
                continue
            value_extra_kwargs = extra_kwargs.get(json_field)
            value_extend_extra_kwargs = extend_extra_kwargs[json_field]

            # Меппинг значений поля
            try:
                values_map = value_extend_extra_kwargs['values_map']
                if json_value in values_map.keys():
                    data[json_field] = values_map[json_value]
                    json_value = data[json_field]
            except KeyError:
                pass
            if json_value is None:
                continue
            try:
                foreign_model_lookup_field = value_extend_extra_kwargs['foreign_model_lookup_field']
            except KeyError:
                continue
            foreign_model = value_extend_extra_kwargs['foreign_model']
            try:
                model_field = value_extra_kwargs['source']
            except (KeyError, TypeError):
                model_field = json_field
            try:
                queryset = foreign_model.objects.get(**{foreign_model_lookup_field: json_value})
                if model == foreign_model and model_field == foreign_model_lookup_field:
                    self.instance = queryset
                else:
                    data[json_field] = queryset.pk
            except:
                if not(model == foreign_model and model_field == foreign_model_lookup_field):
                    data[json_field] = -1

        return super().to_internal_value(data)
