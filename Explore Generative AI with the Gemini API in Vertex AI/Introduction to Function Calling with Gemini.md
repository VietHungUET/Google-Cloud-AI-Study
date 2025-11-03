

Function calling là cơ chế cho phép lập trình viên định nghĩa một mô tả về hàm trong mã nguồn của mình, sau đó truyền mô tả đó cho mô hình ngôn ngữ (LLM) trong yêu cầu gửi đến hệ thống. Mô hình sẽ đọc mô tả, nhận diện hàm nào phù hợp với nội dung đầu vào của người dùng, và trả về tên của hàm cùng các tham số cần thiết để gọi hàm đó.

Điều này giúp chuyển đổi dữ liệu đầu vào không có cấu trúc (ví dụ: câu hỏi bằng ngôn ngữ tự nhiên) thành dữ liệu có cấu trúc (dạng JSON) mà chương trình có thể xử lý được. Nói cách khác, function calling là cầu nối giữa mô hình ngôn ngữ và các chức năng lập trình cụ thể, cho phép AI tự động hóa việc gọi hàm một cách chính xác và có ngữ cảnh.



```
# Bước 1: User hỏi
prompt = "Do you have the Pixel 9 in stock?"
response = chat.send_message(prompt)

# Bước 2: Kiểm tra xem Model muốn gọi function không
if response.function_calls:
    print("Model yêu cầu gọi function:", response.function_calls[0].name)
    # ❌ KHÔNG thể print(response.text) ở đây - chưa có text!
    
    # Bước 3: Gọi API/Database
    api_response = {"sku": "GA04834-US", "in_stock": "yes"}
    
    # Bước 4: GỬI kết quả về Model
    response = chat.send_message(
        Part.from_function_response(
            name="get_product_info",
            response={"content": api_response}
        )
    )
    
    # Bước 5: BÂY GIỜ MỚI có thể print text!
    print(response.text)  # ✅ OK!
    # Output: "Yes, the Pixel 9 (SKU: GA04834-US) is currently in stock!"
```

Sự khác nhau giữa
- client.models.generate_content(): tự động gọi python function, gửi 1 request -> nhận kết quả luôn
- client.charts.create(): tạo chat session. Rồi gửi câu hỏi qua chat .send_message() : Tự gọi function, hỗ trợ hội thoại dài



```
# Task 4.2 Generate a video description
# In this cell, update the prompt to ask Gemini to describe the video URL referenced.
# You can use the documentation at the following link to assist.
# https://cloud.google.com/vertex-ai/docs/generative-ai/multimodal/sdk-for-gemini/gemini-sdk-overview-reference#generate-content-from-video
# https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/inference#sample-requests-text-stream-response
# Video URI: gs://github-repo/img/gemini/multimodality_usecases_overview/mediterraneansea.mp4

prompt = """
What is shown in this video?
Where should I go to see it?
What are the top 5 places in the world that look like this?
"""
video = Part.from_uri(
    file_uri="gs://github-repo/img/gemini/multimodality_usecases_overview/mediterraneansea.mp4",
    mime_type="video/mp4",
)
contents = [prompt, video]

responses = client.models.generate_content(
    model=multimodal_model,
    contents=contents
)

print("-------Prompt--------")
print_multimodal_prompt(contents)

print("\n-------Response--------")
for response in responses:
    print(response.text, end="")
```