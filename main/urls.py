from django.urls import path
from main.views import WelcomeView, HelpModalView

app_name = 'main'
urlpatterns = [
    path('', WelcomeView.as_view(), name='welcome'),
    path('help/', HelpModalView.as_view(), name='showHelpModal')

]
