FROM tensorflow/tensorflow

WORKDIR /usr/src/

COPY . /usr/src/

CMD [ "python", "classify.py" ]
