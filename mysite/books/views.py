from django.shortcuts import render
from django.db.models import Q
from books.modelsapp import Book,Publisher
from books.formsapp import ContactForm,PublisherForm
from django.http import HttpResponseRedirect,HttpResponse
from django.core.mail import send_mail
from django.views.generic import ListView,DetailView
from django.http import Http404
from django.template import RequestContext
import csv
from reportlab.pdfgen import canvas

# Create your views here.
def search(request):
    error = False
    if 'q' in request.GET:
        query = request.GET.get('q', '')
        if query and len(query)<=20:
            qset =(
            Q(title__icontains=query) |
            Q(authors__first_name__icontains=query) |
            Q(authors__last_name__icontains=query)
            )
            results = Book.objects.filter(qset)

        elif len(query) > 20:
            error = True
            return render(request,'search.html', {'error': error})
        else:
            error = True
            #results = []
            return render(request,'search.html', {'error': error})
        error = False
        return render(request,"search.html", {
        "results": results,
        "query": query
        })
    else:
        return render(request,'search.html', {'error': error})

def thanks(request):
    return render(request,'thanks.html',{})

def contact(request):
    if True:
        form = ContactForm(request.POST)
        if form.is_valid():
            topic = form.cleaned_data['topic']
            message = form.cleaned_data['message']
            sender = form.cleaned_data.get('sender', 'noreply@example.com')

            """send_mail(
            'Feedback from your site, topic: ' + topic,
            message, sender,
            ['parfaittolefo23@gmail.com']
            )"""
            return HttpResponseRedirect('/thanks/')
        else:
            return render(request,'contact.html', {'form': form})
        

def add_publisher(request):
    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/thanks/')
    form = PublisherForm()
    return render(request,'add_publisher.html', {'form': form})

def get_books():
    return Book.objects.all()
    
class PublisherList(ListView):
    model = Publisher
    template_name='publisher_list.html'
    context_object_name='publisher_list'
    extra_context = {"book_list" : get_books()}

"""def publishers(request):
    results= Publisher.objects.all()
    results=(results)
    print(results)
    return render(request,'publisher_list.html',{"results":results})"""

class PublisherDetail(DetailView):
    
    model = Publisher
    template_name='publisher_detail.html'
    context_object_name='publisher_detail'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PublisherDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['book_list'] = Book.objects.all()
        return context

class BookList(ListView):
    queryset = Book.objects.order_by('-publication_date')
    context_object_name = 'book_list'


def books_by_publisher(request, name):
    # Look up the publisher (and raise a 404 if it can't be found).
    try:
        publisher= Publisher.objects.get(name__iexact=name)
    except Publisher.DoesNotExist:
        raise Http404
     

contexts={
            'ap': 'My app',
            'user': 'User name',
            'ip_address':'User IP'
        }

def my_proc_view(request):
    return render(request,'processors_template.html',contexts)

#Serve image to broswer
def my_image(request):
    image_data= open("/tmp/chall_1.jpg", "rb").read()
    return HttpResponse(image_data, content_type="image/png")


def some_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment';
    filename="somefilename.csv"

    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"'])

    return response

#PDF Generating

def some_view(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment';
    filename="somefilename.pdf"

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response
        
    
    # Complexe ODF more efficient

from io import BytesIO
from reportlab.pdfgen import canvas

def some_view(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment';
    filename="somefilename.pdf"

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response