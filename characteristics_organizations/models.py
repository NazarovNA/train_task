from django.db import models

from dictionaries import models as md


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


