
## Các bước thực hiện

1. Tạo API key
2. Tạo Cloud Storage bucket.
	- Điều chỉnh Access Control. Ở đây có 2 lựa chọn
		- Uniform: tất cả object trong bucket chia sẻ chung một mức quyền
		- Fine-grained: mỗi object có thể thiết lập quyền truy cập riêng
	- Tắt Enforec public access prevention
3. Upload ảnh lên bucket. Sau đó điều chỉnh quyền truy cập vào file. Chọn Edit access và chọn Add entry để thêm quyền mới.
4. Tạo request.json từ cloud shell
5. Thực hiện label detection
```
curl -s -X POST -H "Content-Type: application/json" --data-binary @request.json  https://vision.googleapis.com/v1/images:annotate?key=${API_KEY} -o label_detection.json && cat label_detection.json
```
6. Thưc hiện face detection
- Upload ảnh
- Tạo request.json
```
{
  "requests": [
      {
        "image": {
          "source": {
              "gcsImageUri": "gs://PROJECT_ID-bucket/selfie.png"
          }
        },
        "features": [
          {
            "type": "FACE_DETECTION"
          },
          {
            "type": "LANDMARK_DETECTION"
          }
        ]
      }
  ]
}
```
- Call Vision API
```
curl -s -X POST -H "Content-Type: application/json" --data-binary @request.json  https://vision.googleapis.com/v1/images:annotate?key=${API_KEY}
```

7. Thực hiện object localization
- Không chỉ nhận diện trong ảnh có những gì mà còn xác định vị trí của từng đối tượng
- Tạo request.json
```
{
  "requests": [
    {
      "image": {
        "source": {
          "imageUri": "https://cloud.google.com/vision/docs/images/bicycle_example.png"
        }
      },
      "features": [
        {
          "maxResults": 10,
          "type": "OBJECT_LOCALIZATION"
        }
      ]
    }
  ]
}
```
Call the Vision API
```

curl -s -X POST -H "Content-Type: application/json" --data-binary @request.json  https://vision.googleapis.com/v1/images:annotate?key=${API_KEY}
```