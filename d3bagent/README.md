# D3B Federate

There is the code of D3B Agent It is possibile to instantiate a local version of the d3b agent using flask.

It is recommended to build and run a docker image with the following commands.

## build and run

To build

```
docker build -t d3bagent:latest .

docker-compose build
```

To run

```
docker-compose up
```

After docker compose, d3bfed is available at http://localhost:5001 and the mongo database has a web interface
at http://localhost:8081
