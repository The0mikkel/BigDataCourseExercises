#!/usr/bin/env bash

# Please have context set correctly before running this script

# Clone the helm example, if it does not exist
if [ ! -d "hello-kubernetes" ]; then
	git clone https://github.com/paulbouwer/hello-kubernetes
fi
cd hello-kubernetes || (echo "Could not cd into hello-kubernetes" && exit 1)
echo ""

# Deploy application specified
helm install hello-kubernetes-helm ./deploy/helm/hello-kubernetes
echo ""

# Get status
helm status hello-kubernetes-helm
echo ""

# List the helm releases
helm list
echo ""
kubectl get all
echo ""

# Wait for user input before continuing
read -p "Press enter to continue"
echo ""

# Reapply the helm chart
helm upgrade hello-kubernetes-helm ./deploy/helm/hello-kubernetes --set deployment.replicaCount=5
echo ""

# Wait for user input before continuing
read -p "Press enter to continue"
echo ""

# List the helm releases
helm list
echo ""
kubectl get all
echo ""

# Wait for user input before continuing
read -p "Press enter to continue"

# Remove helm chart
helm uninstall hello-kubernetes-helm 

cd ..

sleep 5
echo ""

# List the helm releases
helm list
echo ""
kubectl get all
echo ""
