FROM openjdk:8-jre-alpine

# Install wkhtmltopdf
RUN apk add --no-cache wkhtmltopdf

ENTRYPOINT ["wkhtmltopdf"]

ADD . /SheepFishtest

WORKDIR SheepFishtest/src