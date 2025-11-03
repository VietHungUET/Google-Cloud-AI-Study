

### 1. Khái niệm

**Kafka** là một nền tảng **phát luồng dữ liệu phân tán (distributed streaming platform)**, được dùng để:
- Gửi (produce), nhận (consume), lưu trữ (store) và xử lý (process) dữ liệu dạng **luồng (stream)**.
- Ứng dụng trong hệ thống **real-time analytics**, **event-driven microservices**, **log processing**, v.v.
4 tính chất của Kafka:
- **High scalable**: Kafka là hệ thống phân tán - distributed system, có khả năng mở rộng rất nhanh và dễ dàng với **zero downtime** - mọi thứ vẫn hoạt động bình thường khi thêm hoặc bớt **broker**.
- **High durable**: message được lưu trên disk, đảm bảo nếu mất điện.. data vẫn còn nguyên. Ngoài ra, một message sẽ có nhiều bản sao lưu trên nhiều **broker** khác nhau, phụ thuộc vào config và set up. Nếu một **broker** die, flow vẫn hoạt động bình thường không bị ngắt quãng.
- **High reliable**: giống **durable**, lưu trữ message ở nhiều nơi. Ngoài ra có cơ chế cân bằng request trong trường hợp gặp sự cố về các **broker**. Đại khái là đáng tin cậy hơn các **message broker** hiện có trên thị trường.
- **High performance**: high throughput cho cả đầu gửi và nhận message với khả năng **scale** tuyệt vời. Nhờ vậy nó có thể xử lý hàng TB data mà không gặp nhiều vấn đề về performance.

![[Pasted image 20251102161155.png]]

- Producer là người gửi message đến mesage broker.
- Message broker được chia ra làm 2 loại
	- Message base: RabbitMQ, ActiveMQ. Lưu trạng thái của Consumer để đảm bảo tất cả đều nhận được message từ topic đang subsribe. Message bị xóa sau khi các Consumer nhận được message.
	- Data pipeline: RocketMQ, Kafka. Không lưu trạng thái của Consumer. Message chưa bị xóa ngay sau khi Consumer nhận message. Consumer có thể tùy ý lựa chọn lấy về một danh sách các message, bao gồm cả message cũ.
- Consummer đọc message từ topic, xác định bằng topic name. Việc đọc message trong một **partition** diễn ra tuần tự để đảm bảo message ordering. Một **consumer** cũng có thể đọc message từ một hoặc nhiều hoặc tất cả **partition** trong một **topic**.
- Topic là luồng dữ liệu của Kafka, một dãy các message nối tiếp nhau. Topic giống nhưu table trong relational database.
- ![[Pasted image 20251102164607.png]]
- Message sau một khoảng thời gian sẽ bị xóa nhưng offset không reset mà tiếp tục tăng
- Data sau khi lưu vào parition là bất biến, không thể thay đổi
- Topic được lưu trữ trên file, trên disk, và tất cả đều được lưu trữ trên server. Và server là một Kafka parition
- **Cách thứ hai**: hardcode, chỉ định partition cho message, thực tế không mấy khi làm như vậy.
- **Cuối cùng**: tự define cơ chế partitioning, routing message bằng cách implement interface **Partitioner**.
![[Pasted image 20251102212548.png]]