from django.shortcuts import render  # For rendering templates w/ context data
from django.contrib import messages  # For displaying messages to users
from .models import About
from .forms import CollaborateForm

# Create your views here.


def about_me(request):
    """
    Renders the most recent information on the website author
    and allows user collaboration requests

    Displays an individual instance of :model:'about.About'.
    **Context**
    'about':
        The most recent instance of :model:'about.About'.
    'collaborate_form':
        An instance of :form:'about.CollaborateForm'.
    **Template:**
    :template:'about/about.html'
    """

    # Retrieve the most recent About instance, ordered by the last updated date
    about = About.objects.all().order_by('-updated_on').first()

    # Handle the form submission if the request is a POST
    if request.method == "POST":
        collaborate_form = CollaborateForm(data=request.POST)
        if collaborate_form.is_valid():
            # If the form is valid, save the data and show a success message
            collaborate_form.save()
            messages.add_message(
                request, messages.SUCCESS,
                "We received your message! We'll respond within 3 days."
            )
    collaborate_form = CollaborateForm()

    return render(
        request,
        "about/about.html",
        {"about": about,
         "collaborate_form": collaborate_form
         },
    )
