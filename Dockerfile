FROM continuumio/miniconda:latest

RUN apt-get --allow-releaseinfo-change update && apt-get install python3.7 \
    pip install mlflow \
    && pip install numpy\
    && pip install scipy \
    && pip install pandas \
    && pip install scikit-learn\
