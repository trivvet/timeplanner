from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView

from rest_framework_jwt.views import obtain_jwt_token

# from freports.admin import admin_site
from business_card import views as business_card
from ang import AngularTemplateView

urlpatterns = [
    url(r'^$', business_card.first_page, name='first_page'),
    url(r'^freports/', include('freports.urls', namespace='freports')),
    url(r'^login/', include('login.urls', namespace='login')),
    url(r'^finance/', include('finance.urls', namespace='finance')),
    url(r'^api/freports/', include('freports.api.urls', 
        namespace='freports_api')),
    url(r'^admin/', admin.site.urls),
]

urlpatterns += [
    url(r'^angular/', login_required(TemplateView.as_view(template_name="ang/base.html")),
        name="angular_page"),
    url(r'^api/templates/(?P<item>[A-Za-z0-9\-\_\.\/]+)\.html$', 
        AngularTemplateView.as_view()),
    url(r'^api/auth/token/', obtain_jwt_token),
]
