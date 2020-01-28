from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('assign', views.assign, name='assign'),
    path('submit', views.submit, name='submit'),
    path('save_verdict', views.save_verdict, name='save_verdict'),
    path('source_list', views.source_list, name='source_list'),
    path('check/<int:submit_id>', views.check_solution, name="check"),
    path('submit/<int:pk>', views.SubmitDetailView.as_view(), name="submit-detail"),
    path('<int:pk>', views.ProblemDetailView.as_view(), name='problem-detail'),
    path('bulk_users', views.bulk_create_users, name='bulk_users'),
    path('bulk_sources', views.bulk_create_sources, name='bulk_sources'),
    path('load_test', views.load_test, name='load_test'),
]