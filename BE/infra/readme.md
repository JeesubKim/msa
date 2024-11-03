```
C:\Users\jaysk>kubectl config current-context
minikube
```

```
C:\Users\jaysk>kubectl config get-contexts
CURRENT   NAME             CLUSTER          AUTHINFO         NAMESPACE
          docker-desktop   docker-desktop   docker-desktop
*         minikube         minikube         minikube         default
```

```
C:\Users\jaysk>kubectl config use-context docker-desktop
Switched to context "docker-desktop".
```

```
C:\Users\jaysk>kubectl get node
NAME             STATUS   ROLES           AGE     VERSION
docker-desktop   Ready    control-plane   5m26s   v1.30.2
```

# create pod, get pod information

```
kubectl apply -f post.yaml
kubectl get pods
```

# common kubectl commands

```
docker ps --> kubectl get pods
docker exec -it [container id] [cmd] --> kubectl exec -it [pod_name] -- [cmd]
docker logs [container id] --> kubectl logs [pod_name]
```

```
kubectl delete pod [pod_name]
kubectl apply -f [config file name]
kubectl describe pod [pod_name]
```

# deployment commands

```
kubectl get deployments
kubectl describe deployment [depl name]
kubectl delete deployment [depl name]
```

# Updating the project

1. The deployment must be using the 'latest' tag in the pod spec section
2. Make an update to your code
3. Build the image

```
docker build -t be/post .
```

4. Push the image to docker hub

```
docker push gshopping/be/post
```

5. Run the command

```
kubectl rollout restart deployment [depl_name]
```

# Creating Cluster IP service for two different service and make them communicate

1. Build an image for the Event Bus
2. Push the image to docker hub
3. Create a deployment for Event Bus
4. Create a Cluster IP service for Event Bus and Posts
5. Wire it all up!

# Apply multiple config files at once

```
kubectl apply -f .
```
