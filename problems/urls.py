from django.urls import path

from . import views


urlpatterns = [

    path('', views.index, name='index'),
    path('failed/<int:student_id>/<int:testset_pk>', views.failed_tests, name='failed'),
    path('<str:problem_type>/<int:start>/<int:amount>', views.ajax_problems, name='ajax_problems'),
    path('assign', views.assign, name='assign'),
    path('submit', views.submit, name='submit'),
    path('save_verdict', views.save_verdict, name='save_verdict'),
    path('source_list', views.source_list, name='source_list'),
    path('check/<int:submit_id>', views.check_solution, name="check"),
    path('submit/<int:pk>', views.submit_detail, name="submit-detail"),
    path('<int:pk>', views.ProblemDetailView.as_view(), name='problem-detail'),
    path('bulk_users', views.bulk_create_users, name='bulk_users'),
    path('bulk_sources', views.bulk_create_sources, name='bulk_sources'),
    path('load_test', views.load_test, name='load_test'),
    path('testset/<int:pk>', views.testset, name='testset'),
    path('check_testset', views.testset_submit, name='check_testset'),
    path('testset_result/<int:test_assignment_id>', views.test_result, name='testset_result'),
    path('testset_result_all/<int:testset_pk>', views.testset_all_results, name='testset_result_all'),
    path('test', views.test, name='test'),
    path('rejudge_test/<int:test_id>', views.rejudge_test, name='rejudge_test'),
    path('student_page/<int:pk>', views.student_page, name='student_page'),

]