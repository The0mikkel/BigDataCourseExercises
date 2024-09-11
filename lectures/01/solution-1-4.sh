#!/usr/bin/env bash

# Please have context set correctly before running this script

# Deploy application specified
kubectl apply -f hello-kubernetes.yaml
echo ""

# Wait for the application to be ready
kubectl wait --for=condition=available --timeout=60s deployment/hello-kubernetes
echo ""

# Open portforward in the background
kubectl port-forward service/hello-kubernetes 8080:8080 &
echo ""

# Display what is running
kubectl get all
echo ""


# Wait for the portforward to be ready
sleep 5
echo "Portforwarding started"
echo ""

# Wait for user input before continuing
read -p "Press enter to continue - You can now access the application at http://localhost:8080"

# Test the application
curl http://localhost:8080
echo ""

# Rescale the application
kubectl scale --replicas=5 deployment/hello-kubernetes
echo ""

# Wait for the application to be ready
kubectl wait --for=condition=available --timeout=60s deployment/hello-kubernetes
echo ""

# Display what is running
kubectl get all
echo ""

# Test the application
curl http://localhost:8080
echo ""
curl http://localhost:8080
echo ""
echo ""

# Rescale the application
kubectl scale --replicas=3 deployment/hello-kubernetes
echo ""

# Wait for the application to be ready
kubectl wait --for=condition=available --timeout=60s deployment/hello-kubernetes
echo ""

# Display what is running
kubectl get all
echo ""

# Test the application
curl http://localhost:8080
echo ""

# Stop the portforward
kill %1
echo ""

# Delete the application
kubectl delete -f hello-kubernetes.yaml
echo ""

# Wait for the application to be deleted
kubectl wait --for=delete deployment/hello-kubernetes

# Display what is running
kubectl get all
echo ""
