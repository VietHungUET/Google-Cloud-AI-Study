

- Kubernetes (K8s) là một nền tảng mã nguồn mở để quản lý container. Nó giúp triển khai, mở rộng, cập nhật và vận hành các ứng dụng chạy trong container tự động
- Một cluster là tập hợp các máy tính(node) mà Kubernetes quản lý.
- Bên trong cluster này, các container sẽ được kết nối với nhau thông qua địa chỉ ip
- Node gồm 2 loại node:
	- Master node: Điều khiển và quản lý toàn bộ cluster. Ra lệnh tạo, xóa, giám sát Pod
	- Worker node: Thực sự chạy các containers
- Mỗi node có thể gồm nhiều pod. Khi Node chết thì Pod chết
- Pod là đơn vị nhỏ nhất trong Kubernetes. Trong mỗi pod quản lý được 1 hoặc nhiều container. Các container trong cùng Pod chia sẻ mạng, chia sẻ volume, chạy trên cùng một Node.
- Service cung địa chỉ cố định cho nhóm Pod.  Bởi Pod chỉ có một IP và nếu Pod chết và được tạo lại, IP thay đổi -> các client khác không thể truy cập ổn định.
- 3 loại Service:

| Loại         | Mô tả                                         |     |
| ------------ | --------------------------------------------- | --- |
| ClusterIP    | Chỉ truy cập nội bộ trong cluster (mặc định). |     |
| NodePort     | Mở cổng trên tất cả Node (ví dụ: `:31000`).   |     |
| LoadBalancer | Tạo Load Balancer ngoài Internet.             |     |
- Service tìm các Pods mục tiêu dựa trên **label selector** (các nhãn mà Service định nghĩa).
- Nếu không có Pod nào có nhãn phù hợp, Service sẽ **không có endpoint** → tức là không có nơi nào để gửi request đến.
- Replicas là phân thân của node
- Rollout là quá trình triển khai phiên bản mới của ứng dụng trong Kubernetes
- Các loại Rollout:

| Loại                      | Mô tả                                                                                                 | Đặc điểm               |
| ------------------------- | ----------------------------------------------------------------------------------------------------- | ---------------------- |
| **Rolling Update**        | Cập nhật dần dần từng Pod (xóa 1 Pod cũ, tạo 1 Pod mới)                                               | Không downtime         |
| **Canary Deployment**     | Chạy song song 2 phiên bản, gửi ít traffic cho phiên bản mới để thử nghiệm                            | Kiểm thử có kiểm soát  |
| **Blue-Green Deployment** | Chạy cả hai phiên bản, nhưng chỉ một phiên bản nhận traffic. Khi sẵn sàng thì chuyển hẳn sang bản mới | Đổi nhanh, rollback dễ |
- **Deployment** trong Kubernetes là một **đối tượng (object)** dùng để **triển khai và quản lý vòng đời của ứng dụng** (các Pod).  Nó giúp bạn:
	- Tự động **tạo, xóa, cập nhật** các Pod khi cần.
	- Đảm bảo luôn có đúng **số lượng bản sao (replica)** đang chạy.
	- Hỗ trợ **rollout** (triển khai bản mới) và **rollback** (quay lại bản cũ khi lỗi).
- Traffic là các yêu cầu đi qua hệ thống.
- Lệnh tạo cluster
```
gcloud container clusters create bootcamp \
  --machine-type e2-small \
  --num-nodes 3 \
  --scopes "https://www.googleapis.com/auth/projecthosting,storage-rw"

```
- Nội dung file deployment
```
# orchestrate-with-kubernetes/kubernetes/deployments/fortune-app-blue.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fortune-app-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fortune-app
  template:
    metadata:
      labels:
        app: fortune-app
        track: stable
        version: "1.0.0"
    spec:
      containers:
        - name: fortune-app
          # The new, centralized image path
          image: "us-central1-docker.pkg.dev/qwiklabs-resources/spl-lab-apps/fortune-service:1.0.0"
          ports:
            - name: http
              containerPort: 8080
...
```
- Lệnh tạo deployment
```

kubectl create -f deployments/fortune-app-blue.yaml
```
- Lệnh tìm hiểu về Deployment
```
kubectl explain deployment

```
- Lệnh mở rộng Deployment
```
kubectl scale deployment fortune-app-blue --replicas=5
```
- Lệnh dừng rolling update
```
kubectl rollout pause deployment/fortune-app-blue
```

- Lệnh kiểm tra trạng thái hiện tại của rollout
```
kubectl rollout status deployment/fortune-app-blue
```
- Lệnh rollback về phiên bản cũ 
```
kubectl rollout undo deployment/fortune-app-blue
```

