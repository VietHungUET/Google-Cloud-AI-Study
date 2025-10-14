
- Đây là dịch vụ Kubernetes được Google quản lý
- Nó giúp dev triển khai, quản lý và mở rộng ứng dụng container dễ dàng mà không phải lo về hạ tầng
- Mọi tài nguyên trong Google Cloud (VM, cluster, storage…) phải nằm trong một khu vực cụ thể — gọi là region (vùng) và zone (khu vực con trong vùng).Khi bạn chưa thiết lập region/zone, lệnh `gcloud container clusters create` không biết nơi nào để tạo cluster.
- Deployment : Quản lý việc triển khai và cập nhật container. Nó định nghĩa ứng dụng gồm bao nhiêu Pod, dùng image nào, cách cập nhật ra sao.
- Service: Tạo một điểm truy cập ổn định để kết nối với tới các Pod.
```
kubectl expose deployment hello-server --type=LoadBalancer --port 8080

```