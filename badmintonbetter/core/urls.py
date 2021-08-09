from django.urls import path

from .views import index, PlayerListView, SportListView, extend_information_view, \
    EventCreateView, DisciplineCreateView, SportCreateView, PlayerCreateView, bet, results, detail, \
    EventListView, DisciplineListView, ClubListView, ClubCreateView, ClubDetailView, SportDetailView, \
    DisciplineDetailView, wip, login_request, register_request, logout_request

app_name = 'core'
urlpatterns = [
    path('', index, name='index'),
    path('player-list', PlayerListView.as_view(), name='player-list'),
    path('sport-list', SportListView.as_view(), name='sport-list'),
    path('discipline-list', DisciplineListView.as_view(), name='discipline-list'),
    path('event-list', EventListView.as_view(), name='event-list'),
    path('club-list', ClubListView.as_view(), name='club-list'),
    path('<int:question_id>/', detail, name='detail'),
    path('club/detail/<int:pk>/', ClubDetailView.as_view(), name='club-detail'),
    path('sport/detail/<int:pk>/', SportDetailView.as_view(), name='sport-detail'),
    path('discipline/detail/<int:pk>/', DisciplineDetailView.as_view(), name='discipline_detail'),
    path('<int:question_id>/results', results, name='results'),
    path('<int:question_id>/bet', bet, name='bet'),
    path('club/add', ClubCreateView.as_view(), name='add-club'),
    path('player/add', PlayerCreateView.as_view(), name='add-player'),
    path('sport/add', SportCreateView.as_view(), name='add-sport'),
    path('discipline/add', DisciplineCreateView.as_view(), name='add-discipline'),
    path('event/add', EventCreateView.as_view(), name='add-event'),
    path('menu.html', extend_information_view, name='extend_menu'),

    ### user management
    path('register', register_request, name='register'),
    path('login', login_request, name='login'),
    path('logout', logout_request, name='logout')
]