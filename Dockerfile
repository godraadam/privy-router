FROM python:3.9
WORKDIR /privy-router
COPY ./requirements.txt /privy-router/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /privy-router/requirements.txt
COPY ./src /privy-router/src
EXPOSE 6130
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "6130"]
