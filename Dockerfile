FROM python:3.10

EXPOSE 8000

WORKDIR /app
COPY app /app
COPY requirements.txt /app
# RUN  --mount=type=cache,target=/root/.cache \
#     pip3 install -r shared/requirements.txt

RUN  pip3 install -r requirements.txt
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]