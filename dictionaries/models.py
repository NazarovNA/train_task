from django.db import models


class InstitutionType(models.Model):
    """Модель описывающая тип учереждения
        name - Наименование типа учереждения
        outside_id - ID источника
        """
    name = models.CharField(max_length=100, verbose_name='Наименование типа учереждения')
    outside_id = models.CharField(max_length=20, verbose_name='ID источника')


class OrganizationType(models.Model):
    """Модель описывающая тип организации
        name - Наименование типа организации
        outside_id - ID источника
        """
    name = models.CharField(max_length=100, verbose_name='Наименование типа организации')
    outside_id = models.CharField(max_length=20, verbose_name='ID источника')


class EgrulStatus(models.Model):
    """Модель описывающая статус ЕГРЮЛ
        name - Наименование статуса ЕГРЮЛ
        outside_id - ID источника
        """
    name = models.CharField(max_length=200, verbose_name='Наименование статуса ЕГРЮЛ')
    outside_id = models.CharField(max_length=20, verbose_name='ID источника')


class RubpnubpStatus(models.Model):
    """Модель описывающая статус РУБПНУБП
        name - Наименование статуса РУБПНУБП
        outside_id - ID источника
        """
    name = models.CharField(max_length=200, verbose_name='Наименование статуса РУБПНУБП')
    outside_id = models.CharField(max_length=20, verbose_name='ID источника')


class ChapterBK(models.Model):
    """Модель описывающая основные совйства главы по БК
        key - Код главы по БК
        name - Наименование главы по БК
        outside_id - ID источника
        """
    key = models.CharField(max_length=20, verbose_name='Код главы по БК')
    name = models.CharField(max_length=200, verbose_name='Наименование главы по БК')


class IndustrySpecificTyping(models.Model):
    """Модель описывающая отраслевую типизацию
        name - Наименование отраслевой типизации
        outside_id - ID источника
        """
    name = models.CharField(max_length=200, verbose_name='Наименование отраслевой типизации')
    outside_id = models.CharField(max_length=20, verbose_name='ID источника')


class BudgetLevel(models.Model):
    """Модель описывающая уровнь бюджета
        name - Наименование уровня бюджета
        outside_id - ID источника
        """
    name = models.CharField(max_length=200, verbose_name='Наименование уровня бюджета')
    outside_id = models.CharField(max_length=20, verbose_name='ID источника')