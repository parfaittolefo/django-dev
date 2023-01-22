from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context

import datetime


# This was firt type to define view
"""def currente_time(request):
    current_time= datetime.datetime.now()
    html="<html><body>It is now %s.</body></html>" % current_time
    return HttpResponse(html)
"""
# This was firt type to define view
def currente_time_with_offset(request,offset):
    try:
        offset = int(offset) 
    except ValueError:
        #raise Http404("Not found")
        pass
    #assert False  
    dt= datetime.datetime.now() +  datetime.timedelta(hours=offset)    
    html="<html><body>In %s hour(s) it will be %s.</body></html>" % (offset,dt)
    return HttpResponse(html)


# Define view using templates
def currente_time(request):
    now_time=datetime.datetime.now()
    tpl=get_template('currente_time.html')
    html = tpl.render({'now_time':now_time})
    
    return HttpResponse(html)

