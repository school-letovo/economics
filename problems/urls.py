from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('assign', views.assign, name='assign'),
    path('submit', views.submit, name='submit'),
    path('save_verdict', views.save_verdict, name='save_verdict'),
    path('test', views.test, name='test'),
    path('source_list', views.source_list, name='source_list'),
    path('check/<int:submit_id>', views.check_solution, name="check"),
    path('<int:pk>', views.ProblemDetailView.as_view(), name='problem-detail'),
    path('bulk_users', views.bulk_create_users, name='bulk_users'),
    path('bulk_sources', views.bulk_create_sources, name='bulk_sources'),
]