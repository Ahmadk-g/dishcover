from django.test import TestCase
from django.urls import reverse
from .models import About, CollaborateRequest
from .forms import CollaborateForm


class TestAboutView(TestCase):
    """
    Test cases for the About view;
    ensuring it renders correctly and handles form submissions.
    """

    def setUp(self):
        """Create a test instance of the about model"""

        self.about = About(
            title="About Me", content="This is about me.")
        self.about.save()

    def test_about_me_view(self):
        """
        Test that the about_me view renders the about.html
        template with the correct context data.
        """
        # Perform a GET request to the 'about' view
        response = self.client.get(reverse('about'))
        # Assert the response status code is 200
        self.assertEqual(response.status_code, 200)
        # Assert that the correct template is used
        self.assertTemplateUsed(response, 'about/about.html')

        # Assert that the 'About Me' title & content are in the response
        self.assertContains(response, self.about.title)
        self.assertContains(response, self.about.content)

    def test_render_about_page_with_collaborate_form(self):
        """Verify that the 'about' page contains a collaboration form. """

        # Perform a GET request to the 'about' view
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

        # Assert that the page contains the text "About Me"
        self.assertContains(response, "About Me")

        # Assert that the collaborate_form is present in the context
        # and is an instance of CollaborateForm
        self.assertIsInstance(
            response.context['collaborate_form'], CollaborateForm
        )
        # Check that form fields are present
        self.assertContains(response, 'name="name"')
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'name="message"')

    def test_about_me_view_post_valid(self):
        """
        Test that the about_me view correctly processes
        a valid POST request for the collaboration form.
        """
        # Define valid form data
        form_data = {
            'name': 'Test User',
            'email': 'testuser@example.com',
            'message': 'I want to collaborate!'
        }
        # Perform a POST request to the 'about' view with the form data
        response = self.client.post(reverse('about'), data=form_data)

        # Assert the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the form data was saved correctly
        self.assertTrue(CollaborateRequest.objects.filter(
            email='testuser@example.com').exists())
        collaborate_request = CollaborateRequest.objects.get(
            email='testuser@example.com')
        self.assertEqual(collaborate_request.name, 'Test User')
        self.assertEqual(collaborate_request.message, 'I want to collaborate!')

        # check that a success message is displayed
        self.assertContains(response,
                            "We received your message!"
                            " We'll respond within 3 days.")
