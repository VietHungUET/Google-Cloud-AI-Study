
Mỗi máy ảo được khởi tạo với **một ổ đĩa khởi động (boot disk)**, và bạn có thể gắn thêm **persistent disk** – loại ổ đĩa lưu trữ dữ liệu bền vững.

Điểm quan trọng là: **persistent disk tồn tại độc lập với vòng đời của máy ảo**. Nghĩa là, nếu bạn xóa VM, dữ liệu trên persistent disk vẫn còn, trừ khi bạn chọn xóa kèm theo.

Compute Engine có hai loại persistent disk:

- **Standard persistent disk (HDD):** phù hợp cho lưu trữ tuần tự hoặc khối lượng dữ liệu lớn.
    
- **SSD persistent disk:** tốc độ cao hơn, phù hợp với các ứng dụng yêu cầu truy xuất nhanh.

Lệnh tao disk
```
gcloud compute disks create mydisk --size=200GB --zone $ZONE

```
Lệnh gắn persisten disk vào máy ảo
```
gcloud compute instances attach-disk gcelab --disk mydisk --zone $ZONE

```
Một ổ đĩa mới chưa thể dùng ngay, cần tạo hệ thống tập tin
```
sudo mkdir /mnt/mydisk
sudo mkfs.ext4 -F -E lazy_itable_init=0,lazy_journal_init=0,discard /dev/disk/by-id/scsi-0Google_PersistentDisk_persistent-disk-1

```
Sau đó tạo một thư mục để gắn đĩa
```

sudo mkdir /mnt/mydisk
```
Gắn đĩa vào thư mục
```
sudo mount -o discard,defaults /dev/disk/by-id/scsi-0Google_PersistentDisk_persistent-disk-1 /mnt/mydisk

```
Có thể ngăn việc xóa persistne disk khi VM bị xóa bằng 2 cách:
- Cách 1: Bỏ chọn tùy chọn Delete boot disk when instance is deleted khi tạo vM
- Cách 2: Khi dùng lệnh xóa, thêm tùy chọn --keep-disks