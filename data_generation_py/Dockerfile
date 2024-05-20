FROM python
RUN pip install psycopg2
RUN pip install faker
COPY generation.py generation.py
CMD ["python", "-u", "generation.py"]
