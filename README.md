# Fantastic-Lib
A Library management system built using Django framework. It is designed for managing Authors, Books, Categories and Users. 
The frontend is designed with html (css+js) and the sqLite is used as database.

### Exemples of views
![alt text](https://i.postimg.cc/tRvgBYg2/pic3.png)
![alt text](https://i.postimg.cc/jdWSmtwK/pic4.png)
## Installation
* Download Python > 3.8
* Install virtualenv  
```bash
pip install virtualenv
```
* Create virtualenv
```bash
virtualenv library # you can choose your own name
```
* Activate virtualenv
```bash
library\Scripts\Activate
```
* Install Django
```bash
cd library
pip install django
```
* Additional packages I used so I can encrypt the password of the user, and show the media uploaded
```bash
pip install bcrypt
python -m pip install Pillow
```
### Encryption of the password
![alt text](https://i.postimg.cc/NfWjwSmX/pic6.png)

## Usage

Go to the library folder and run

```bash
python manage.py runserver
```

Then go to the browser and enter the url **http://127.0.0.1:8000/**

### Index page
![alt text](https://i.postimg.cc/C55xFVcG/pic1.png)

## Signup

The Signup page is used for all users.  
An error message will show up if the data entred is not compliant.   

### Signup Page
![alt text](https://i.postimg.cc/XJQvSvkN/pic2.png)

You can access the django admin page at **http://127.0.0.1:8000/admin** and login with username 'admin' and with the password Admin_pass123.

Also a new admin user can be created using

```bash
python manage.py createsuperuser
```
### Admin Panel
![alt text](https://i.postimg.cc/zvQXvPQ9/pic5.png)




  
  

