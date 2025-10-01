

1. Tạo API key
2. Tạo request.josn gồm đoạn text để API trích xuất các entity như tên người, địa danh,..
3. Gọi API analyzeEntites
4. Với sentiment analysis thì gửi nội dung thành 1 đoạn mang cảm xúc rõ ràng.
	- Gọi API analyzeSentiment
```

{
  "document": {
    "type": "PLAIN_TEXT",
    "content": "Harry Potter is the best book. I think everyone should read it."
  },
  "encodingType": "UTF8"
}
```

- Nếu phả hồi score từ -1 tới 1 với dương là tích cực, âm là tiêu cực
5. Phân tích cú pháp và từ loại
	- Gọi API analyzeSyntax
	- Nó sẽ thực hiện chia nhỏ token và cho biết:
		- loại từ
		- quan hệ cú pháp với các từ
		- lemma hay dạng gốc của từ
	- Nhận được phản hồi cho từng token
6. 