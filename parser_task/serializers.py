import copy

from rest_framework import serializers


class ParseApiSerializer(serializers.ModelSerializer):
    """
    Сериализатор предназначенный для обеспечения загрузки и обновления справочников из API.

    При работе с данным классом в Meta класс необходимо занести дополнительный параметр
        extend_extra_kwargs: словарь - дополнение к extra_kwargs. Ключами являеются наименования полей json для
    занесения модели. Значениями являются словари, которые запоняются по шаблону
    {'Поле json': {'foreign_model': 'Модель в которой ищем', 'foreign_model_lookup_field':'Поле по которому ищем'}}
    Для указания поля pk в json с внешним кодом записи, по которому можно найти запись в модели необходимо в
    параметр 'foreign_model_lookup_field' занести наименование поля pk в json
    """

    def get_combining_extra_kwargs(self):
        """
        Метод позволяет получить параметр extra_kwargs объединенный с extend_extra_kwargs
        """
        extra_kwargs = self.get_extra_kwargs()
        extend_extra_kwargs = copy.deepcopy(getattr(self.Meta, 'extend_extra_kwargs', None))

        if not extra_kwargs:
            return extend_extra_kwargs

        for field in extra_kwargs.keys():
            if field in extend_extra_kwargs.keys():
                extra_kwargs[field].update(extend_extra_kwargs[field])
                del extend_extra_kwargs[field]
        extra_kwargs.update(extend_extra_kwargs)

        return extra_kwargs

    def to_internal_value(self, data):
        """
        Метод для поддержки десериализации для операций записи.
        В нем происходит: поиск записи в случае, если она уже существует, занесение в связные поля необходимых
        данных и в случае отличия наименований полей входного параметра data с полями модели, происходит
        их переименование в соответствии с extra_kwargs.
        """
        # получение параметров из Meta класса
        extra_kwargs = self.get_combining_extra_kwargs()
        model = copy.deepcopy(getattr(self.Meta, 'model', None))

        for key, value in extra_kwargs.items():
            if key in value.values():
                if 'source' in value:
                    json_code_field = key
                    model_code_field = value['source']
                else:
                    json_code_field = key
                    model_code_field = key

        # проверка на наличие такой записи в моделе
        obj = model.objects.filter(**{model_code_field: data[json_code_field]})
        if obj.exists():
            self.instance = obj[0]
        else:
            self.instance = None

        # занесение в связные поля модели id записей связных моделей
        for (key, value) in data.items():
            if not value:
                data[key] = None
                continue
            if key not in extra_kwargs.keys():
                continue
            if key in extra_kwargs[key].values():
                continue
            connection = extra_kwargs[key]
            if 'foreign_model' not in connection:
                continue
            # наложение фильтра на связную модель для определения id записи
            connection_value = connection['foreign_model'].objects.filter(
                **{connection['foreign_model_lookup_field']: data[key]})
            if connection_value:
                data[key] = connection_value[0].id
            else:
                data[key] = -1

        data = super().to_internal_value(data)

        return data
