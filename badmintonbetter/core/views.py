from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from datetime import date
from django.contrib import messages

from .forms import PlayerCreateForm, DisciplineCreateForm, NewUserForm
from .models import Question, Choice, Player, Sport, Event, Discipline, Club
from .widgets import FengyuanChenDatePickerInput


# Create your views here.

# region ListViews


class PlayerListView(ListView):
    model = Player
    template_name = 'core/players/players.html'
    context_object_name = 'players'


class ClubListView(ListView):
    model = Club
    template_name = 'core/club/clubs.html'
    context_object_name = 'clubs'


class SportListView(ListView):
    model = Sport
    template_name = 'core/sports/sports.html'
    context_object_name = 'sports'


class EventListView(ListView):
    model = Event
    template_name = 'core/event/events.html'
    context_object_name = 'events'


class DisciplineListView(ListView):
    model = Discipline
    template_name = 'core/sports/disciplines.html'
    context_object_name = 'disciplines'


# endregion ListViews

# region FormViews (using model forms)

# region CreateViews

class PlayerCreateView(CreateView):
    model = Player
    form_class = PlayerCreateForm
    template_name = 'core/player/add/new_data.html'


class ClubCreateView(CreateView):
    model = Club
    template_name = 'core/club/add/new_data.html'
    fields = '__all__'


class SportCreateView(CreateView):
    model = Sport
    template_name = 'core/sport/add/new_data.html'
    fields = [
        'name', 'olympic'
    ]


class EventCreateView(CreateView):
    model = Event
    template_name = 'core/event/add/new_data.html'
    fields = [
        'name', 'date_begin', 'date_end'
    ]


class DisciplineCreateView(CreateView):
    model = Discipline
    form_class = DisciplineCreateForm
    template_name = 'core/discipline/add/new_data.html'


# endregion CreateViews

# region UpdateViews

# TODO: update views

# endregion UpdateViews

# region DeleteViews

# TODO deleteViews

# endregion DeleteViews

# region DetailViews

class PlayerDetailView(DetailView):
    model = Player

    pass


class ClubDetailView(DetailView):
    model = Club
    template_name = 'core/club/detail.html'

    pass


class SportDetailView(DetailView):
    model = Sport
    template_name = 'core/sport/detail.html'

    pass


class DisciplineDetailView(DetailView):
    model = Discipline
    template_name = 'core/discipline/detail.html'

    pass


# endregion DetailView

# endregion FormViews (using model forms)

# Get questions and display them
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'core/index.html', context=context)


def wip(request):
    return render(request, 'pages/wip.html')


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("core:index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="core/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("pages:index")


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("core:index")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm
    return render(request=request, template_name="core/register.html", context={"register_form": form})


# show specific question and choices
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'core/details.html', {'question': question})


# show results of specific question
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'core/details.html', {'question': question})


# bet for a specific question choice
def bet(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # reroute to display the question voting form
        return render(request, 'core/vote.html', {
            'question': question,
            'error-message': 'You didn\'t select a choice'
        })
    else:
        selected_choice.votes += 1

        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the 'Back' button
        return HttpResponseRedirect(reverse('core:results', args=(question_id,)))


def extend_information_view(request):
    return render(request, 'core/menu.html',
                  context={
                      'player_total': Player.objects.count(),
                      'event_total': Event.objects.count(),
                      'sport_total': Sport.objects.count(),
                      'discipline_total': Discipline.objects.count(),
                      'club_total': Club.objects.count()
                  })