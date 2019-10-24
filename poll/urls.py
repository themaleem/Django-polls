from django.urls import path,include
from poll import views
app_name="poll"

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
        path('users',views.user_list,name="user_list"),
        path('poll/', include([
            path('',views.PollList2.as_view(),name="polls_list"),
            path('<int:pk>',views.PollDetail2.as_view(),name="poll_detail"),
            path('<int:poll_pk>/choices',views.ChoiceList.as_view(),name="choice_list"),
            path('<int:poll_pk>/choices/<int:choice_pk>/vote',views.CreateVote.as_view(),name="create_vote"),
        ]))
    ]))
]
