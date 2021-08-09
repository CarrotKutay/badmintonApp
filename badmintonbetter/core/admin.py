from django.contrib import admin

# Register your models here.
from .models import Question, Choice, Discipline, EventDiscipline, Event, Sport, Player, Participant, Club

admin.site.site_header = 'BadmintonBetter Admin'
admin.site.site_title = 'BadmintonBetter Admin Area'
admin.site.index_title = 'Welcome to BadmintonBetter admin area'


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['question_text']}),
                 ('Date Information', {'fields': ['pub_date'], 'classes': ['collapse']}), ]
    inlines = [ChoiceInLine]


class PlayerAdmin(admin.ModelAdmin):
    list_display = ['id', 'lastname', 'firstname', 'dob']
    list_filter = ['lastname', 'firstname', 'dob']
    # define model data list ordering.
    ordering = ['id']


class ClubAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'name_abbrev']
    list_filter = ['id', 'name', 'name_abbrev']
    # define model data list ordering.
    ordering = ['id']


class SportAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'olympic']
    list_filter = ['id', 'name', 'olympic']
    # define model data list ordering.
    ordering = ['id']


class DisciplineAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sport', 'description', 'discipline_gender']
    list_filter = ['id', 'name', 'sport', 'description', 'discipline_gender']
    # define model data list ordering.
    ordering = ['id']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Club, ClubAdmin)
admin.site.register(Sport, SportAdmin)
admin.site.register(Discipline, DisciplineAdmin)