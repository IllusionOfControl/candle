# candle

_Сourse project_

An educational project that allows you to catalog books by author, book series, publisher and tags. Allows you to search.

## Local running

```sh
pip install -r requirements.txt
python ./manage.py collectstatic
python ./manage.py migrate
python ./manage.py runserver
```

## Docker running

```sh
docker build -t candle .
docker run -e DEBUG=False -p 8000:8000 -v $(pwd)/storage:/app/storage candle
```
