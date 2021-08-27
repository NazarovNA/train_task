from django.db import models, transaction
from django.conf import settings

from dictionaries import models as md
from pickle import load


class Organization(models.Model):
    """Модель описывающая признаки организации
    -
    -
    -
    -
    -
    -
    """

    institution_key = models.IntegerField(unique=True, verbose_name='Код учереждения')
    name = models.TextField(verbose_name='Наименование организации')
    inn = models.CharField(max_length=10, unique=True, verbose_name='ИНН организации')
    kpp = models.CharField(max_length=9, verbose_name='КПП организации')

    institution_type = models.ForeignKey(md.InstitutionType, on_delete=models.DO_NOTHING)
    organization_type = models.ForeignKey(md.OrganizationType, on_delete=models.DO_NOTHING)
    egrul_status = models.ForeignKey(md.EgrulStatus, on_delete=models.DO_NOTHING)
    rubpnubp_status = models.ForeignKey(md.RubpnubpStatus, on_delete=models.DO_NOTHING)
    chapter_bk = models.ForeignKey(md.ChapterBK, on_delete=models.DO_NOTHING)
    industry_specific_typing = models.ForeignKey(md.IndustrySpecificTyping, on_delete=models.DO_NOTHING)
    budget_level = models.ForeignKey(md.BudgetLevel, on_delete=models.DO_NOTHING)

    @classmethod
    def load_from_file(cls):
        with open('C:/Users/strai/Snake/trait_django', 'rb') as f:
            data = load(f)

        with transaction.atomic():
            for m, d in enumerate(data):
                print(m)
                institutiontype, _ = md.InstitutionType.objects.get_or_create(name=d['Тип учреждения'],
                                                                           outside_id='')
                organizationtype, _ = md.OrganizationType.objects.get_or_create(name=d['Тип организации'],
                                                                             outside_id='')
                egrulstatus, _ = md.EgrulStatus.objects.get_or_create(name=d['Статус ЕГРЮЛ'],
                                                                   outside_id='')
                rubpnubpstatus, _ = md.RubpnubpStatus.objects.get_or_create(name=d['Статус РУБПНУБП'],
                                                                         outside_id='')
                chapterbk, _ = md.ChapterBK.objects.get_or_create(name=d['Наименование главы по БК'],
                                                               key=d['Код главы по БК'])
                industryspecifictyping, _ = md.IndustrySpecificTyping.objects.get_or_create(
                    name=d['Отраслевая типизация'],
                    outside_id='')
                budgetlevel, _ = md.BudgetLevel.objects.get_or_create(name=d['Уровень бюджета'],
                                                                   outside_id='')

                cls.objects.get_or_create(institution_key=d['Код учреждения'],
                                          name=d['Наименование организации'],
                                          inn=d['ИНН'],
                                          kpp=d['КПП'],

                                          institution_type=institutiontype,
                                          organization_type=organizationtype,
                                          egrul_status=egrulstatus,
                                          rubpnubp_status=rubpnubpstatus,
                                          chapter_bk=chapterbk,
                                          industry_specific_typing=industryspecifictyping,
                                          budget_level=budgetlevel)
