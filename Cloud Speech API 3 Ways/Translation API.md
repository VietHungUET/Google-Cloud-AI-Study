
- Dịch ngôn ngữ, phát hiện ngôn ngữ
- Dùng API key, lưu vào biến môi trường $API_KEY rồi dùng với curl
- Lệnh translate:
```
TEXT="My%20name%20is%20Steve"
curl "https://translation.googleapis.com/language/translate/v2?target=es&key=${API_KEY}&q=${TEXT}"
```
- Lệnh phát hiện ngôn ngữ:
```
TEXT_ONE="Meu%20nome%20é%20Steven"
TEXT_TWO="日本のグーグルのオフィスは、東京の六本木ヒルズにあります"
curl -X POST "https://translation.googleapis.com/language/translate/v2/detect?key=${API_KEY}" -d "q=${TEXT_ONE}" -d "q=${TEXT_TWO}"
```