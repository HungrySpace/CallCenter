from rest_framework import routers
# from .api import EventsViewSet, ClientNumberViewSet
from . import views
from django.urls import path

# router = routers.DefaultRouter()
# router.register('event', EventsViewSet, 'event')
# router.register('ClientNumber', ArticleView, 'ClientNumber')

urlpatterns = [
    path('events', views.EventsViews.as_view()),
    path('client', views.ClientCardCreateGet.as_view()),
    path('client/<int:pk>', views.ClientCardEditingDelete.as_view()),
]

#urlpatterns = router.urls
