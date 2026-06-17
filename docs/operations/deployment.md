# ReconX Deployment Guide

## Prerequisites
- Docker & Docker Compose
- PostgreSQL 15+

## Deployment via Docker Compose (Recommended for single-node)

1. Clone the repository
2. Set up the `.env` file based on `.env.example`
3. Run the following command:
```bash
docker compose -f deployment/compose/docker-compose.yml up -d
```

## Kubernetes Deployment

1. Apply the ConfigMap:
```bash
kubectl apply -f deployment/kubernetes/configmap.yaml
```
2. Apply the Service and Deployment:
```bash
kubectl apply -f deployment/kubernetes/deployment.yaml
kubectl apply -f deployment/kubernetes/service.yaml
```
3. Apply the Ingress:
```bash
kubectl apply -f deployment/kubernetes/ingress.yaml
```
