from django.contrib import admin
from django.urls import path
from messageapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create',views.create),
    path('dashboard',views.dashboard),
    path('delete/<rid>',views.delete),
    path('edit/<rid>',views.edit),
    path('home',views.home),
    path('prodet/<pid>',views.prodet),
    path('about',views.about),
    path('cart',views.cart),
    path('contact',views.contact),
    path('placeorder',views.placeorder),
    path('register',views.register),
    path('user_login',views.user_login),
    path('user_logout',views.user_logout),
    path('catfilter/<cv>',views.catfilter),
    path('sort/<sv>',views.sort),
    path('range',views.range),
    path('addtocart/<pid>',views.addtocart),
    path('remove/<cid>',views.remove),
    path('viewcart',views.viewcart),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('makepayment',views.makepayment),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
