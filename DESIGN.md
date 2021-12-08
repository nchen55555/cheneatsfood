# DTC Computer Science Camps 

Welcome to DTC Computer Science Camps. I implemented the website utilizing Python, Flask, HTML, and CSS. In the files, you will find a folder called static, which stores the styles.css as well as the image files of the website. In the templates folder, you will find the html and different pages of the website. Outside, you will find a file called app.py which contains the Python/Flask of the code. Lastly, you will also find a camps.db file that is the database I created to hold the websites information. 

## Static Folder 

In the static folder, I have a variety of uploaded images as well as a styles.css page. I utilize the styles.css page throughout my html pages via statements such as `id = ` or `class = `. I also utilize CSS from bootstrap. 

## Templates Folder

In the templates folder, I have a vareity of html pages.

### about.html

In the about page, I've displayed links to the mentors.html, volunteers.html, and professionals.html pages. 

### blog.html 

In the blog page, I've utilized jinja and data passed in from app.py to display all the different blog posts in the blogs sqlite table. I've utilized a for loop from jinja to do so, so that the blogs page can easily upate any newly added blog posts. Each blog post also has a button that says "Read More." When users click on the "Read More" button, the form passes the button's value, which I coded to be the blog post's id, so that when the user is redirected to the subblog page, the page can display the speciic blog's text based on its blog_id. More on this in subblog.html.

### change.html 

In the change page, users are allowed to change their password. I've implemented a form and also utilized jinja so that a message displays on the html page if the change was successful. If not, the message will display so. The change form renders its information via POST so that hackers or malicious users cannot access the inputted information via the URL. The change post checks if the user inputted a valid username and password both via HTML as well as via app.py. This ensures that malicious hackers can't easily just change the HTML so that they destroy/bypass form requirements.

### contact.html

In the contact page, the user can contact DTC Computer Science Camps via submitting a form. The program (app.py) makes sure that all form questions are filled and that the email is valid (aka. one can email the inputted email). Then, to send the message, the code sends the message from dtccscamp@gmail.com to dtccscamp@gmail.com, including in the message the name, return email, and message of the user. To access if the contact page truly works, you may want to log in to the dtccscamp gmail account. The username is `dtccscamp@gmail.com` and the password is `DTCcsr0ck5!`. You may be wondering why we would be sending the email from dtccscamp@gmail.com to dtccscamp@gmail.com. This is because as we have no access to the user's gmail account and password, we cannot directly send it from the user's gmail account to dtccscamp@gmail.com. 

### flyer.html 

In the flyer page, the user can look at the flyer of the camps.

### index.html

In the index/home page, the user can access the flyer page because there is a button that when clicked, redirects to /flyer in app.py which renders the flyer.html template. 

### info.html 

In the Sessions and Information page, the user can sign up/register for the camps. Walking through the implementation, it is important to note that I've utilized some jinja to display a message of whether the registration was successful or not. For example, once app.py receives the form information, it checks to see if the information in the form is valid. If it is not, it will pass in a message saying so via render_template and the message will be displayed in the info.html page. 

In app.py, it adds the registration information to both the registration table as well as the members table. This is because once registered, the user is considered a "member" of the camps and therefore should be able to access the resources of the camps. The default username and password for registrants are their first name and last name respectively, but registrants can change their password later on via the Change Password page. It is important to note that if two registrants have the same first name, app.py will adjust the username and password accordingly. Thus, if "Nicole Chen" signed up for first, she will receive a username of "Nicole" and a password of "Chen." But if another "Nicole Chen" signs up, she will receive a username of "Nicole2" and a password of "Chen." This ensures that there aren't duplicate usernames. The log in information will be sent via email to the registrant. 

### layout.html

In the layout page, I have used jinja to determine that if a user is signed in, the About, Sessions and Information, Contact Us, Blog, Resources, Log Out, and Change Password pages will be open to access. However, if the user is not logged in, the navigation panel will only display About, Sessions and Information, Contact Us, Blog, and Log in. This is because only registered/logged in users should have access to the camp's resources. 

### login.html 

In the login page, users can log in to access the resources page. The HTML automatically checks to see if all inputs are inputted, but app.py also checks too. If there are invalid inputs, app.py will pass in an error message that will be displayed via jinja on the login.html page. 

### mentors.html 

In the mentors page, users can view the biographies of the mentors. 

### professionals.html 

In the professionals page, users can view the biographies of the professionals who have come to speak at the camps. 

### resources.html 

In the resources page, users can access links to the different camp lessons and notes. Please note, that as specified in app.py, this page is restricted so that only users that have logged in can access it. Moreover, towards the bottom of the resources page is a blog post form. However, the blog post form is only visible to administrators, and I was able to restrict this access using jinja, passing in whether a member was an admin or not via app.py. It is stored in the members database whether or not a user is an admin. The blog post form is only visible to administrators because not everyone should be able to post a blog. Please check the README.md file if you would like to log in as an administrator. Please note: in inserting blog text, you can add html tags such as an `<a></a>` tag or a `<BR>` tag and the text will apply that html when it displays the blog text. This is because in app.py, the text goes through the `Markup()` function. This is only available to the blog text input. 

### subblog.html 

In the subblog page, users can read the specific blog the clicked on to "Read More." The subblog page takes in the blog_id value from the "Read More" button passed by blog.html, and utilizing the blogs sqlite table, accesses the title, date, text, and image source of the blog post with the specific blog_id passed by the button in app.py. Using jinja, the subblog.html page successfully posts each blog's title, text, date, and imagesource accordingly. 

### volunteers.html 

In the volunteers page, users can apply to be a volunteer. There is jinja that displays a message passed in from app.py that determines whether the form inputs were valid or not. The input is all stored in the volunteerResponses sqlite table. Moreover, an email is sent from app.py notifying the volunteer via their email that the camps have received their application. 

## app.py 

In app.py, I've utilized Flask to ensure that information from the webpage can be dynamically passed around. There are several routes that utilize both GET and POST in app.py: /info, /contact, /resources, /change, /login, and /volunteers. This is because these routes bring in private data such as passwords to app.py and as such, should be rendered through POST. There are four databases in app.py: volunteerResponses, which takes in all the volunteer applications from volunteer.html; registration, which takes in all the registration responses via info.html; blogs, which takes in all the blog posts from resources.html; and members, which documents all the members of DTC Computer Science Camps - updated in conjunction with registration via the info.html page. Please note that there are some funky functions that I utilized in app.py because I did not import SQL from the CS50 library. As such, I had to search up different remedies for when SQL acted up, and these funky functions provided the best remedies. 

