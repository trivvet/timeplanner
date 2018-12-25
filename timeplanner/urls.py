from django.conf.urls import url, include
from django.views.generic.base import TemplateView

from freports.admin import admin_site
from business_card import views as business_card

urlpatterns = [
    url(r'^$', business_card.first_page, name='first_page'),
    url(r'^freports/', include('freports.urls', namespace='freports')),
    url(r'^login/', include('login.urls', namespace='login')),
    url(r'^finance/', include('finance.urls', namespace='finance')),

    url(r'^freports/api', include('freports.api.urls', 
        namespace='freports_api')),
    url(r'^myadmin/', admin_site.urls),

]

urlpatterns += [
    url(r'^angular/', TemplateView.as_view(template_name="ang/base.html")),
]
