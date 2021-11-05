from rest_framework import serializers


def serializer_factory(mod):
    """ Создает серериализатор для указанной модели
    :param mod: модель для которой создается сериализатор
    :return AbstractSerializer: сериализатор для указанной модели
    """

    class AbstractSerializer(serializers.ModelSerializer):

        @staticmethod
        def renaming_keys(data, table_correspondences):
            """Метод приведения ключей данных к таблице соответствия
            :param table_correspondences: словарь соответствий полей api и полей модели
            :param data: словарь
            :return: new_data: входной словарь с обновленными значениями ключей по таблице"""
            d = {}
            for (key, value) in data.items():
                if not value:
                    value = None
                if key in table_correspondences.keys():
                    d[table_correspondences[key]] = value
                else:
                    d[key] = value
            return d

        @classmethod
        def data_api_processing(cls, data, table_correspondences, model, code_field, foreign_key_fields):
            flag_without_connection = 0

            data = cls.renaming_keys(data, table_correspondences)

            obj = model.objects.filter(**{code_field: data[code_field]})
            if obj.exists():
                instance = obj[0]
            else:
                instance = None

            # занесение в связные поля модели объекты связных моделей
            if foreign_key_fields:
                for (key, value) in data.items():
                    if key in foreign_key_fields.keys():
                        connection = foreign_key_fields[key]
                        if data[connection[2]]:
                            connection_value = connection[0].objects.filter(**{connection[1]: data[connection[2]]})
                            if connection_value:
                                data[key] = connection_value[0].id
                            else:
                                data[key] = None
                                flag_without_connection = 1
                        else:
                            data[key] = None

            ser = cls(data=data, instance=instance)
            if ser.is_valid():
                ser.save()
            else:
                # clearning error fields
                for error_key in ser.errors.keys():
                    data.pop(error_key, None)
                ser = cls(data=data, instance=instance)
                if ser.is_valid():
                    ser.save()
                else:
                    flag_without_connection = 0
                    print(ser.errors)

            return flag_without_connection

        class Meta:
            model = mod
            fields = '__all__'

    return AbstractSerializer
