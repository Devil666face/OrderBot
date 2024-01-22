FROM python:3.10-bookworm

ENV TOKEN ${TOKEN}
ENV DB ""
ENV ADMIN_ID=446545799
ENV DEPS "wget ca-certificates"
ENV APP_NAME orderbot

WORKDIR ${APP_NAME}

COPY . .

RUN python3 -m venv venv && \
    ./venv/bin/pip install --no-cache-dir -r requirements.txt

CMD ["./venv/bin/python","main.py"]
