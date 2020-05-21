
#### Update ECR Authentication Token
```sh
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 162471567408.dkr.ecr.us-east-1.amazonaws.com
```

#### Deploy, tag and push local image to ECR

```sh
docker build -t resilient-ai-rds .
docker tag resilient-ai-rds:latest 162471567408.dkr.ecr.us-east-1.amazonaws.com/resilient-ai-rds:latest
docker push 162471567408.dkr.ecr.us-east-1.amazonaws.com/resilient-ai-rds:latest
```

#### Run image in container locally

```sh
docker run -t resilient-ai-rds:latest -p 5000:5000
```

#### Access the page

Go to `http://0.0.0.0:5000/` in browser.

