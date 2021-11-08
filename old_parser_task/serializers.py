import copy

from rest_framework import serializers


class AbstractSerializer(serializers.ModelSerializer):
    """
    Абстрактный сериализатор предназначенный для обеспечения загрузки и обновления справочников
    из внешнего API.
    С помощью данного класса обеспечивается: приведение данных json к формату модели, валидация данных и
    их сохранение.
    Для работы с данным классом используется функция serializer_factory, в которой происходит передача параметров
    в Meta класс.

    Параметры, передающиеся в Meta класс для обеспечения работы сериализатора по назначению:
        model: модель для которой создается сериализатор.
        foreign_key_fields: словарь соответствий полей модели при наличии связей с другой моделью:
    ключами являеются наименования полей json, котороые соответствуют полям модели, в которую заносятся даннные,
    значениями являются списки из трех значениий:
    0 - модель, к которой идет связь, 1 - наименование поля связной модели по которому строится фильтр,
    2 - наименование поля в json, которое соответствует полю в связной модели.
        code_field:  наиименование поля json в котором содержится внешний код записи, соотнеся который с полем
    модели можно найти можно найти данную запись если она существует.
        extra_kwargs: является таблией соответствий при различных наменованиях полей json и соответствующих им
    полей модели. Передается в формате {наименование поля json: 'source': наименование поля в модели}.
        fields: параметр fields является списком полей json для заполнения модели.
    """

    # флаг необходимый для выделения записи, у которой в связном поле не нашлось соответствий
    flag_without_connection = False

    def get_code_field(self):
        """
        Метод позволяющий получить наименование поля json и модели, содержащих код, по котороому можно найти
        данную запись json в модели.
        Наименование поля модели необходимо для наложения фильтра на модель.
        Наименование поля json необходимо для получения значения по которому накладывается фильтр.
        """
        json_code_field = copy.deepcopy(getattr(self.Meta, 'code_field', None))
        extra_kwargs = self.get_extra_kwargs()
        if json_code_field in extra_kwargs.keys():
            return json_code_field, extra_kwargs[json_code_field]['source']
        else:
            return json_code_field, json_code_field

    def get_model(self):
        """
        Метод предназначенный для получения модели, в которую заносятся данные.
        Необходим для наложения фильтра для заполнения связных полей.
        """
        return getattr(self.Meta, 'model', None)

    def get_foreign_key_fields(self):
        """
        Метод предназначенный для получения словаря, содержащего данные о связных полях модели.
        Необходим для заполнения связных полей моделей.
        """
        return getattr(self.Meta, 'foreign_key_fields', {})

    def to_internal_value(self, data):
        """
        Метод для поддержки десериализации для операций записи.
        В нем происходит: поиск записи, в лучае если она уже существует, занесение в связные поля необходимых
        данных и в случае отличия наименований полей входного параметра data с полями модели, происходит
        их переименование в соответствии с параметром extra_kwargs.
        """
        self.flag_without_connection = False

        # получение параметров из Meta класса
        json_code_field, model_code_field = self.get_code_field()
        foreign_key_fields = self.get_foreign_key_fields()
        model = self.get_model()

        # проверка на наличия такой записи в моделе
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
    #
    # class Meta:
    #     abstract = True


def serializer_factory(mod, list_fields=None, extra_keywords=None, field_code=None, dict_foreign_key_fields=None,
                       serializer=None):
    """
    Функция для создания сериализатора для указанной модели с занесением параметров в Meta класс.
    Используется для обеспечения загрузки и обновления справочников из внешнего API.
    Взаимодействие с данной фабрикой происходит через класс ParseRequest, из которого в данную функцию
    передаются параметры.

    :param serializer: сериализатор, в который заносятся параметры, по умолчанию AbstractSerializer.
    :param mod: модель для которой создается сериализатор.
    :param dict_foreign_key_fields: словарь соответствий полей модели при наличии связей с другой моделью:
    ключами являеются наименования полей json, котороые соответствуют полям модели, в которую заносятся даннные,
    значениями являются списки из трех значениий:
    0 - модель, к которой идет связь, 1 - наименование поля связной модели по которому строится фильтр,
    2 - наименование поля в json, которое соответствует полю в связной модели.
    :param field_code:  наиименование поля json в котором содержится внешний код записи, соотнеся который с полем
      модели можно найти можно найти данную запись если она существует.
    :param extra_keywords: является таблией соответствий при различных наменованиях полей json и соответствующих
    им полей модели. Передается в формате: {наименование поля json: 'source': наименование поля в модели}.
    :param list_fields: является списком полей json для заполнения модели.
    :return serializer: сериализатор с указанными параметрами для заданной модели.
    """
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
