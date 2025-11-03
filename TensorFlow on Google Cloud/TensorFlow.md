
### 1. TensorFlow là gì ?

- TensorFlow là một thư viện mã nguồn mở do Google phát triển dùng để xây dựng các mô hình học máy và mạng nơ ron, tính toán biểu đồ cho các phép toán đại số tuyến tính, tối ưu hóa việc tính toán trên CPU, GPU.
- Một số khái niệm

| Khái niệm                    | Giải thích ngắn gọn                                                                                                |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **Tensor**                   | Là cấu trúc dữ liệu cơ bản, giống như mảng (array) nhiều chiều trong NumPy.                                        |
| **Graph (Đồ thị tính toán)** | Là mô hình của TensorFlow mô tả các phép toán (operation) như các nút, và dữ liệu (tensor) như các cạnh.           |
| **Session (phiên làm việc)** | Là môi trường thực thi đồ thị (graph). Trong TensorFlow 2.x, Session không còn cần thiết vì đã có Eager Execution. |
| **Eager Execution**          | Cho phép chạy lệnh ngay lập tức, giống như code Python thông thường (được bật mặc định từ TensorFlow 2.0).         |
| **Keras**                    | Là API cấp cao của TensorFlow giúp xây dựng mô hình dễ dàng và trực quan hơn.                                      |

- Lệnh cài: pip3 install tensorflow

## 2. Tổng các strategy trong TensorFlow


1. Distributed Training Strategies
	- **OneDeviceStrategy** – chạy trên một thiết bị duy nhất (CPU/GPU).
	- **MirroredStrategy** – song song nhiều GPU trong một máy.
		- TensorFlow **nhân bản (mirror)** toàn bộ mô hình lên **mỗi GPU**.
		- Dữ liệu huấn luyện được **chia nhỏ thành nhiều batch con** (mini-batch) và gửi tới từng GPU.
		- Mỗi GPU thực hiện tính toán  forward pass và backward pass trên phần dữ liệu của mình.
		- Sau mỗi bước huấn luyện (training step), **các GPU đồng bộ hóa gradient** qua mạng nội bộ (thường dùng NCCL hoặc AllReduce).
		- TensorFlow **tổng hợp và cập nhật trọng số đồng nhất** cho tất cả GPU, đảm bảo các bản sao mô hình luôn giống nhau.
	- **MultiWorkerMirroredStrategy** – nhiều máy (multi-node).
	- **TPUStrategy** – chạy trên TPU.
	- **ParameterServerStrategy** – huấn luyện bất đồng bộ.
	- **CentralStorageStrategy** – lưu biến trung tâm, chia dữ liệu cho GPU
2. Training Optimization Strategies: Mixed Precision, Pruning
3. Inference & Deployment Strategies
4. Resource & Execution Strategies: Eager, Graph, Device Placement
5. Optimization & Compression Strategies