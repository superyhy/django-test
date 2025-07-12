from django.urls import path

from stud_project import subject, login

urlpatterns = [
    path('create', subject.subject_add),
    path('query', subject.subject_query),
    path('delete', subject.subject_delete),
    path('update',subject.subject_update),
    path('login',login.custom_token_view)
]
