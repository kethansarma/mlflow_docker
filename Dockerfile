FROM continuumio/miniconda:latest

RUN pip install mlflow \
    && pip install numpy\
    && pip install scipy \
    && pip install pandas \
    && pip install scikit-learn\
