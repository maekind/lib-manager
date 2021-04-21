# Event-manager program
FROM python:slim
LABEL maekind.webplayer.name="lib-manager" \
      maekind.webplayer.maintainer="Marco Espinosa" \
      maekind.webplayer.version="1.0" \
      maekind.webplayer.description="Listen for incoming file system change events and webserver requests" \
      maekind.webplayer.email="hi@marcoespinosa.es"

# Change working dir to app and copy requirements
WORKDIR /app
COPY requirements.txt requirements.txt

# Install requirements
RUN pip3 install -r requirements.txt

# Copy application into app dir
#COPY ./src/ ./

# Set working dir to path
ENV PATH="/app:${PATH}"

# Set flask to development mode
ENV FLASK_ENV=development

# Entry command for docker image
ENTRYPOINT [ "lib-manager.py" ]
