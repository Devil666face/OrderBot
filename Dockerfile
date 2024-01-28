FROM python:3.10-bookworm

ENV TOKEN ${TOKEN}
ENV DB ""
ENV ADMIN_ID=446545799
ENV DEPS "wget ca-certificates locales"
ENV APP_NAME orderbot

RUN DEBIAN_FRONTEND=noninteractive \
    apt-get update --quiet --quiet && \
    apt-get upgrade --quiet --quiet && \
    apt-get install --quiet --quiet --yes \
    --no-install-recommends --no-install-suggests \
    ${DEPS} \
    && apt-get --quiet --quiet clean \
    && rm --recursive --force /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8   

WORKDIR ${APP_NAME}

COPY . .

RUN python3 -m venv venv && \
    ./venv/bin/pip install --no-cache-dir -r requirements.txt

CMD ["./venv/bin/python","main.py"]
