from django.urls import include, re_path
from .  import views
from django.views.generic import TemplateView
from .modelsapp import Publisher, Book
from .views import PublisherList

publisher_info = {
    "queryset" : Publisher.objects.all(),
    "template_object_name" : "publisher",
    "extra_context" : {"book_list" : Book.objects.all()}
    }
urlpatterns = [
    re_path(r'^search/$',views.search),
    re_path(r'^contact/$',views.contact),
    re_path(r'^thanks/$',views.thanks),
    re_path(r'^add_publisher/$',views.add_publisher),
    #re_path(r'^search/$', TemplateView.as_view(template_name='search.html'), name="search"),
    #re_path(r'^publishers/$', PublisherList.as_view()),
    re_path(r'^publishers/$', PublisherList.as_view(),publisher_info),
    re_path(r'^my_proc/$',views.my_proc_view),

]