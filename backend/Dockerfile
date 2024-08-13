FROM python:3.10.13

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ADD build.sh /build.sh
RUN chmod a+x /build.sh
ENTRYPOINT [ "/build.sh" ]