from django.contrib import admin
from django.urls import path, include

# from freports.admin import admin_site
from business_card import views as business_card

urlpatterns = [
    path('', business_card.first_page, name='first_page'),
    path('freports/', include('freports.urls', namespace='freports')),
    path('login/', include('login.urls', namespace='login')),
    path('finance/', include('finance.urls', namespace='finance')),
    path('admin/', admin.site.urls),

]
