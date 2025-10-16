
- Là dịch vụ cho phép tạo và quản lý máy ảo trên hạ tầng Google
- Trước khi tạo máy ảo cần set region/zone
```
gcloud config set compute/zone Zone
gcloud config set compute/region Region
```
- Có 2 cách tạo VM:
	- Dùng Google Cloud Console: Mở Menu -> Compute Engine -> VM Instances -> Create Instance. Nhớ đặt tên, chỉnh Firewall, chọn machine type và Os, disk size.
	- Tạo bằng dòng lệnh trong Cloud Shell:
	```
	gcloud compute instances create gcelab2 --machine-type=e2-medium --zone=$ZONE

	```
- Lệnh kiểm tra danh sách VM
```
gcloud compute instances list

```
- Lệnh SSH vào VM qua cloud shell
```
gcloud compute ssh gcelab2 --zone=us-east1-c

```
