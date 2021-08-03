FROM python:3.7-stretch
RUN mkdir -p /app && cd /app
WORKDIR /app
COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt
ENTRYPOINT ["python", "-m", "pv_simulator"]
