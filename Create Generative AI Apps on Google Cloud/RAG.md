
Một số cách để cải thiện độ chính xác của model:
1. Mode tunning: Giúp mô hình chính xác hơn cho một nhiệm vụ cụ thể, nhưng chi phí cao và không linh hoạt khi dữ liệu thay đổi
	-  Supervised tunning: dùng dữ liệu có gán nhãn với hàng trăm, hàng nghìn ví dụ
	- Trên Vertex AI, khi chạy supervised tunning, mô hình sẽ học thêm tham số phụ để lưu lại kiến thức.
2. Grounding: Kết nối câu trả lời của mô hình với nguồn thông tin đáng tin cậy  giúp giảm tình trạng hallucination.
	- Grounding response với Google search
	- ![[Pasted image 20251004224005.png]]
	- Khi bật Grounding bằng Google Search, kết quả sẽ có thêm metadat:
		- Source link: Là url tới trang web mà Gemini đã dùng để lấy thông tin
		- Search entry point: không phải là đáp án, mà chỉ là dấu vết cho thấy mô hình đã tìm kiếm cái gì. Khi người dùng click vào, họ sẽ được chuyển đến kết quả tìm kiếm thực tế.
	- Grounding response to your own data with VertexAI Search: áp dụng với data riêng của bạn. Mỗi data stroe chứa một loại dữ liệu(text, hình ảnhl, video). Mỗi data store có nhiều data record tức là đơn vị nhỏ dữ liệu.
3.  Retrieval augmented generation: thay vì để mô hình tự “nhớ” hết kiến thức, ta sẽ **truy xuất dữ liệu liên quan** (retrieval) từ một kho dữ liệu bên ngoài rồi **chèn vào prompt** để mô hình dùng khi sinh câu trả lời (generation).
	1. Người dùng đặt câu hỏi → Hệ thống **retriever** tìm kiếm dữ liệu liên quan từ **data store** (FAQ, knowledge base, database, tài liệu PDF, BigQuery, v.v.).
	2. Các dữ liệu được tìm thấy → được đưa vào **prompt** cùng với câu hỏi gốc.
	3. Foundation model (ví dụ Gemini) dựa vào prompt + dữ liệu bổ sung để tạo ra câu trả lời.
	- RAG tường dùng 2 loại data cho model trong prompt
		- User data
		- Những data khác không có sẵn trong model
	- Vector search: một công cụ thực hiện semantic search