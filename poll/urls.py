from django.urls import path
from poll import views
app_name="poll"

urlpatterns = [
    path('',views.polls,name="polls"),
    path('add/',views.add_poll,name="add"),
    path('delete/poll/<int:poll_id>/',views.delete_poll,name="delete_poll"),
    path('edit/poll/<int:poll_id>',views.edit_poll,name="edit_poll"),
    path('details/<int:poll_id>/',views.poll_detail,name="details"),
    path('edit/<int:poll_id>/choice/add/',views.add_choice,name="add_choice"),
    path('edit/choice/<int:choice_id>',views.edit_choice,name="edit_choice"),
    path('delete/choice/<int:choice_id>',views.delete_choice,name="delete_choice"),
    path('details/<int:poll_id>/vote/',views.poll_vote,name="vote"),
    
    # API VIEWS starts
    path('api/user/',views.user_list,name="user_list"),
    path('api/polls',views.PollList2.as_view(),name="polls_list"),
    path('api/poll/<int:pk>',views.PollDetail2.as_view(),name="poll_detail"),
    path('api/poll/<int:poll_pk>/choices/',views.ChoiceList.as_view(),name="choice_list"),
    path('api/poll/<int:poll_pk>/choices/<int:choice_pk>/vote',views.CreateVote.as_view(),name="create_vote"),
]
