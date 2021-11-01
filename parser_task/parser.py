import requests

from parser_task.serializers import serializer_factory


class ParseRequest:
    """Класс для загрузки или обновления данных справочников из внешнего api
    :param table_of_correspondences: словарь соответствий полей api и полей модели
    :param url: ссылка на внешнюю api
    :param model: модель которую необходимо обновить
    :param code_field: наиименование поля в котором содержится внешний код собственных код записи
    :param parent_field: наименование поля в котором содержится код родителя при
    иерархической структуре данных, в которой данное поле ссылается на объект модели
    """
    def __init__(self, table_of_correspondences, url, model, code_field, parent_field=None):
        self.table_of_correspondences = table_of_correspondences

        self.url = url
        self.model = model
        self.code_field = code_field
        self.parent_field = parent_field

        if self.parent_field:
            self.hierarchical_flag = True
        else:
            self.hierarchical_flag = False

    def download_external_api(self):
        """Получение набора данных из внешней api
        :return: data: список словарей, содержащих данные из api"""

        for_replace = None
        for u in self.url.split('&'):
            if 'pageNum' in u:
                for_replace = u

        data = []
        if for_replace:
            page = 1
            while True:
                base_url = self.url.replace(for_replace, f"pageNum={page}")
                print(base_url)
                r = requests.get(base_url, timeout=10)

                if (r.status_code == 200) and (r.json()['data']):
                    data += r.json()['data']
                    page += 1
                else:
                    break
            return data
        else:
            r = requests.get(self.url, timeout=10)
            if r.status_code == 200:
                data += r.json()['data']
            return data

    @staticmethod
    def ordered_set(data):
        """Метод исключения дубликатов из данных.
        :param data: входной список данных
        :return: out_list: входыные данные без дубликатов"""
        out_list = []
        for d in data:
            if not (d in out_list):
                out_list.append(d)
        return out_list

    def renaming_keys(self, data):
        """Метод приведения ключей данных к таблице соответствия
        :param data: список словарей
        :return: new_data: входные данные с обновленными значениями ключей по таблице"""
        new_data = []
        for i, d_json in enumerate(data):
            d = {}
            for (key, value) in d_json.items():
                if not value:
                    value = None
                if key in self.table_of_correspondences.keys():
                    d[self.table_of_correspondences[key]] = value
            new_data.append(d)
        return new_data

    def find_main_parents(self, data):
        """Метод поиска главных родителей для иерархических данных. Главным родителем принимается
         запись с кодом ссылающемся на себя, с отсутствующем родительским кодом и с нулевым кодом
        :param data: список словарей данных
        :return: main_parents: список, содержащий записи о главных родителях
        :return: parents_codes: список их собственных кодов"""

        main_parents = []
        parents_codes = []
        for i, d in enumerate(data):
            search_zero = False
            if d[self.parent_field]:
                search_zero = not bool(int(d[self.parent_field]))
            if (d[self.code_field] == d[self.parent_field]) or (not d[self.parent_field]) or search_zero:
                d[self.parent_field] = None
                main_parents.append(d)
                parents_codes.append(d[self.code_field])
        return main_parents, parents_codes

    def save_list_data(self, data):
        """Метод для сохранения списка данных в модель
        :param data: список словарей данных"""
        set_objects = self.model.objects.all()
        for d in data:
            obj = set_objects.filter(**{self.code_field: d[self.code_field]})
            if obj.exists():
                instance = obj[0]
            else:
                instance = None

            if self.hierarchical_flag:
                parent = set_objects.filter(**{self.code_field: d[self.parent_field]})
                if parent:
                    d[self.parent_field] = parent[0].id
                else:
                    d[self.parent_field] = None

            serializer = serializer_factory(self.model)
            ser = serializer(instance=instance, data=d)

            if ser.is_valid():
                ser.save()
            else:
                for error_key in ser.errors.keys():
                    d.pop(error_key, None)
                ser = serializer(instance=instance, data=d)
                if ser.is_valid():
                    ser.save()
                else:
                    print(ser.errors)

    def data_processing_and_save_in_model(self, data):
        """Метод для обработки данных, приведения к таблице соответствия с возможностью иерархической сортировки
        :param data: список словарей данных"""
        new_data = self.renaming_keys(data)
        new_data = self.ordered_set(new_data)

        if self.hierarchical_flag:
            parents, parents_codes = self.find_main_parents(new_data)

            hierarchical_sort = []
            new_parents_codes = parents_codes[:]
            list_use_codes = []
            while parents:
                hierarchical_sort.append(parents)
                parents = []
                parents_codes = new_parents_codes[:]
                list_use_codes += parents_codes
                new_parents_codes = []
                for d in new_data:
                    if (d[self.parent_field] in parents_codes) and (d[self.parent_field]):
                        parents.append(d)
                        new_parents_codes.append(d[self.code_field])

            without_parents = []
            for d in new_data:
                if not d[self.parent_field] in list_use_codes:
                    d[self.parent_field] = None
                    without_parents.append(d)
            if without_parents:
                hierarchical_sort.insert(0, without_parents)

            for list_data in hierarchical_sort:
                self.save_list_data(list_data)
        else:
            self.save_list_data(new_data)
