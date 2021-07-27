FROM python:3.8.0
RUN pip install psycopg2
ADD . /prepare_dwh_app
CMD ["/prepare_dwh_app/prepare_dwh.py"]
ENTRYPOINT ["python3"]
