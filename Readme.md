# Cardiologs homeworks`

## Prerequisites

The project has been made and tested on ubuntu os

The following project needs the following setup to be launched:
- conda or any other virtual environment
- npm
- nodejs


## Run project
```
cd cardiologs_homeworks
conda activate cardiologs
pip install -r requirements.txt

gunicorn --bind 0.0.0.0:5000 wsgi:app
```
and reach [http://127.0.0.1:5000](http://127.0.0.1:5000)


## How to use the interface

When reaching the interface, select the file you want to upload by clicking first on `browse` and then click on `upload`. You can select the date using the upper right date selection. Time will be displayed regarding your timezone.

## Run server only

Use the following to run the backend code

```
cd cardiologs_homeworks
python app.py
```

debug mode
```
cd cardiologs_homeworks
flask –app app.py –debug run
```

## Run web browser (debug mode)

Run the following to use the front end in a debug mode
```
cd cardiologs_homeworks/frontend
npm install
npm start

```
## Build static files for front-end
In order to build the react project run:
```
cd cardiologs_homeworks/frontend
npm run build
```

## Dependencies

Please find dependencies:
- python dependencies: [`requirements.txt`](./requirements.txt).
- javascript and react dependencies: [`frontent/package.json`](./frontend/package.json).

Front end template has been taken from [materialGUI examples](https://mui.com/material-ui/getting-started/templates/).

## Missing aspects in the homework

- general 
    - remove commented piece of code
    - add unit tests

- front end
    - handling http or bad request error (eg 404)
    - fixing vulnerabilities pointed out by `npm`

- middleware
    - the software as it is is not suited for production. Some components are missing (middleware, testing suit, ...)

- backend
    - missing documentation in the methods due to lack of time
    - correct the warning outputed in the logs 
    - heart rate computation: using the mean of the wave_offest and wave_onset (what I called QRS_time) instead of the wave onset should reduce uncertainty in the measurement (assuming there is a small but non negligeable uncertainty when measuring wave_onset and wasv_offset)