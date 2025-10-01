

## Các bước thực hiện 

1. Kích hoạt Cloud Natural Language API.
	- Chọn APIs and Services. Chọn  Cloud Natural Language API. Chọn Enaable
2. Tạo API key: Vào Credentials để tạo Credential rồi chọn API key
3. Tạo máy ảo linux. Gõ lệnh export API = ..
4. Tạo một file request.json
 ```
	  {
  "document":{
    "type":"PLAIN_TEXT",
    "content":"A Smoky Lobster Salad With a Tapa Twist. This spin on the Spanish pulpo a la gallega skips the octopus, but keeps the sea salt, olive oil, pimentón and boiled potatoes."
  }
}
```
5.  Gửi tới Natural Language APi classifyText method

```
curl "https://language.googleapis.com/v1/documents:classifyText?key=${API_KEY}" \
  -s -X POST -H "Content-Type: application/json" --data-binary @request.json
```

## Phân loại văn bản lớn

1. Viết script Python đọc từng file .txt từ Cloud Storage
```

from google.cloud import storage, language, bigquery

# Set up your GCS, NL, and BigQuery clients

storage_client = storage.Client()
nl_client = language.LanguageServiceClient()
bq_client = bigquery.Client(project='Project ID')

dataset_ref = bq_client.dataset('news_classification_dataset')
dataset = bigquery.Dataset(dataset_ref)
table_ref = dataset.table('article_data')
table = bq_client.get_table(table_ref)

# Send article text to the NL API's classifyText method

def classify_text(article):
    response = nl_client.classify_text(
        document=language.Document(
            content=article,
            type=language.Document.Type.PLAIN_TEXT
        )
    )
    return response

rows_for_bq = []
files = storage_client.bucket('qwiklabs-test-bucket-gsp063').list_blobs()
print("Got article files from GCS, sending them to the NL API (this will take ~2 minutes)...")

# Send files to the NL API and save the result to send to BigQuery

for file in files:
    if file.name.endswith('txt'):
        article_text = file.download_as_bytes().decode('utf-8')  # Decode bytes to string
        nl_response = classify_text(article_text)
        if len(nl_response.categories) > 0:
            rows_for_bq.append((article_text, nl_response.categories[0].name, nl_response.categories[0].confidence))

print("Writing NL API article data to BigQuery...")

# Write article text + category data to BQ

if rows_for_bq:
    errors = bq_client.insert_rows(table, rows_for_bq)
    if errors:
        print("Encountered errors while writing to BigQuery:", errors)
else:
    print("No articles found in the specified bucket.")


```
2. Tạo service account để authenticate Natural Language API and BigQuery từ  Python script.
	- export PROJECT
	- ```
	  gcloud iam service-accounts create my-account --display-name my-account
gcloud projects add-iam-policy-binding $PROJECT --member=serviceAccount:my-account@$PROJECT.iam.gserviceaccount.com --role=roles/bigquery.admin
gcloud projects add-iam-policy-binding $PROJECT --member=serviceAccount:my-account@$PROJECT.iam.gserviceaccount.com --role=roles/serviceusage.serviceUsageConsumer
gcloud iam service-accounts keys create key.json --iam-account=my-account@$PROJECT.iam.gserviceaccount.com
export GOOGLE_APPLICATION_CREDENTIALS=key.json
	  ```
3. Gửi nội dung của từng bài báo tới API classifyText
4. Nhận kết quả phân loại
5. Lưu kết quả phân loại vào BigQuery để có thể phân tích tiếp
- Ví dụ truy vấn xem chủ đề nào phổ biến nhất
```
SELECT
  category,
  COUNT(*) c
FROM
  `Project ID.news_classification_dataset.article_data`
GROUP BY
  category
ORDER BY
  c DESC
```