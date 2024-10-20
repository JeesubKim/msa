# Build docker image for the service

```
$ sudo docker build --network=host .
```

K8S Terminology

- Kubernetes Cluster: A collections of nodes + a master to manage them

- Node: A virtual machine that will run our containers

- Pod: More or less a running container. Technically, a pod can run multiple containers

- Deployment: Moniotrs a set of pods, make sure they are running and restarts them if they crash

- Service: Provides an easy-to-remember URL to access a running container
