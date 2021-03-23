FROM python:3.9.1
WORKDIR /usr/src
ADD requirements.txt /usr/src/
RUN pip3 install -r requirements.txt
ADD *.py /usr/src/
ENTRYPOINT [ "/usr/src/gethurricaneloss.py" ]