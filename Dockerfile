FROM python:3.8
WORKDIR /APP
COPY . /APP
RUN pip install update
RUN pip install -r requirements.txt

ENV TLG_ACCESS_TOKEN=7090085173:AAEWYRaqleogIyZySqSgfUl_CL0O3rUgjHg
ENV BASICURL=https://chatgpt.hkbu.edu.hk/general/rest
ENV MODELNAME=gpt-35-turbo
ENV APIVERSION=2024-02-15-preview
ENV GPT_ACCESS=c813af90-2980-4c99-9bf5-8cf8e0eaa493

CMD python app.py