from django.conf.urls import url, include
from django.contrib import admin

# from freports.admin import admin_site
from business_card import views as business_card

urlpatterns = [
    url(r'^$', business_card.first_page, name='first_page'),
    url(r'^freports/', include('freports.urls', namespace='freports')),
    url(r'^login/', include('login.urls', namespace='login')),
    url(r'^finance/', include('finance.urls', namespace='finance')),
    url(r'^admin/', admin.site.urls),

]
