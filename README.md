# City's Weather API (Kubernetes ready)

This project contains FastAPI application with Weather API along with Kubernetes config to run in Kubernetes cluster

## Prerequisites

You should have Docker installed.

## Setup

This documentation using `kind` to create and configure cluster with Nginx. You could use your own Ingress controller and cluster.

1. Create a cluster:

```shell
kind create cluster
```

2. Build image and load it into a cluster:

```shell
cd server
docker build -t weather-api:latest .
kind load docker-image weather-api:latest
```

3. Go to `kube_config` directory:

```shell
cd kube_config
```

3. Start Nginx Ingress controller and wait untill it's ready:

```shell
kubectl apply -f deploy-ingress-nginx.yaml
kubectl wait --namespace ingress-nginx \
 --for=condition=ready pod \
 --selector=app.kubernetes.io/component=controller \
 --timeout=90s
```

4. Export your OpenWeather API key to the environment and apply app configuration

```shell
export APP_OWM_API_KEY=<your API key>
envsubst < app.yaml | kubectl apply -f -
```

5. Check that pods are running:

```shell
kubectl get pods -n weather-api
```

6. Add host to your `/etc/hosts` file or similar file on Windows:

```shell
127.0.0.1 weather.local
```

7. Open `http://weather.local/forecast?city=Kyiv` in your browser or use `curl` to check that API is working.
