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
            :param data: список словарей
            :return: new_data: входные данные с обновленными значениями ключей по таблице"""
            d = {}
            for (key, value) in data.items():
                if not value:
                    value = None
                if key in table_correspondences.keys():
                    d[table_correspondences[key]] = value
                else:
                    d[key] = value
            return d

        @staticmethod
        def data_api_processing(data, table_correspondences, model, code_field, foreign_key_fields):
            flag_without_connection = 0

            data = AbstractSerializer.renaming_keys(data, table_correspondences)

            set_objects = model.objects.all()

            obj = set_objects.filter(**{code_field: data[code_field]})
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

            ser = AbstractSerializer(data=data, instance=instance)
            if ser.is_valid():
                #print('save1')
                ser.save()
            else:
                # здесь убрать если ерроры чойсов
                for error_key in ser.errors.keys():
                    data.pop(error_key, None)
                ser = AbstractSerializer(data=data, instance=instance)
                if ser.is_valid():
                    #print('save2')
                    ser.save()
                else:

                    flag_without_connection = 0
                    print(ser.errors)
            if flag_without_connection:
                return 1
            else:
                return 0

        class Meta:
            model = mod
            fields = '__all__'

    return AbstractSerializer
