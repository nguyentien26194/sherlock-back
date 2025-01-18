# README #

This README would normally document whatever steps are necessary to get your application up and running.

## Deployment

### Login AWS: 

```bash
aws ecr get-login-password --region eu-west-3 | docker login --username AWS --password-stdin 943635619664.dkr.ecr.eu-west-3.amazonaws.com
```

### Backend: 

```bash
docker build -t sherlock-back:1.0.0 -f deployment/production/backend/Dockerfile . && \
docker tag sherlock-back:1.0.0 943635619664.dkr.ecr.eu-west-3.amazonaws.com/sherlock-back:1.0.0 && \
docker push 943635619664.dkr.ecr.eu-west-3.amazonaws.com/sherlock-back:1.0.0
```

### Worker: 

```bash
docker build -t sherlock-worker:1.0.0 -f deployment/production/worker/Dockerfile . && \
docker tag sherlock-worker:1.0.0 943635619664.dkr.ecr.eu-west-3.amazonaws.com/sherlock-worker:1.0.0 && \
docker push 943635619664.dkr.ecr.eu-west-3.amazonaws.com/sherlock-worker:1.0.0
```
"# sherlock-back" 
"# sherlock-back" 
