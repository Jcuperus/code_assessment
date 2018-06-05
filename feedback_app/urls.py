from django.urls import path

from . import views

app_name = 'feedback'

urlpatterns = [
    path('', views.index, name='index'),
    path('result', views.result, name='result'),
    path('assessments', views.assessments, name='assessments'),
    path('assessments/<int:assessment_id>', views.assessment_detail, name='assessment_detail')
]