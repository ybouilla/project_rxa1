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

When reaching the interface, select the file you want to upload and click on `upload`. You can select the date using the upper right date selection. Time will be displayed regarding your timiezone.

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
cd frontend
npm install
npm start

```
## Build static files for front-end
```
npm run build
```

Missing aspects in the homework

- front end
    - handling http or bad request error (eg 404)
    - fixing vulnerabilities pointed out by `npm`

- middleware
    - the software as it is is not suited for production. Some component are missing 

- backend
    - missing documentation in the methods due to lack of time
    - correct the warning outputed in the logs 
    - heart rate computation: using the mean of the wave_offest and wave_onset (what I called QRS_time) instead of the wave onset reduces uncertainty by .5 (assuming there is a small but non negligeable uncertainty when measuring wave_onset and wasv_offset)