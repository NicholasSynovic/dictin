FROM python:3-buster as base
WORKDIR /opt/app
RUN mkdir output
COPY MerriamWebster.py .

FROM base as optionalUpgrade
RUN apt-update
RUN apt-upgrade -y

FROM optionalUpgrade as requirementInstaller
RUN python -m pip install --upgrade pip
RUN python -m pip install bs4 lxml progress requests

FROM requirementInstaller as executor
ENTRYPOINT [ "python", "MerriamWebster.py" ]
