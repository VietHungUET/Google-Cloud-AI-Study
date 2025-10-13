
-  Là api cho phép chuyển văn bản thành giọng nói
- Tạo một service account để gọi Text-to-Speech API
- Luồng hoạt động:
	1. Input: Gửi văn bản hoặc SSML (Speech Synthesis Markup Language)
	2. Chọn giọng nói ảo
	3. Cấu hình đầu ra: tùy chọn tốc độ nói, cao độ, định dạng âm thanh
	4. Output: API trả về dữ liệu âm thanh, nội dung gửi được chuyển thành giọng nói tổng hợp
- SSML: ngôn ngữ đánh dấu tổng hợp giọng nói. 

|Thẻ|Chức năng|Ví dụ|
|---|---|---|
|`<speak>`|Thẻ gốc, bắt buộc phải có|`<speak>Xin chào!</speak>`|
|`<break>`|Tạm dừng một chút|`<break time="500ms"/>` (ngừng 0.5 giây)|
|`<emphasis>`|Nhấn mạnh từ|`<emphasis level="strong">rất quan trọng</emphasis>`|
|`<prosody>`|Điều chỉnh tốc độ, cao độ, âm lượng|`<prosody rate="slow" pitch="high">Xin chào</prosody>`|
|`<say-as>`|Quy định cách đọc (ví dụ số, ngày, địa chỉ,...)|`<say-as interpret-as="date">2025-10-13</say-as>`|
|`<p>` / `<s>`|Chia đoạn và câu|`<p>Đoạn 1.</p><p>Đoạn 2.</p>`|
|`<sub>`|Thay thế từ viết tắt bằng cách đọc khác|`<sub alias="World Wide Web">WWW</sub>`|
