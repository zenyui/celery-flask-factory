# kubernetes-testing

Guides:
- [celery application pattern](https://gist.github.com/albarrentine/1326477)
- [local docker images](https://gist.github.com/coco98/b750b3debc6d517308596c248daf3bb1)
- [set kubectl cred](https://cloud.google.com/sdk/gcloud/reference/container/clusters/get-credentials)
- [deploy to pool](https://stackoverflow.com/questions/40154907/kubernetes-assign-pods-to-pool)
- [gorgias kuberenetes](http://blog.gorgias.io/deploying-flask-celery-with-docker-and-kubernetes/)
- [k8 secrets](https://kubernetes.io/docs/tasks/inject-data-application/distribute-credentials-secure/#create-a-pod-that-has-access-to-the-secret-data-through-environment-variables)
- [GCP K8 Load Balancing](https://cloud.google.com/kubernetes-engine/docs/tutorials/http-balancer)
- [K8 TLS](https://kubernetes.io/docs/concepts/services-networking/ingress/#tls)
- [K8 GCE Ingress Annotations](https://github.com/kubernetes/ingress-gce/blob/master/docs/annotations.md)
- [K8 Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/#name-based-virtual-hosting)
- [Ingress example](https://daemonza.github.io/2017/02/13/kubernetes-nginx-ingress-controller/)
- Medium Guides:
  - [Full Ingress Example](https://medium.com/@gokulc/setting-up-nginx-ingress-on-kubernetes-2b733d8d2f45)
  - [Intro to Ingress](https://medium.com/@cashisclay/kubernetes-ingress-82aa960f658e)

Notes:
- To get a temporary shell in cluster:
  - `kubectl run --image=ubuntu --restart=Never -i --tty ubuntu -- bash`
  - `kubectl delete pod ubuntu`
- Run shell on running busybox
  - `kubectl exec -it [POD-NAME] -c [CONTAINER-NAME] /bin/sh`
- To apply gcloud security to local kubectl:
  - `gcloud container clusters get-credentials funnel-api`
  - `kubectl config get-contexts`
  - `kubectl config use-context CONTEXT_NAME`
- To expose NodePort:
  - `ubectl expose deployment funnel-api --target-port=8080  --type=NodePort`
- To provision static ip:
  - `gcloud compute addresses create [IP_NAME] --global`
