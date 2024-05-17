# DTC Computer Science Camps 

A web application built so that individuals can access the DTC Computer Science Camps website, register for the camps, sign up to be a volunteer, access resources posted on the camp website once registered to the camps, and read through the camps' blog posts. Please access my github account [here] (https://github.com/nchen55555/DTCCSCamps)

## Compiling the Website 

Once Heroku (the web-hosting platform) is up and running, you can access the website via the link [here] (https://dtccscamps.herokuapp.com/); however, if Heroku is down again or simply not working, please access the website via the terminal commands first `. venv/bin/activate` then `flask run`. In other words, please type in `. venv/bin/activate` and click enter then type in `flask run`. The terminal will provide you a link to run the website. 


## Exploring the Website
Upon accessing the website, you will find a webpage with a navigation panel that has 6 different tabs - DTC CS Camps (the homepage), About, Sessions and Information, Contact Us, Blog, and Log In. You can also watch this video as I go through the project myself linked [https://youtu.be/eZlZbD-GdcA] (https://youtu.be/eZlZbD-GdcA).

#### Home Page 
On the home page, you should find a button, that when clicked, should lead to the Flyer page that displays a Flyer for the camps. In the About page, you should find three buttons: Mentors, Volunteers, and Professionals. Each of these buttons, once clicked, will lead to a different page. 

##### Mentors Page
The Mentors page will showcase a page dedicated to the mentors and their biographies. 

##### Volunteers Page 

The Volunteers page will showcase a page dedicated to the volunteers and their biographies. There will also be a form towards the bottom of the Volunteers page that allows users to apply to be a volunteer. After applying, the form will send out an email to the volunteer based on the email they inputted in the form and save the volunteer's response. 

#### Professionals Page 
The Professionals Page displays professionals pictures and biographies of the professionals who have come to the camps to speak. 

### Sessions and Information Page 

Going back to the navigation panel, the Sessions and Information page displays the two different camp sessions ofered at DTC Computer Science Camps: Processing and Java. As you scroll down, there is also a registration form that takes in a future registrant's first name, last name, email, phone number, age, and has a check box to which camp sessions the registrant would like to take. Registrants are automatically registered as "members" of the camps, and therefore will be able to log in and access the additional resources of the camps. The registrant will receive their log in information via email after they have signed up for the camps. Towards the bottom of the Sessions and Information page are two videos that showcase what the camps were like in 2020 and 2019. Lastly, the Sessions and Information page displays student and parent testimonials. 

### Contact Us Page 

The Contact Us Page displays a contact us form that required the user to input their name, email, and message. To check if the contact us page is working, please email me at `nicole_chen@college.harvard.edu` or text me at `3035055533` so that I can send you a screenshot of the email sent to `dtccscamp@gmail.com`. I can also provide you the password of the email account if you contact me individually. The contact us form will send an email to the dtccscamp email.

### Blog Page

The Blog Page displays all the blog posts from the blog sqlite table. Users can click the "Read More" button to read each individual blog post. 

### Log In Page

The Log In Page displays a log in form where users can log in to access additional resources to the camps. Users may only log in AFTER they have registered for the camps. 

### Resources Page

Once logged in, users can access the Resources page which contain several links to the materials used throughout the camps. If the user is considered an admin, he/she can access the blog post form. Currently, the only admin is Nicole Chen (me). If you would like to access the website via an admin perspective, log in with the username of `Nicole` and password of `Chen`. The blog post form allows the administrator to update the blog sqlite table and post more blogs. There are 4 parts of the blog post form: title, date, image source, and blog post text, where image source is the file name of the image (ie. nicole.jpg). Once a blog is posted, it is updated on the blogs page. 

### Log Out Page

If the user is logged in, there is also a log out page that essentially logs the user out. 

### Change Password Page

If the use is logged in, there is also a change password page that allows the user to change their password, granted they input the correct username and password. Once changed, the website automatically signs the user out so they have to re-login with their new password. 

