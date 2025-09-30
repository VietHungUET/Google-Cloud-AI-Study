


## Khái niệm
- Pipeline là một chuỗi các bước (steps) trong quy trình học máy (ML workflow), được tự động hóa và sắp xếp theo thứ tự nhất định.
- Kubeflow Pipeline SDK là một nền tảng mã nguồn mở cho  ML workflow. Khi kết hợp với Vertex AI, có thể tận dụng khả năng mở rộng và hạ tầng mạnh mẽ của Google Cloud
- Google Cloud Pipeline Components: là 1 thư viện cung cấp các pre-build component giúp tương tác dễ dàng với cách dịch vụ của Vertex AI từ pipeline của bạn.
- **Vì sao cần pipelines**:
	- Một workflow ML thường gồm nhiều bước: xử lý dữ liệu, huấn luyện, tinh chỉnh siêu tham số, đánh giá, triển khai.
	- Nếu làm tất cả trong một khối lớn (monolith) sẽ rất khó quản lý, đặc biệt khi làm việc nhóm.
	- Với pipeline, mỗi bước là một **container riêng biệt** → dễ phát triển độc lập, dễ kiểm soát đầu vào/đầu ra, và đảm bảo có thể tái sử dụng/lặp lại.
	- Ngoài ra, pipeline có thể tự động chạy khi có dữ liệu mới hoặc theo lịch định sẵn.