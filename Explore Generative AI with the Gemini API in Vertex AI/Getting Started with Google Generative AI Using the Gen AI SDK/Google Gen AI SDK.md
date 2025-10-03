
- Google Gen AI SDK là một thư viện (Software Development Kit) do Google cung cấp, giúp bạn dễ dàng kết nối và sử dụng các mô hình Generative AI (như Gemini). Thay vì phải trực tiếp gọi API phức tạp, SDK đóng vai trò là **giao diện thống nhất** – giúp lập trình viên tích hợp AI vào ứng dụng của mình nhanh hơn, ít lỗi hơn. Ví dụ thay vì phải dùng curl ở các lab trước thì tương tác dễ dàng hơn.
- Phương thức generate_content(): gửi prompt dạng văng bản cho Gemini. Sau khi gọi, lấy nội dung trả lời bằng .text. Ngoài ra có thể gửi thêm PDF, ảnh, audio, video. Nếu file ở trên cloud/storage, truyền trực tiếp URL thông qua Part.from_uri
- Cài đặt system instruction
- Cấu hình bộ lọc an toàn
- Duy trì hội thoại nhiều lượt
- Điều chỉnh dữ liệu trả về: Thay vì để Gemini trả lời tự do, ta có thể ép model sinh dữ liệu theo **schema** (cấu trúc JSON/Pydantic).
- Phương thức generate content stream: Thay vì chờ model trả lời xong mới nhận thì stream kết quả dần dần
- Gửi request bất đồng bộ
- Quản lý chi phí và hiệu năng khi dùng Gemini API dùng count_token và compute token để tính số token trước khi gửi request và sau khi model sinh phản hồi