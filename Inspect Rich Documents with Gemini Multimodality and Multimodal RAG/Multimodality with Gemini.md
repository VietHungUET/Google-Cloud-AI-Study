

Sử dụng Gemini API để làm việc với nhiều loại dữ liệu khác nhau:
 - Text: tạo và trả lời văn bản
 - Image: phân tích hình ảnh, phát hiện đối tượng, đọc biểu đồ, so sánh hình ảnh
 - Video: mô tả nội dung, tìm điểm nổi bật
 - Audio
 - Phân tích codebase. Với các codebase lớn dùng thêm Context caching, cho phép lưu trữ input tokens thường dùng vào một cache riêng biệt. Sau đó khi gửi request tiếp theo, chỉ cần tham chiếu đến cache thay vì gửi lại toàn bộ dữ liệu.
Một số Gemini API: Gemini PRo, Gemini Flash

Gemini Flash được tối ưu cho tốc độ và chi phí thấp, hữu ích với các tác vụ real time, interactive hoặc cần trả lời nhanh. Nó vẫn hỗ trợ multimodal.