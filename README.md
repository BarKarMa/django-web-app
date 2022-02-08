# django Dashboard and parsing blog.python.org

<p align="center">
   <img src="images/img_0001.jpg" alt="[YOUR_ALT]" width="300" height="200"/>
</p>

### Initialize and activate the virtual environment

#### For the application to work, you must have Django version at least 3.2.12

### Install all packages from the requirements.txt file in the root folder of the project
### Go to the folder with  manager.py  
  > cd blog-api/blogparsing
### Deploy the python 
  > manage.py migrate database migration 
### Parse the site with the 
  > python manage.py parse_blog 
### command in the console
### Launch the development server and go to the home page
