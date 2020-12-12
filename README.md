# City's Weather API (Kubernetes ready)

This project contains FastAPI application with Weather API along with Kubernetes config to run in Kubernetes cluster

## Prerequisites
You should have Docker installedand Kubernetes cluster up and running.

## Setup
1. Build Docker image and push it to some Docker registry (e. g. local docker registry)
2. Change `kube_config/owm-credentials.yaml` and insert your key to [Open Weather Map API](https://openweathermap.org/)
3. Change `kube_config/app.yaml:Deployment` with your container name with address of registry
4. Run `kubectl apply -f app.yaml`
5. Now you have Service and Deployments up and running on `weather-api:8000`. You could use port-forwarding to make it enable on your local computer, or setup Ingress controller with Nginx-Ingress or use any other setup for this. To enable port-forwarding, use Makefile command in `kube_config` - `make port-forward`.
