
# Vertex AI 

- ** Định nghĩa: ** Vertex AI là một nền tảng **Machine Learning/AI toàn diện trên Google Cloud**. Nó được thiết kế để hỗ trợ cả quá trình xây dựng, huấn luyện, triển khai và quản lý vòng đời mô hình AI/ML trong cùng một môi trường.
- Một số điểm chính về Vertex AI:
	- **Nền tảng hợp nhất (Unified platform):** Trước đây Google có nhiều dịch vụ riêng lẻ như AI Platform, AutoML,… thì Vertex AI gom tất cả về một nơi, giúp thao tác dễ dàng và đồng bộ.
	- **AutoML + Custom Training:** Hỗ trợ cả huấn luyện tự động (AutoML) cho người không rành ML, và huấn luyện tuỳ chỉnh (Custom Training) khi bạn muốn dùng mô hình/phần cứng riêng.
	- **Quản lý dữ liệu và pipeline:** Tích hợp với BigQuery, Dataflow, Dataproc,… để tiền xử lý dữ liệu. Hỗ trợ **Vertex Pipelines** cho việc xây dựng workflow ML có thể tái sử dụng và theo dõi.
	- **Model Registry & Deployment:** Cung cấp kho lưu trữ mô hình (Model Registry) và triển khai (deployment) với khả năng scale tự động, quản lý phiên bản.
	- **MLOps:** Vertex AI hỗ trợ MLOps, bao gồm theo dõi thí nghiệm (experiments tracking), monitoring hiệu suất mô hình sau khi triển khai, và retraining khi cần.
	- **Tích hợp Generative AI:** Hiện nay Vertex AI cũng tích hợp **Vertex AI Studio** và **Vertex AI Search/Conversation**, cho phép phát triển ứng dụng Generative AI dựa trên các mô hình lớn (LLMs) của Google như **PaLM** hoặc **Gemini**.

## Vertex AI Workbench instance
- Là một **môi trường phát triển tích hợp (IDE) chạy trên cloud** do Google Cloud cung cấp, nằm trong hệ sinh thái **Vertex AI**. Nó cho phép bạn tạo và quản lý notebook Jupyter