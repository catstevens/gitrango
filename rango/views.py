from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

from rango.models import Page
from rango.models import Category

def category(request, category_name_url):
    # Request our context from the request passed to us.
    context = RequestContext(request)

    # Change underscores to the category name to spaces.
    # URLs don't handle spaces well, so we encode them as underscores.
    # We can then simply replace the underscores with spaces again to get the name
    category_name = category_name_url.replace('_',' ')

    # Create a context dictionary which we can pass to the template rendering engine.
    # We start by containing the name of the category passed by the user.
    context_dict = {'category_name': category_name}

    try:
        # Can we find a category with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception
	category = Category.objects.get(name=category_name)

	# Retrieve all of the associated pages.
        # Note that filter returns >=1 model instance.
        pages = Page.objects.filter(category=category)

	# Add our results list to the template context under name pages.
	context_dict['pages'] = pages
	# We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render_to_response('rango/category.html', context_dict, context)

def index(request):
    # Obtain the context from the HTTP request.
    context = RequestContext(request)

    # Query the database for the list of ALL categories currently stored.
    # Order the categories by no. Likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    # The following two lines are new.
    # We loop through each category returned, and create a URL attribute.
    # This attribute stores an encoded URL (e.g. space replaced with underscores).
    for category in category_list:
	category.url = category.name.replace(' ','_')    

    # Return the response and send send it back!
    return render_to_response('rango/index.html', context_dict, context)

def index1(request):
    #return HttpResponse("Rango says: Hello world! <a href='/rango/about'>About</a>")
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'boldmessage': "I am bold font from the context"}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('rango/index.html', context_dict, context)

def about(request):
    return HttpResponse("Rango says: Here is the about page. <a href='/rango'>Index</a>")
