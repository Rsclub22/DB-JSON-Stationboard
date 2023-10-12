FROM python:latest
WORKDIR /hafas_db
COPY Hafas_Main_web.py app.py
RUN mkdir -p templates
COPY templates templates/.
RUN pip3 install pyhafas Flask
CMD ["python3", "app.py"]
EXPOSE 5000
