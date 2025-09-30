
## I. Khái niệm

- Là một data warehouse dạng đám mây do Google Cloud cung cấp
- Được thiết kế để xử lý và phân tích big data với tốc độ nhanh, mà không phải lo việc quản lý hạ tầng, máy chủ hay tối ưu cơ sở dữ liệu phức tạp
## II. Đặc điểm chính
- Serverless
- Dùng truy vấn SQL
- Tích hợp được với các dịch vụ khác như Dataflow, Pub/Sub

## III. Các tính nnăng

1. Big Query Hashing Function
	- - Là các **hàm băm** (hash functions) được BigQuery cung cấp để **chuyển đổi một input (chuỗi, số,…) thành một giá trị băm cố định**. Kết quả băm thường là một chuỗi hexa hoặc số, dùng để:
		- Ẩn danh dữ liệu nhạy cảm (ví dụ: email, số điện thoại).
		- Tạo **ID duy nhất** cho bản ghi.
		- Dùng trong **partitioning / clustering** để phân phối dữ liệu đồng đều.
		- Kiểm tra tính toàn vẹn dữ liệu.
2. 
