
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