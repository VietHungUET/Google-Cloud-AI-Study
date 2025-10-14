
1. Khởi tạo môi trường, thiếp lập region/zone
2. Tạo cluster 
3. Tải mã nguồn mẫu
```
gcloud storage cp -r gs://spls/gsp021/* .
cd orchestrate-with-kubernetes/kubernetes

```
4. Tạo deployment
```
kubectl create deployment nginx --image=nginx:1.27.0

```
5. Tạo service
```
kubectl expose deployment nginx --port 80 --type LoadBalancer

```

6.  Tương tác với Pod
- Port forwarding: mục đích là ánh xạ ip private của pod thành port của máy cục bộ giúp có thể truy cập từ bên ngoài
```
kubectl port-forward fortune-app 10080:8080

```
- Xem log của Pod:
```
kubectl logs fortune-app

```
- Truy cập bên trong container để kiểm tra
```
kubectl exec -it fortune-app -c fortune-app -- /bin/sh
ping -c 3 google.com
exit

```
7. Mở tường lửa cho Nodeport
```
gcloud compute firewall-rules create allow-fortune-nodeport --allow tcp:31000

```
8. Kiểm tra IP node:
```
gcloud compute instances list
curl -k https://<EXTERNAL_IP>:31000

```
9. Tạo Pod HTTPS và expose ra ngoài thông qua Service loại NodePort
```
kubectl create secret generic tls-certs --from-file tls/
kubectl create configmap nginx-proxy-conf --from-file nginx/proxy.conf
kubectl create -f pods/secure-fortune.yaml

```
10 . Kiểm tra Pod có label
```
kubectl get pods -l "app=fortune-app"
kubectl get pods -l "app=fortune-app,secure=enabled"

```
11. Thêm label
```
kubectl label pods secure-fortune 'secure=enabled'


```

12. Chuyển từ monolithic app sang microservices

- Tạo **auth deployment**:
	- kubectl create -f deployments/auth.yaml 
	- kubectl create -f services/auth.yaml`
    
- Tạo **fortune deployment**:
	- kubectl create -f deployments/fortune-service.yaml
	- kubectl create -f services/fortune-service.yaml`
    
- Tạo **frontend deployment + configmap**:
	- kubectl create configmap nginx-frontend-conf --from-file=nginx/frontend.conf 
	- kubectl create -f deployments/frontend.yaml 
	- kubectl create -f services/frontend.yaml`