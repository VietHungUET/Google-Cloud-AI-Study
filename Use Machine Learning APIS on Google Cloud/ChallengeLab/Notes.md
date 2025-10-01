 - Nhiệm vụ: Xử lý và phân tích dữ liệu ảnh. Các ảnh đều có chữ viết, chữ viết ở bất kỳ ngôn ngữ nào
 - Nhiệm vụ chính: Xây dựng một script Python để:
	 - Đọc ảnh từ bucket
	 - Sử dụng Google Vision API để nhận dạng chữ, lấy ra nội dung text
	 - Với các trường hợp Vision API không nhận diện được ngôn ngữ thì phải dùng Google Translation API để dịch text đó ra tiếng anh
	 - Đưa dữ liệu cuối cùng bào Big query
- Các task cần thực hiện:
1. Cấu hình service account để truy cập ML APIs
2. Tạo và tải file credential cho service account
3. Viết Python script để extract text từ ảnh
4. Viết Python script để translate
5. Sử dụng Big query để tìm ra ngôn ngữ phổ biến nhất