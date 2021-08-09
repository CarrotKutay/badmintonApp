from django.db import models
from django.db.models import DateField
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import datetime


# Create your models here.


class Question(models.Model):
    # id automatically created (PR)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    total_votes = models.IntegerField(default=0)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    # id automatically created (PR)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Event(models.Model):
    name = models.CharField(max_length=200, null=False)
    date_begin = models.DateField(null=False)
    date_end = models.DateField(null=False)

    def get_duration(self) -> int:
        """
        Get the duration of the event in days
        :return: number of days as an integer
        """
        return self.date_end.date() - self.date_begin.date()

    def is_happening(self) -> bool:
        """
        Find out if the event is currently happening or not. Will compare if the current date
        is past the end date of the event.
        :return: True if the end date is larger then the current date
        """
        return (datetime.now().date() - self.date_end.date()) >= 0

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk': self.pk})


class Sport(models.Model):
    # id automatically created (PR)
    name = models.CharField(max_length=200, unique=True)
    olympic = models.BooleanField(null=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('sport-detail', kwargs={'pk': self.pk})


class Discipline(models.Model):
    # id automatically created (PR)

    class DisciplineGender(models.TextChoices):
        WOMEN = 'W', _('Women')
        MEN = 'M', _('Men')
        MIXED = 'MXD', _('Mixed')

    name = models.CharField(max_length=200, unique=True)
    sport = models.ForeignKey(Sport, related_name='disciplines', on_delete=models.CASCADE)
    discipline_gender = models.CharField(
        max_length=3,
        choices=DisciplineGender.choices,
        default=DisciplineGender.WOMEN
    )
    description = models.TextField(max_length=1000, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('core:discipline_detail', kwargs={'pk': self.pk})


class Participant(models.Model):
    # id automatically created (PR)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, null=True)
    date_since = models.DateField(null=True)
    # TODO: include ranking -> world ranking / korean high ranking


class EventDiscipline(models.Model):
    """
    Class to connect the disciplines played during a Event with the Event required.
    Relation: <event> many <-> many <discipline>
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)


class Club(models.Model):
    name = models.CharField(max_length=200, verbose_name='Club name', null=False, unique=True)
    name_abbrev = models.CharField(max_length=10, verbose_name='Abbreviation')

    def get_absolute_url(self):
        return reverse('club-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name_abbrev

    pass


class Player(models.Model):
    # id automatically created (PR)

    # personal information
    class Gender(models.TextChoices):
        FEMALE = 'F', _('female')
        MALE = 'M', _('male')
        OTHER = 'O', _('other')

    firstname = models.CharField(max_length=200, null=False)
    lastname = models.CharField(max_length=200, null=False)
    dob: DateField = models.DateField(verbose_name='Date of birth', null=False, default=timezone.now)
    gender = models.CharField(
        max_length=3,
        choices=Gender.choices,
        default=Gender.OTHER
    )

    def is_other(self) -> bool:
        return self.gender is self.Gender.OTHER

    def is_female(self) -> bool:
        return self.gender is self.Gender.FEMALE

    def is_male(self) -> bool:
        return self.gender is self.Gender.MALE

    def age(self) -> int:
        return (datetime.now - self.dob).year

    def name(self) -> str:
        return self.__str__()

    # professional information
    disciplines = models.ManyToManyField(Discipline, related_name='participants')
    club = models.ForeignKey(Club, related_name='members', on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f'{self.firstname}, {self.lastname}'

    def get_absolute_url(self):
        return reverse('player-detail', kwargs={'pk': self.pk})


class League(models.Model):

    class LeagueTyp(models.TextChoices):
        INTERNATIONAL = 'I', _('international')
        CONTINENTAL = 'C', _('continental')
        NATIONAL = 'N', _('national')

        pass

    name = models.CharField(max_length=200, null=False, default='name')
    type = models.CharField(
        max_length=3,
        choices=LeagueTyp.choices,
        default=LeagueTyp.NATIONAL
    )
    league_pos = models.IntegerField(verbose_name='League Standing', unique=False, null=True,
                                     help_text='Standing of the league compared to other leagues of its type, '
                                               'e.g. 1st national league, 2nd national league, ...')

    pass


class Ranking(models.Model):
    update = models.DateTimeField(verbose_name='last update', default=timezone.now)
    league = models.ForeignKey(League, on_delete=models.SET_NULL, null=True)

    pass


class Team(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='clubs', null=False)
    ranking = models.ForeignKey(Ranking, on_delete=models.CASCADE, null=True)

    pass