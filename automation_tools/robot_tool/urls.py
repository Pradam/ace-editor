from django.conf.urls import url
from .views import AceView

urlpatterns = [
    url(r'^$', AceView.as_view(), name='editor'),
]
