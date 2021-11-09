import copy

from rest_framework import serializers


class AbstractSerializer(serializers.ModelSerializer):
    """
    Сериализатор предназначенный для обеспечения загрузки и обновления справочников из API.

    Параметры, передающиеся в Meta класс для обеспечения работы сериализатора по назначению:
        model: модель для которой создается сериализатор.
        foreign_key_fields: словарь соответствий полей модели при наличии связей с другой моделью:
    ключами являеются наименования полей json, котороые соответствуют полям модели, значениями являются списки
    из трех значениий: 0 - модель, к которой идет связь, 1 - наименование поля связной модели по которому
    строится фильтр, 2 - наименование поля в json, которое соответствует полю в связной модели.
        code_field:  наиименование поля json в котором содержится внешний код записи, соотнеся который с полем
    модели можно найти можно найти данную запись если она существует.
        fields: является списком полей json для заполнения модели.
        extra_kwargs: является таблией соответствий при различных наменованиях полей json и соответствующих им
    полей модели. Передается в формате {наименование поля json: 'source': наименование поля в модели}.
    """
    # флаг необходимый для выделения записи, у которой в связном поле не нашлось соответствий
    flag_without_connection = False

    def get_code_field(self):
        """
        Метод позволяет получить наименование полей json и модели, содержащих код, по котороому можно найти
        данную запись json в модели.
        Наименование поля модели необходимо для наложения фильтра.
        Наименование поля json необходимо для получения значения, по которому накладывается фильтр.
        """
        json_code_field = copy.deepcopy(getattr(self.Meta, 'code_field', None))
        extra_kwargs = self.get_extra_kwargs()
        if json_code_field in extra_kwargs.keys():
            return json_code_field, extra_kwargs[json_code_field]['source']
        else:
            return json_code_field, json_code_field

    def to_internal_value(self, data):
        """
        Метод для поддержки десериализации для операций записи.
        В нем происходит: поиск записи в случае, если она уже существует, занесение в связные поля необходимых
        данных и в случае отличия наименований полей входного параметра data с полями модели, происходит
        их переименование в соответствии с extra_kwargs.
        """
        self.flag_without_connection = False

        # получение параметров из Meta класса
        json_code_field, model_code_field = self.get_code_field()
        foreign_key_fields = copy.deepcopy(getattr(self.Meta, 'foreign_key_fields', {}))
        model = copy.deepcopy(getattr(self.Meta, 'model', None))

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
            if foreign_key_fields is None:
                continue
            if key not in foreign_key_fields.keys():
                continue
            connection = foreign_key_fields[key]
            if data[connection[2]]:
                # наложение фильтра на связную модель для определения id записи
                connection_value = connection[0].objects.filter(**{connection[1]: data[connection[2]]})
                if connection_value:
                    data[key] = connection_value[0].id
                else:
                    data[key] = None
                    # флаг True ставится в случае отсутствия элемента в связной модели
                    self.flag_without_connection = True
            else:
                data[key] = None
        data = super().to_internal_value(data)

        return data
