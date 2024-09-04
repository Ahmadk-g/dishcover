# Testing

## Manual Testing

Page/View | What was tested | Expected outcome | Result |
|------------|------------------------------|--------------------------------------|--------|
| NavBar | Logo - Click on the Logo | Redirect to the home page | Passed|
| NavBar | Links - Click to open links | Redirect to each page | Passed |
| NavBar | Register - Click on the "Register" Button | Redirect to relevant pages | Passed |
| NavBar | Login - Click on the "Login" Button | Redirect to relevant pages | Passed |
| NavBar | Logout - Click on the "Logout" Button | Redirect to relevant pages | Passed |
| Home | Searchbar | Redirect to recipes page, showing recipes that match the search criteria. | Passed|
| Home | "Recipes" link box | Redirect to Recipes page | Passed |
| Home | "Add Recipe" link box | Redirect to Add Recipe view | Passed |
| Home | "Collaborate with us " link box | Redirect to About page | Passed |
| Recipes | Page Load | Display a paginated list of Recipes, starting with latest| Passed|
| Recipes | Filter Functionality | Filter results are accurate| Passed |
| Recipes | "Add Recipe" link box | Redirect to Add Recipe view | Passed |
| Recipes | Pagination controls | Redirect to next or previous page | Passed |
| Recipes | Click on Recipe card| Redirect to detailed view of recipe | Passed |
| Recipe Detail | Detailed view of recipe | All fields are displayed | Passed|
| Recipe Detail | Like count | Like count is displayed | Passed |
| Recipe Detail | Like recipe | Like count increases and recipe added to favorites | Passed |
| Recipe Detail | Unlike recipe | Like count decreases and recipe removed from favorites| Passed |
| Recipe Detail | Click on Edit Recipe | Redireced to Edit Recipe form with prefilled fields| Passed |
| Recipe Detail | Click on Delete Recipe | Redirect to Delete confirmation page | Passed |
| Recipe Detail | Like/unlike feedback messages | Correct messages displayed | Passed |
| Recipe Detail | Update or delete feedback messages | Correct messages displayed | Passed |
| Add Recipe | Empty Required field | Can't submit, error is displayed | Passed|
| Add Recipe | Upload image| image uploaded to cloudinary | Passed |
| Add Recipe | Click on 'Create Recipe' | Redirect to Recipes page, showing new recipe | Passed |
| Edit Recipe | Form Load | Display prefilled form fields | Passed |
| Edit Recipe | Click on 'Update Recipe' | Redirect to updated recipe detail view | Passed |
| Delete Recipe | Click on Back | Redirect to recipe detailed view| Passed |
| Delete Recipe | Click on Confirm Delete | Delete recipe & redirect to last page | Passed |
| My Recipes | Page view | Display all recipes created by requesting user | Passed |
| My Recipes | Empty | Display 'Create new recipe' with link | Passed |
| My Favorites | Page view | Display all recipes liked by requesting user | Passed |
| My Favorites | Page view | Display "no favorites" with link to Recipes page | Passed |
| Sign up | Create an account| Username and password required | Passed |
| Sign up | Email| optional | Passed |
| Sign up | back button and submit | redirect to Home page | Passed |
| Sign in | login | Username and password are required, remember me is optional  | Passed |
| Sign in | login with wrong credentials | warning message | Passed |
| Sign in | after process | redirect to Home page| Passed |
| Sign Out | after process | redirect to Home page| Passed |
| Feedback Messages | Like Recipe | "Recipe added to Favorites." | Passed |
| Feedback Messages | Unlike Recipe | "Recipe removed from Favorites." | Passed |
| Feedback Messages | Edit Recipe | "Recipe updated." | Passed |
| Feedback Messages | Create Recipe | "Recipe added successfully." | Passed |
| Feedback Messages | Delete Recipe | "Recipe deleted successfully." | Passed |
| Feedback Messages | logout | "You have signed out." | Passed |
| Feedback Messages | login | "Successfully signed in as {User}" | Passed |
| Feedback Messages | Fade out | message fade out in seconds | Passed |
| Admin Dashboard | Admin Panel Access | Appears in Navbar for superusers | Passed |

## Automated Testing 

Automated testing in Django and Python is essential for maintaining code quality and reliability. Django’s built-in testing framework, which integrates with Python's unittest module, supports the creation of various tests. For example, test_forms.py and test_views.py focus on unit and functional tests for forms and views, verifying that they work correctly. Automated testing helps quickly identify and address issues, maintain code integrity, and improve the overall stability and performance of the application.


![Automated Testing](documentation/testing/autotesting.png)

### Running the Tests

**1. Open Terminal/Command Prompt:** Launch your termianl or command prompt.

**2. Navigate to Project Directory:** Use the terminal to navigate to the project's root directory where manage.py is located.

**3. Run the Tests:** Execute the Following Command:
```bash
python manage.py test
```
This command triggers the Django test runner, which locates and runs all test cases across the project. It scans the project's directories, identifies test files, and runs each test case, providing detailed results, including the number of tests, any failures or errors, and an overall summary.

Django will create a temporary test database, run the tests, and then discard the database. This ensures that your testing is clean and doesn't affect your production data.

## Responsiveness Testing

Responsiveness testing was conducted using Chrome Developer Tools to ensure Dishcover provides an optimal user experience across various devices. During development, the following devices were emulated:

- Desktop
- Laptops
- Tablets
- Mobile Phones

This approach ensured the webpage adapts seamlessly to different screen sizes and orientations, maintaining functionality and aesthetics across all devices.


## Validator Testing

### Python

[PEP8 CI Linter](https://pep8ci.herokuapp.com/) provided by the Code Institute according to the PEP 8 style guide for validating the Python code.

#### foodblog - Project Module Python Validation Results

Python File | Results | Comment |
|------------|------------------------------|--------------------------------------|
|setting.py| <details> <summary><strong>Click to View Results</strong></summary>![PEP8 Results](documentation/testing/pep8/settings.py.png) </details> | No Errors
|manage.py| <details> <summary><strong>Click to View Results</strong></summary>![PEP8 Results](documentation/testing/pep8/manage.py.png) </details> | No Errors
|urls.py| <details> <summary><strong>Click to View Results</strong></summary>![PEP8 Results](documentation/testing/pep8/urls.py.png) </details> | No Errors
|views.py| <details> <summary><strong>Click to View Results</strong></summary>![PEP8 Results](documentation/testing/pep8/views.py.png) </details> | No Errors
|wsgi.py| <details> <summary><strong>Click to View Results</strong></summary>![PEP8 Results](documentation/testing/pep8/wsgi.py.png) </details> | No Errors
|asgi.py| <details> <summary><strong>Click to View Results</strong></summary>![PEP8 Results](documentation/testing/pep8/asgi.py.png) </details> | No Errors

#### Recipes - App Module Python Validation Results

Python File | Results | Comment |
|------------|------------------------------|--------------------------------------|
|admin.py| <details> <summary><strong>Click to View Results</strong></summary>![PEP8 Results](documentation/testing/pep8/recipe-admin.py.png) </details> | No Errors
|forms.py| <details> <summary><strong>Click to View Results</strong></summary>![PEP8 Results](documentation/testing/pep8/recipe-forms.py.png) </details> | No Errors
|models.py| <details> <summary><strong>Click to View Results</strong></summary>![PEP8 Results](documentation/testing/pep8/recipe-models.py.png) </details> | No Errors
|urls.py| <details> <summary><strong>Click to View Results</strong></summary>![PEP8 Results](documentation/testing/pep8/recipe-urls.py.png) </details> | No Errors
|views.py| <details> <summary><strong>Click to View Results</strong></summary>![PEP8 Results](documentation/testing/pep8/recipe-views.py.png) </details> | Long lines can't be divided
|apps.py| <details> <summary><strong>Click to View Results</strong></summary>![PEP8 Results](documentation/testing/pep8/recipe-apps.py.png) </details> | No Errors

#### About - App Module Python Validation Results

Python File | Results | Comment |
|------------|------------------------------|--------------------------------------|
|admin.py| <details> <summary><strong>Click to View Results</strong></summary>![PEP8 Results](documentation/testing/pep8/about-admin.py.png) </details> | No Errors
|forms.py| <details> <summary><strong>Click to View Results</strong></summary>![PEP8 Results](documentation/testing/pep8/about-forms.py.png) </details> | No Errors
|models.py| <details> <summary><strong>Click to View Results</strong></summary>![PEP8 Results](documentation/testing/pep8/about-models.py.png) </details> | No Errors
|urls.py| <details> <summary><strong>Click to View Results</strong></summary>![PEP8 Results](documentation/testing/pep8/about-urls.py.png) </details> | No Errors
|views.py| <details> <summary><strong>Click to View Results</strong></summary>![PEP8 Results](documentation/testing/pep8/about-views.py.png) </details> | No Errors
|apps.py| <details> <summary><strong>Click to View Results</strong></summary>![PEP8 Results](documentation/testing/pep8/about-apps.py.png) </details> | No Errors




