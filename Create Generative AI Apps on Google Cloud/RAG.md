
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
	- Vector search: một công cụ thực hiện semantic search. Biểu diễn văn bản/hình ảnh/audio/... dưới dạng vector (mảng số) gọi là _embeddings_. Các vector này mã hóa ý nghĩa — vector gần nhau nghĩa là nội dung gần nghĩa.  Các bước của quy trình vector search:
		- Encode - tạo embedding: Dùng model embedding (text-only hoặc multimodal) để chuyển mỗi document hoặc đoạn văn thành vector. Lưu kèm metadata cho document (id, title, url, thuộc tính khác) để có thể hiển thị nguồn sau khi tìm được vector phù hợp. Với các tài liệu dài thì cần chia thành các chunk rồi embed từng chunk
```
# import embedding libraries
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel

# choose your embedding model
# for example, textembedding-gecko or multimodalembedding
model = TextEmbeddingModel.from_pretrained(model_name)

# create object input (example embeds single text string, but could create list)
text_embedding_input = TextEmbeddingInput(
    task_type="RETRIEVAL_DOCUMENT",
    title=doc_id,
    text=text)

# get embeddings for list of text inputs
embeddings = model.get_embeddings([text_embedding_input])
```
-  Index the data: Sau khi đã có embedding thì cần lưu và tổ chức chúng trong một cấu trúc đặc biệt gọi là index. Index sẽ giúp tìm các vector gần nhất nhanh và chính xác mà không phải so sánh từng vector môt. Sử dụng thuật toán ScaNN( Sclable Nearest Neighbor Search)
	- Cách ScaNN hoạt động:
		1. Phân cụm vector (Clustering): Tập vector sẽ được phân chia thành nhiều nhóm bằng kỹ thuật clustering ví dụ như K-means
		2. Tạo index: Mỗi cụm được lưu kèm vector đại diện và danh sách vector con của nó.
		3. Tìm kiếm nhanh: Khi có một vectory truy vấn. Sẽ tính khoảng cách giữa query vector và các vector đại diện của mỗi nhóm. Chọn ra một vài nhóm gần nhất. Trong những nhóm được chọn, tìm các vector thật sự gần nhất.
- Search the data: Dùng embedding api để tạo vector embedding từ query. Tìm kiếm trong không gian vector. Khi đã có danh sách các vector gần, có thể sắp xếp lại dựa trên khoảng cách chính xác. Lọc thêm các thuộc tính của dữ liệu


- Augmenting the prompt: Đưa kết quả đã tìm được vào prompt, rồi gửi toàn bộ prompt đó cho mô hình LLM để mô hình sinh ra câu trả lời chính xác, có dẫn chứng.
```
You are a chatbot agent answering customer support questions in chat.  
**Your task is to answer customer questions using the data provided in the <DATA> section.****- The current date is located in <CURRENTDATE>.  
- The customer's chat history is located in <CHATHISTORY>.  
- Each separate day's chat is in a block that includes the date and resembles <CHAT date="2024/06/01">.  
- Each separate chat message is specified in a block with tag <USER> or <BOT>, depending upon the source of the chat message.  
- Documents that may be useful in answering are located in <DOCS>.  
- Each separate document is in a block that includes a title and URL. The block tag resembles <DOC title="TITLE" URL="https://example.com/...">.**  
  
**<DATA>**  
**<CURRENTDATE>2024/06/01</CURRENTDATE>****  
<CHATHISTORY>  
<CHAT date="2024/05/24"><USER>...</USER><BOT>...</BOT></CHAT>  
...  
</CHATHISTORY>  
<DOCS>  
<DOC title="Resetting your password" URL="https://example.com/docs/U4A22">  
Follow these instructions to reset your password...  
</DOC>**  
**...  
</DOCS>  
</DATA>  
**  
INSTRUCTIONS:  
1. If there is no data to help answer the question, respond with "I do not have this information. Please contact customer service."  
2. You may ask a follow up question if it helps determine the information to return.  
3. All support recommendations must be taken from these documents, and you must return the title and URL of any documents used in the answer.  
  
QUESTION: **I failed login too many times and I am locked out of my account. Please help!**  
ANSWER:

```
![[Pasted image 20251005115447.png]]

Các bước cụ thể trong Data ingestion flow:
1. Data upload: upload lên Cloud Storage bucket
2.  Khi data được upload, một thông báo sẽ được gửi tới Pub/Sub
3. Khi Pub/Sub phát hiện file mới được tải lên, nó sẽ gửi một thông điệp để kích hoạt CloudRun.
4. Trích xuất dữ liệu từ database
5. CloudRun sử dụng Document AI để chuẩn bị data. Ví dụ như chuyển đổi dữ liệu thành format yêu cầu, chia dữ liệu các chunk
6. CloudRun sử dụng Vertex AI Embedding cho Text model để tạo vector embedding
7. Lưu embedding vào database

Các bước cụ thể trong Serving process:
1. User gửi request tới app qua frontend
2. Generative AI app sử dụng embedding models (data ingestion subsystem) để chuyển request thành embedding
3. App thực hiện tìm kiếm ngữ nghĩa cho embedding được lưu trữ trong data ingestion subsystem. App sẽ kết reuqest gốc và dữ liệu trích xuất được thông qua matching embedding để tạo một promt mới.
4. Gửi prompt mới cho LLM
5. LLM sẽ gửi phản hồi
6. App có thế lưu log request response hoạt động  trong Cloud Logging. Có thể dùng thêm Cloud Monitoring để giám sát
7. App sẽ gửi response tới BigQuery để phân tích
8. Dùng thêm các bộ lọc an toàn
9. Trả về kết quả cho user qua frontend

Các bước cụ thể trong Quality evaluation subsytem
1.  Quá trình sẽ được kích hoạt khi gửi Pub/sub message tới Pub/Sub topic
2. Pub/Sub sẽ kích hoạt Cloud Run
3. Cloud Run thực hiện sử dụng dữ liệu đã được lưu trữ trong database
4. Cloud Run lấy promts để đánh giá từ database. Prompt này được upload lên database trong quá trình data ingestion
5. Cloud Run sử dụng prompt để đánh giá chấy lượng phản hồi mà serving subsystem tạo ra. Output đánh giá là thông số điểm chính xác và mức độ liên quan
6. Lưu trữ scrote và prompt và response vào BigQuery.