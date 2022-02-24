
# AuthApi
This project provides a set of REST API endpoints and HTML interface for registration, authentication , password reset, retrieve JWT token on successful login.


## Get Started (Locally)

Clone the project

```bash
  git clone https://github.com/navi532/AuthApi.git
```

Go to the project directory.  
```bash
  cd my-project
```
Make sure `manage.py` exists in current directory. 


Install dependencies

For `Python 2:`
```bash
  pip install -r requirements.txt
```

For `Python 3:`
```bash
  pip3 install -r requirements.txt
```

`(Make sure pip/pip3 is installed in your system)`

If running the server for the first time
```bash
    python3 manage.py migrate
```

Start the server
```bash
  python3 manage.py runserver
```


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`JWT_SECRET_KEY` = "any_randomkey_for_JWT_Token"  
`EMAIL_USER` = "yourgmailid"  
`EMAIL_PASS` = "yourpassword"  

## API Documentation
To learn about API Endpoints, start the server and go to `/swagger`.
