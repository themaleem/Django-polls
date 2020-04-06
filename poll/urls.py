from django.urls import path,include
from poll import views
from rest_framework.routers import DefaultRouter

app_name="poll"

router=DefaultRouter()
router.register('api/polls',views.PollViewSet,)

urlpatterns = [
    path('',views.polls,name="polls"),
    path('add/',views.add_poll,name="add"),
    
    path('details/',include([
        path('<int:poll_id>/',views.poll_detail,name="details"),
        path('<int:poll_id>/vote/',views.poll_vote,name="vote")
    ])),
    
    path('edit/',include([
        path('poll/<int:poll_id>',views.edit_poll,name="edit_poll"),
        path('<int:poll_id>/choice/add/',views.add_choice,name="add_choice"),
        path('choice/<int:choice_id>',views.edit_choice,name="edit_choice"),
    ])),
    
    path('delete/',include([
        path('choice/<int:choice_id>',views.delete_choice,name="delete_choice"),
        path('poll/<int:poll_id>/',views.delete_poll,name="delete_poll"),
    ])),
    
    # API VIEWS starts
    path('api/',include([
        path('users',views.Users.as_view(),name="users"),
        path('login',views.LoginView.as_view(),name="api_login"),
        path('polls/', include([
            # path('',views.PollList2.as_view(),name="polls_list"),
            # path('<int:pk>',views.PollDetail2.as_view(),name="poll_detail"),
            path('<int:poll_pk>/choices',views.ChoiceList.as_view(),name="choice_list"),
            path('<int:poll_pk>/choices/<int:choice_pk>/vote',views.CreateVote.as_view(),name="create_vote"),
        ]))
    ]))
]

# adds url paths for polls list,create and details views
# first arg on register func tacks on to the app's default url i.e  127.0.0.1:8000/<app_name>/<first_arg>/
# and use base_name for path name ie poll-list,poll-details
urlpatterns+= router.urls 