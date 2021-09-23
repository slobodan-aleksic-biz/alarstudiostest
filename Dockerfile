FROM python:3.9 
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY app/requirements.txt /app/requirements.txt 
RUN pip install -r requirements.txt 
COPY ./ ./

CMD . ./run.sh


