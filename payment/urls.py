from django.urls import path
from payment import views

app_name = 'payment'

urlpatterns = [
    path('<int:id>/', views.pay, name='pay'),
    path("lnm/", views.LNMCallbackUrlAPIView.as_view(), name='callback')
]