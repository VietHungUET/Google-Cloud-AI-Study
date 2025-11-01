import os, warnings
import matplotlib.pyplot as plt
from matplotlib import gridspec

import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image_dataset_from_directory
from tensorflow import keras
from tensorflow.keras import layers

import pandas as pd

# Reproducability Đảm bảo rằng kết quả thí nghiệm có thể được lặp lại chính xác, sử dụng seed
def set_seed(seed=31415):
    np.random.seed(seed)
    tf.random.set_seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    os.environ['TF_DETERMINISTIC_OPS'] = '1'
set_seed(31415)

# Set Matplotlib defaults
plt.rc('figure', autolayout=True)
plt.rc('axes', labelweight='bold', labelsize='large',
       titleweight='bold', titlesize=18, titlepad=10)
plt.rc('image', cmap='magma')
warnings.filterwarnings("ignore") # to clean up output cells


# Load training and validation sets. Đây là phân loại nhị phân chỉ có truck và car
ds_train_ = image_dataset_from_directory(
    '../input/car-or-truck/train',
    labels='inferred',
    label_mode='binary',
    image_size=[128, 128],
    interpolation='nearest',
    batch_size=64,
    shuffle=True,
)

ds_valid_ = image_dataset_from_directory(
    '../input/car-or-truck/valid',
    labels='inferred',
    label_mode='binary',
    image_size=[128, 128],
    interpolation='nearest',
    batch_size=64,
    shuffle=False,
)

# Data Pipeline. Đưa các giá trị pixel từ dải 0-255 về dải 0.0-1.0
def convert_to_float(image, label):
    image = tf.image.convert_image_dtype(image, dtype=tf.float32)
    return image, label
# Pipeline này có dùng cache để lưu sau lần duyệt đầu tiên. Giúp tăng tốc độ cho các epoch huấn luyện tiếp theo. Ngoài ra dùng
# prefetch để nạp dữ liệu song song với việc huấn luyện mô hình
AUTOTUNE = tf.data.experimental.AUTOTUNE
ds_train = (
    ds_train_
    .map(convert_to_float)
    .cache()
    .prefetch(buffer_size=AUTOTUNE)
)
ds_valid = (
    ds_valid_
    .map(convert_to_float)
    .cache()
    .prefetch(buffer_size=AUTOTUNE)
)


pretrained_base = tf.keras.models.load_model(
    '../input/cv-course-models/cv-course-models/vgg16-pretrained-base',
)
# Đóng băng các trọng số của mô hình đã huấn luyện trước để không bị cập nhật trong quá trình huấn luyện. 
# Phần head là mới hoàn toàn -> các trọng số trong head ngẫu nhiên. Khi backpropagation diễn ra, gradient từ head truyền ngược vào base
# Các trọng số trong base bị thay đổi mạnh nên ta cần đóng băng chúng lại.
pretrained_base.trainable = False

# Định nghĩa mô hình bằng cách thêm các lớp phân loại phía trên mô hình đã huấn luyện trước
# Sử dụng hàm kích hoạt relu cho lớp ẩn và sigmoid cho lớp đầu ra để phân loại nhị phân
# Relu là một hàm kích hoạt phí tuyến.Công thức của relu là f(x) = max(0, x). Lí do chọn relu là vì nó giúp mô hình học nhanh hơn và giảm thiểu vấn đề gradient biến mất.
# Sigmoid là một hàm kích hoạt tuyến tính. Công thức của sigmoid là f(x) = 1 / (1 + exp(-x)). Lí do chọn sigmoid là vì nó giúp mô hình đưa ra xác suất cho mỗi lớp trong phân loại nhị phân.
model = keras.Sequential([
    pretrained_base,
    layers.Flatten(),
    layers.Dense(6, activation='relu'),
    layers.Dense(1, activation='sigmoid'),
])


# Biên dịch mô hình. Sử dụng hàm mất mát binary_crossentropy vì đây là phân loại nhị phân
# Sử dụng Adam optimizer để tối ưu hóa mô hình. Bộ tối ưu hóa chịu trách
# nhiệm cập nhật trọng số của mô hình dựa trên gradient của hàm mất mát
# Sử dụng binary_accuracy để đánh giá hiệu suất của mô hình trong việc phân loại đúng
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['binary_accuracy'],
)



history = model.fit(
    ds_train,
    validation_data=ds_valid,
    epochs=30,
    verbose=0,
)

history_frame = pd.DataFrame(history.history)
history_frame.loc[:, ['loss', 'val_loss']].plot()
history_frame.loc[:, ['binary_accuracy', 'val_binary_accuracy']].plot();