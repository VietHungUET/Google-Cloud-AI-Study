
- Là nền tảng mã nguồn mở cho phép xây dựng, đóng gói và triển khai ứng dụng trong các container
- Container là môi trường riêng biệt và cô lập chứa toàn bộ các thành phần cần thiết để chạy 1 ứng dụng như mã nguồn, thư viện, công cụ hệ thống giúp ứng dụng chạy đồng nhất trên mọi môi -> Giải quyết vấn đề không đồng bộ môi trường lúc test, production,..
    
- Dockerfile là một tập tin văn bản chứa các lệnh hướng dẫn Docker cách **xây dựng (build)** một Docker image. Trong Dockerfile, bạn định nghĩa:
    - Image cơ sở (base image) dùng để phát triển.
    - Các lệnh cài đặt phần mềm, sao chép file, thiết lập biến môi trường,...
    - Lệnh khởi chạy ứng dụng khi container được tạo từ image.

- Dockerfile giúp tự động hóa quá trình tạo image, dễ dàng tái sử dụng và chia sẻ cấu hình.
- Cấu trúc một Dockerfile
```
FROM node:lts
WORKDIR /app    -> Thư mục làm việc của container
ADD . /app      -> Copy mã nguồn thư mục ht vào /ap 
EXPOSE 80       -> Cho phép container mở cổng 80
CMD ["node", "app.js"] -> Khi khởi động, chạy lệnh

```
    
- Docker Compose là công cụ để **định nghĩa và chạy nhiều container Docker cùng lúc** thông qua một file cấu hình (thường là **`docker-compose.yml`**). Nó giúp bạn:
    - Mô tả các dịch vụ (services), mạng (networks), và volume cần thiết cho ứng dụng đa container.
    - Khởi động, dừng, và quản lý toàn bộ hệ thống container chỉ với một lệnh duy nhất.
    - Phù hợp với các ứng dụng microservices hoặc ứng dụng có nhiều thành phần phụ thuộc lẫn nhau.

- Các lệnh docker
	- docker run tên image:  chạy container từ image đó
	- docker build -t <tên và tag cho image> : tạo image có tên và tag
	- docker run -p 4000:80 -- name < tên container>: ánh xạ cổng 4000 trên máy host sang cổng 80 trong container
	- docker ps: xem các container đang chạy
	- docker stop: dừng
	- docker rm <tên container>: xóa container
	- docker exec -it <tên container>: mở shell trong container

Push Image lên Google Artificat Registry
- Tạo repository
```
gcloud artifacts repositories create my-repository \
    --repository-format=docker \
    --location=REGION \
    --description="Docker repository"

```
- Cấu hình xác thực
```
gcloud auth configure-docker REGION-docker.pkg.dev

```
- Tag image
```
docker tag node-app:0.2 REGION-docker.pkg.dev/PROJECT_ID/my-repository/node-app:0.2

```
- Push image
```
docker push REGION-docker.pkg.dev/PROJECT_ID/my-repository/node-app:0.2

```
- Pull và chạy image từ registry
```
docker run -p 4000:80 -d REGION-docker.pkg.dev/PROJECT_ID/my-repository/node-app:0.2

```