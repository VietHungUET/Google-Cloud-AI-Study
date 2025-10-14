
1. Thiếp lập Compute zone & Region
```
gcloud config set compute/region us-central1
gcloud config set compute/zone us-central1-a

```
2.  Tạo một GKE cluster
```
gcloud container clusters create lab-cluster --machine-type=e2-medium --zone=us-central1-a

```
3. Lấy thông tin xác thực để tương tác với cluster
```
gcloud container clusters get-credentials lab-cluster

```
4. Triển khai ứng dụng container
a. Tạo Deployment
```
kubectl create deployment hello-server --image=gcr.io/google-samples/hello-app:1.0

```
b. Tạo Service để mở cổng ra bên ngoài
```
kubectl expose deployment hello-server --type=LoadBalancer --port 8080

```
c. Kiểm tra Service. Cái external ip là cái có thể dùng để mở trình duyệt
```
kubectl get service

```
d. Xóa cluster
```
gcloud container clusters delete lab-cluster

```