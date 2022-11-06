# leaders2022 Hackaton task №3 Application Monitoring Service
# React App + Django API


This project consists of several internal projects:

- the Django project containing the REST API along with all the backend code;
- he React project with all the Node dependencies, settings and things related to the frontend.

## Run it locally

In order to run the projects locally you need to have Node, npm and `python3` installed on your machine.

### Running the Django project

```bash
pip install django djangorestframework django-cors-headers
```

```bash
pip install seaborn
```

```bash
pip install pandas
```

```bash
pip install numpy
```

Finally, `cd` into the _django-react-logrocket_ folder and run the project:

```bash
python manage.py runserver
```


Access the address http://localhost:8000/ and check if the API is up.

### Running the React project

First, `cd` the _jkh_ directory and run:

```bash
npm install
npm start
```
