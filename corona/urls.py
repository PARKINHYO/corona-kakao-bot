from django.urls import path
from .views import daily_views, realtime_views, message_views
# Create your views here.

urlpatterns = [
    path('daily/text', daily_views.text),
    path('daily/image', daily_views.image),

    path('realtime/text', realtime_views.text),

    path('message/text', message_views.text)


    



]
