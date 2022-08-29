# Initializing Backend

After cloning the repository, you should install the requirements on your system.(if you use Windows, we recommend you to install [cmder](https://cmder.app/). But if you use Linux, you don't need to do that.

## Installation system requirements and setup project

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install virtualenv.

```bash
pip install virtualenv 
```

Then go to the project directory where you can see manage.py.

```bash
ls -a 
```
Output:
```bash
broadcast  manage.py  __pycache__       resistance  utils.py
csv        media      requirements.txt  templates 
```
Then create a virtual environment for the python : 

```bash
virtualenv venv 
```
Then activate your virtual environment :
```bash
source venv/bin/activate
```
Now you can install python requirements for this project:
```bash
pip install -r requirements.txt
```
After installing all of the requirements, you should check the database .I use Mongodb in this project.The db name I use is 'local'. Please create this database.

## Running Django
First of all, you should add the .env file to the project directory. This file contains a secret key . It looks like this:
```bash
.
.
SECRET_KEY = 'something'
.
.
```
After adding .env you should migrate your database.(make sure the virtual environment is active)
```bash
python manage.py makemigrations && python manage.py migrate
```
Then you can run the project on port 8000:
```bash
python manage.py runserver 8000
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
## Good luck 😄