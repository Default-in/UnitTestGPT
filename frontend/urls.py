from django.urls import path
from .views import code_input_view

urlpatterns = [
    path('code-input-form', code_input_view, name='code-input-form'),
]
