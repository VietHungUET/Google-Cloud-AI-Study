- Khác với 2 api kia. api này cần gửi nhiều thông tin cấu hình để biết:
	- File âm thanh gửi có định dạng gì
		- FLAC: nén âm thanh không mất dữ liệu
		- MP3: nén âm thanh có mất dữ liệu
	- Âm thanh thuộc ngôn ngữ nào
	- File nằm ở đâu
 Vì vậy cần tạo một request.json
 ```
 {
  "config": {
      "encoding":"FLAC",
      "languageCode": "en-US"
  },
  "audio": {
      "uri":"gs://cloud-samples-data/speech/brooklyn_bridge.flac"
  }
}

 ```
Sau đó gọi api
```
curl -s -X POST -H "Content-Type: application/json" --data-binary @request.json \
"https://speech.googleapis.com/v1/speech:recognize?key=${API_KEY}" > result.json

```