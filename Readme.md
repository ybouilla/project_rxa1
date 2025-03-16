# Cardiologs homeworks`

## Prerequisites

The following project needs the following setup to be launched:
- conda or any other virtual environment
- npm
- nodejs


## Run project
``
conda create -n cardiologs --file requirements.txt
conda activate cardiologs

gunicorn --bind 0.0.0.0:5000 wsgi:app
```
and reach [http://127.0.0.1:5000]()


## Run server only

```
python app.py
```

debug mode
```
flask –app app.py –debug run
```

## Run web browser (development mode)

```
npm start

```
## Build static files for front-end
```
npm run build
```

Missing aspects in the homework

- front end
    - handling http or bad request error (eg 404)