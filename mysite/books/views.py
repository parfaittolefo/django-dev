from django.shortcuts import render
from django.db.models import Q
from books.modelsapp import Book,Publisher
from books.formsapp import ContactForm,PublisherForm
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.views.generic import ListView,DetailView
from django.http import Http404

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
    # Look up the publisher (and raise a 404 if it can’t be found).
    try:
        publisher= Publisher.objects.get(name__iexact=name)
    except Publisher.DoesNotExist:
        raise Http404
     


    