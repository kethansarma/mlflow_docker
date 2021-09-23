FROM continuumio/miniconda:latest

RUN apt update && apt install -y
    pip install mlflow \
    && pip install numpy\
    && pip install scipy \
    && pip install pandas \
    && pip install scikit-learn\
