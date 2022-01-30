FROM python:3.9
WORKDIR /privy-router
COPY ./requirements.txt /privy-router/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /privy-router/requirements.txt
COPY ./app /privy-router/app
EXPOSE 6130
CMD ["python", "app/main.py"]
