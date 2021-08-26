from django.db import models


class InstitutionType(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование типа учереждения')
    outside_id = models.CharField(max_length=20, verbose_name='ID источника')


class OrganizationType(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование типа организации')
    outside_id = models.CharField(max_length=20, verbose_name='ID источника')


class EgrulStatus(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование статуса ЕГРЮЛ')
    outside_id = models.CharField(max_length=20, verbose_name='ID источника')


class RubpnubpStatus(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование статуса РУБПНУБП')
    outside_id = models.CharField(max_length=20, verbose_name='ID источника')


class ChapterBK(models.Model):
    key = models.CharField(max_length=20, verbose_name='Код главы по БК')
    name = models.CharField(max_length=100, verbose_name='Наименование главы по БК')


class IndustrySpecificTyping(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование отраслевой типизации')
    outside_id = models.CharField(max_length=20, verbose_name='ID источника')


class BudgetLevel(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование уровня бюджета')
    outside_id = models.CharField(max_length=20, verbose_name='ID источника')