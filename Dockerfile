FROM continuumio/miniconda:latest

RUN conda install python=3.6 \
    && pip install mlflow \
    && pip install numpy\
    && pip install scipy \
    && pip install pandas \
    && pip install scikit-learn\
