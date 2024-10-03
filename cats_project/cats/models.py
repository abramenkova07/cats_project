from django.contrib.auth import get_user_model
from django.core.validators import (MaxValueValidator,
                                    MinValueValidator)
from django.db import models

from .constants import (COLOR_CHOICES,
                        MAX_LENGTH, MAX_SCORE, MIN_SCORE)

User = get_user_model()


class Breed(models.Model):
    name = models.CharField(
        'Порода',
        max_length=MAX_LENGTH,
        unique=True,
        blank=False
    )
    slug = models.SlugField(
        'Слаг',
        max_length=MAX_LENGTH,
        unique=True,
        blank=False
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'порода'
        verbose_name_plural = 'породы'

    def __str__(self):
        return self.name


class Cat(models.Model):
    name = models.CharField(
        'Кличка',
        max_length=MAX_LENGTH,
        blank=False
    )
    color = models.CharField(
        'Цвет',
        max_length=MAX_LENGTH,
        choices=COLOR_CHOICES
    )
    age = models.PositiveSmallIntegerField(
        'Полный возраст в месяцах',
        blank=False,
        validators=[MinValueValidator(MIN_SCORE)]
    )
    description = models.TextField(
        'Описание',
        blank=True
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Владелец'
    )
    breed = models.ForeignKey(
        Breed,
        on_delete=models.CASCADE,
        verbose_name='Порода'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'котенок'
        verbose_name_plural = 'котята'
        default_related_name = 'cats'
        constraints = [
            models.UniqueConstraint(
                fields=['owner', 'name'],
                name='unique_owner_cat_name'
            )
        ]

    def __str__(self):
        return f'{self.name} - {self.owner}'


class Score(models.Model):
    cat = models.ForeignKey(
        Cat,
        on_delete=models.CASCADE,
        verbose_name='Котенок'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(MIN_SCORE),
                    MaxValueValidator(MAX_SCORE)]
    )

    class Meta:
        ordering = ('cat__name',)
        verbose_name = 'оценка'
        verbose_name_plural = 'оценки'
        default_related_name = 'scores'
        constraints = [
            models.UniqueConstraint(
                fields=['cat', 'owner'],
                name='unique_user_cat'
            )
        ]
