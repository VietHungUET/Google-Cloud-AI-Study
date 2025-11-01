
- Computer vision là một nhánh của TTNT, tập trung vào việc giúp máy tính nhìn và hiểu nội dung từ hình ảnh hoặc video giống như con người
- Nguyên lý hoạt động cơ bản:
	1. Nhận dữ liệu đầu vào
	2. Trích xuất các đặc trưng
	3. Sử dụng các mô hình để nhận diện phân loại, hoặc phát hiện đối tượng
	4. Đưa ra kết quả
- Các bài toán phổ biến trong CV:
	- Image classification: phân loại ảnh (vd: mèo, chó, ô tô).
	- Image classification with localization có thêm bounding box quanh đối tượng
	- **Object detection**: phát hiện vị trí đối tượng trong ảnh (vd: xe, người, biển báo).
	- **Image segmentation**: chia ảnh thành từng vùng ý nghĩa (vd: phân tách đường, xe, người trong ảnh giao thông).
	- Instance segmentation: xác định ranh giới của từng vật thể và gán nhãn cho từng điểm ảnh tương ứng với đối tượng, thậm chí khi các đối tượng cùng loại
	- Semantic segmentation: gán nhãn cho từng pixel nhưng không phân biệt các cá thể cùng loại
	- **Face recognition**: nhận dạng khuôn mặt (bảo mật, xác thực). Một dạng nâng cao của object detection
	- **Pose estimation**: ước lượng tư thế cơ thể người (ứng dụng trong thể thao, game, AR).
	- **OCR (Optical Character Recognition)**: đọc chữ trong ảnh (vd: Google Lens, dịch biển báo).
- Một số công cụ:
	- Pre-built ML APIs
		- Vision API: Đây là một tập hợp các mô hình học máy mạnh mẽ, được cung cấp thông qua các giao thức **REST** và **RPC**. Một ví dụ ứng dụng thực tế: Giả sử các anh chị có các tài liệu văn bản, chẳng hạn như hóa đơn chi phí, cần được phân loại theo loại chi phí. Có thể sử dụng Vision API cho chức năng **OCR** (Nhận dạng ký tự quang học) để "khai thác" văn bản từ các hóa đơn đó và chuyển dữ liệu đã trích xuất vào BigQuery để phân tích. Các tính năng của Vision API:
			- Labeling
			- Classification
			- Object Detection
			- Face Detection
			- OCR
			- Phát hiện tìm kiếm an toàn: Nó cho phép lọc hình ảnh dựa trên bốn yếu tố: nội dung người lớn (adult), y tế (medical), bạo lực (violent), và giả mạo (spoof).
			- Trích xuất văn bản từ ảnh
		- Có 2 cách để gửi ảnh tới Vision API cho việc phát hiện ảnh:
			- Sử dụng base64 encoded image string
			- URL từ Cloud Storage
		- Natural Language API
		- Translation API
	- BigQuery
	- AutoML Vision
	- Custom Models


Extract image code
```
import base64
import json
import os

from google.cloud import pubsub_v1
from google.cloud import storage
from google.cloud import translate_v2 as translate
from google.cloud import vision

vision_client = vision.ImageAnnotatorClient()
translate_client = translate.Client()
publisher = pubsub_v1.PublisherClient()
storage_client = storage.Client()

project_id = os.environ["GCP_PROJECT"]



def process_image(file, context):
    """Cloud Function triggered by Cloud Storage when a file is changed.
    Args:
        file (dict): Metadata of the changed file, provided by the triggering
                                 Cloud Storage event.
        context (google.cloud.functions.Context): Metadata of triggering event.
    Returns:
        None; the output is written to stdout and Stackdriver Logging
    """
    bucket = validate_message(file, "bucket")
    name = validate_message(file, "name")

    detect_text(bucket, name)

    print("File {} processed.".format(file["name"]))
    
## Hàm này trích xuất text từ ảnh sử dụng Cloud Vision API và nó vào queue để thực hiện translate
def detect_text(bucket, filename):
    print("Looking for text in image {}".format(filename))

    futures = []

    image = vision.Image(
        source=vision.ImageSource(gcs_image_uri=f"gs://{bucket}/{filename}")
    )
    text_detection_response = vision_client.text_detection(image=image)
    annotations = text_detection_response.text_annotations
    if len(annotations) > 0:
        text = annotations[0].description
    else:
        text = ""
    print("Extracted text {} from image ({} chars).".format(text, len(text)))

    detect_language_response = translate_client.detect_language(text)
    src_lang = detect_language_response["language"]
    print("Detected language {} for text {}.".format(src_lang, text))

    # Submit a message to the bus for each target language
    to_langs = os.environ["TO_LANG"].split(",")
    for target_lang in to_langs:
        topic_name = os.environ["TRANSLATE_TOPIC"]
        if src_lang == target_lang or src_lang == "und":
            topic_name = os.environ["RESULT_TOPIC"]
        message = {
            "text": text,
            "filename": filename,
            "lang": target_lang,
            "src_lang": src_lang,
        }
        message_data = json.dumps(message).encode("utf-8")
        topic_path = publisher.topic_path(project_id, topic_name)
        future = publisher.publish(topic_path, data=message_data)
        futures.append(future)
    for future in futures:
        future.result()
        

### Hàm này dịch chữ đã trích xuất và cho nó vào queue rồi lưu vào Cloud Storage
def translate_text(event, context):
    if event.get("data"):
        message_data = base64.b64decode(event["data"]).decode("utf-8")
        message = json.loads(message_data)
    else:
        raise ValueError("Data sector is missing in the Pub/Sub message.")

    text = validate_message(message, "text")
    filename = validate_message(message, "filename")
    target_lang = validate_message(message, "lang")
    src_lang = validate_message(message, "src_lang")

    print("Translating text into {}.".format(target_lang))
    translated_text = translate_client.translate(
        text, target_language=target_lang, source_language=src_lang
    )
    topic_name = os.environ["RESULT_TOPIC"]
    message = {
        "text": translated_text["translatedText"],
        "filename": filename,
        "lang": target_lang,
    }
    message_data = json.dumps(message).encode("utf-8")
    topic_path = publisher.topic_path(project_id, topic_name)
    future = publisher.publish(topic_path, data=message_data)
    future.result()
    
    
### Hàm này nhận chữ đã được dich và lưu nó vào cloud storage

def save_result(event, context):
    if event.get("data"):
        message_data = base64.b64decode(event["data"]).decode("utf-8")
        message = json.loads(message_data)
    else:
        raise ValueError("Data sector is missing in the Pub/Sub message.")

    text = validate_message(message, "text")
    filename = validate_message(message, "filename")
    lang = validate_message(message, "lang")

    print("Received request to save file {}.".format(filename))

    bucket_name = os.environ["RESULT_BUCKET"]
    result_filename = "{}_{}.txt".format(filename, lang)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(result_filename)

    print("Saving result to {} in bucket {}.".format(result_filename, bucket_name))

    blob.upload_from_string(text)

    print("File saved.")
```

### 2. CNN

- CNN dùng cho phân loại ảnh gồm 2 phần chính
	- Convolutional Base: Trích xuất các đặc trưng. Vd: Convolution, Pooling, Normalization.
		- Ở các lớp đầu, mạng học cách phát hiện đường thẳng, cạnh, màu sắc, góc cạnh
		- Ở các lớp sâu hơn, mạng học cách nhận biết hình dạng, kết cấu, mô hình phứ tạp hơn như mắt, mũi, bánh xe, cánh chim
	- Dense Head: Phân loại ảnh theo đặc trưng đã trích xuất
		- Các lớp **Fully Connected (Dense)** — kết nối toàn bộ các đặc trưng với đầu ra.
		- Các lớp **Dropout** — giúp giảm overfitting (quá khớp).
		- Một lớp **Softmax** ở cuối — để chuyển đầu ra thành **xác suất phân loại** cho từng lớp.
- Thay vì huấn luyện toàn bộ CNN từ đầu, ta tái sử dụng phần base của một mô hình đã được huấn luyện sẵn, thườn là trên một tập dữ liệu lớn như ImageNet. Sau đó gắn thêm một phần head mới, chưa được huấn luyện, để phân loại theo bài toán cụ thể của mình

Việc trích chọn đặc trưng được thực hiện bới lớp cơ sở gồm các thao tác cơ bản sau
- Lọc hình ảnh cho một tính năng cụ thể( Tích chập)
```
from tensorflow import keras
from tensorflow.keras import layers

model = keras.Sequential([
    layers.Conv2D(filters=64, kernel_size=3), # activation is None
    # More layers follow
])
```
	- Kernel giống một chiếc kính lọc, nó quét qua từng vùng nhỏ của ảnh và tính tổng có trọng số của các pixel. Kernel gíp phát các cạnh, góc, vùng sáng vùng tối.
- Phát hiện đặc điểm đó trong ảnh được lọc (ReLU)
	- Sau khi kernel lọc ảnh, ta thu được feature map có cả giá trị âm và dương. Giá trị dương là vùng có đặc trưng mạnh. Giá trị âm là vùng không có đặc trưng hoặc nhiễu.
- Nén hình ảnh để tăng cường các tính năng(Maximum Pooling)
```
from tensorflow import keras
from tensorflow.keras import layers

model = keras.Sequential([
    layers.Conv2D(filters=64, kernel_size=3), # activation is None
    layers.MaxPool2D(pool_size=2),
    # More layers follow
])
```
![[Pasted image 20251031154113.png]]
- Translation Invariance trong CNN để tránh việc mạng nơ rơn phụ thuộc quá nhiều vào vị trí của đặc trưng trong ảnh thì sử dụgn thêm max pooling để ảnh giảm kích thước, nhưng vẫn giữ được đặc trưng quan trọng nhất
- GlobalAveragePooling2D: Thay thế cho Flattern trong CNN, giúp giảm tham số -> tránh overfitting. Giữ ý nghĩa tổng quát của mỗi feature map. Phổ biến trong các mạng như Inception, ResNet, MobileNet
- Tuy nhiên, để xử lý các đặc trưng phức tạp hơn – như hình dạng hoàn chỉnh của một chiếc xe hơi, đám đông người, hoặc các đường kẻ phức tạp – chúng ta cần lặp lại quy trình này nhiều lần. Các đặc trưng sẽ được tinh chỉnh dần dần khi chúng đi sâu hơn vào mạng nơ-ron, trở nên phức tạp và trừu tượng hơn.
### 3. Sliding window

- Stride: khoảng cách mà cửa sổ trượt di chuyển mỗi bước
- **Hiệu quả của Stride**:
	- Khi stride >1 ở bất kỳ chiều nào, cửa sổ sẽ bỏ qua một số pixel đầu vào ở mỗi bước. Điều này làm giảm kích thước đầu ra (feature map) nhanh hơn, giúp mô hình tính toán nhẹ hơn nhưng có thể mất thông tin quan trọng.
	- **Trong tầng Convolution (Tích chập)**: Thường dùng strides=(1, 1) để đảm bảo chất lượng đặc trưng cao. Tăng stride có nghĩa là bỏ lỡ thông tin giá trị, dẫn đến feature map kém chi tiết hơn.
	- **Trong tầng Maximum Pooling (Pooling Tối đa)**: Thường dùng stride >1, như (2, 2) hoặc (3, 3), để nén dữ liệu hiệu quả (giảm kích thước feature map một nửa hoặc hơn). Tuy nhiên, stride không được lớn hơn kích thước cửa sổ pooling (ví dụ: nếu pool_size=2, stride không vượt quá 2).
	- Lợi ích: Giảm số lượng tham số, tránh overfitting (quá khớp dữ liệu huấn luyện), và làm mô hình nhanh hơn.
- Padding: có 2 lựa chọn là valid hoặc same
	- valid: Cửa sổ ở hoàn toàn bên trong ảnh đầu vào, không thêm đệm bên ngoài
	- same: Có thêm đệm để giữ kích thước
- Receptive field: là tất cả các pixel trong hình ảnh đầu vào mà một neuron cụ thể trong mạng kết nối đến.
- Tầng đầu: Receptive field nhỏ → phát hiện đặc trưng cơ bản (cạnh, màu sắc).
- Tầng sâu: Receptive field lớn → phát hiện đặc trưng cao cấp (vật thể, ngữ cảnh toàn bộ hình ảnh).
- Giúp thiết kế mạng: Nếu receptive field quá nhỏ, mạng không "hiểu" toàn bộ hình; quá lớn có thể mất chi tiết cục bộ.

### 4. Tăng cường dữ liệu (Data augmentation)

Cách tốt nhất để cải thiện mô hình học máy là huấn luyện với nhiều dữ liệu hơn. Nhiều ví dụ giúp mô hình học tốt hơn, nhận biết những đặc điểm quan trọng trong hình ảnh và bỏ qua những thứ không cần thiết. Dữ liệu nhiều giúp mô hình tổng quát hóa tốt hơn (áp dụng cho dữ liệu mới).

Một cách dễ để có thêm dữ liệu là sử dụng dữ liệu hiện có. Chúng ta có thể biến đổi hình ảnh mà vẫn giữ nguyên lớp (class), để mô hình học bỏ qua những biến đổi đó. Ví dụ: Xe hơi hướng trái hay phải vẫn là xe hơi, không phải xe tải. Nếu thêm hình ảnh lật ngang vào dữ liệu huấn luyện, mô hình sẽ học rằng "trái hay phải" không quan trọng.

Ý tưởng chính của tăng cường dữ liệu: Thêm dữ liệu giả nhưng giống thật, giúp mô hình phân loại tốt hơn.

Thường dùng nhiều loại biến đổi cho bộ dữ liệu: xoay hình, điều chỉnh màu sắc/độ tương phản, làm méo hình, v.v., thường kết hợp nhiều loại.

Lưu ý: Không phải biến đổi nào cũng phù hợp cho mọi vấn đề. Quan trọng nhất, đừng làm lẫn lộn các lớp. Ví dụ: Với nhận diện chữ số, xoay hình có thể làm lẫn "9" và "6".