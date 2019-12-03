# trainmodeltrafficsignrecognize
Train model Nhận diện biển báo giao thông sử dụng deep learning
<h2>Yêu cầu:</h2>
<b>Python:</b><br>
<ul>
     <li>python 3.6.9</li>
</ul>
<br>
<b>Packages:</b><br>
<i>*Khuyến khích sử dụng Anaconda 3 tạo một environment mới tên "opencv" để cài tất cả packages như hình</i><br>
<br>
<img src="https://github.com/quangkhoiuit98/trafficsignrecognize/blob/master/static/image/indexguide0.png">
<ul>
    <li>pandas 0.25.2</li>
    <li>numpy 1.17.2</li>
    <li>matplotlib 3.1.1</li>
	  <li>tensorflow 2.0.0</li>
	  <li>opencv 3.4.2</li>
    <li>scikit-image 0.15.0</li>
  	<li>scikit-learn 0.21.3</li>
  	<li>pillow 6.2.1</li>
</ul>
<b>Chuẩn bị input:</b><br>
<ol class="n">
  <li>Tải bộ ảnh input <a href="https://drive.google.com/drive/folders/1VrYO0eTlz4ZDvpiDd8qPiJjFIethaOU1?usp=sharing">tại đây</a></li>
  <li>Copy file Train.zip vào trong thư mục input</li>
  <li>Giải nén</li>
</ol>

<h2>Run project:</h2>
Activate biến môi trường Anaconda 3
<pre>source ospath/anaconda3/anaconda3/bin/activate</pre>
Activate môi trường chứa các packages cần thiết
<pre>conda activate opencv</pre>
Di chuyển đến thư mục chứa project
<pre>cd parentProjectPath/train_model_traffic_sign_recognize-master </pre>
Chạy file main.py trong thư mục main
<pre>python main/main.py</pre>
Sau khi chạy xong chúng ta sẽ được file model.h5 trong thư mục model
<br><br>
<img src="https://github.com/quangkhoiuit98/trainmodeltrafficsignrecognize/blob/master/static/image/guide3.png">

<h2>Lưu ý</h2>
<ul>
    <li>Source code tham khảo bài viết tại link: <a href="https://viblo.asia/p/nhan-dien-bien-bao-giao-thong-gAm5yWQXZdb">Nhận diện biển báo giao thông</a></li>
    <li><p>Một số cấu hình trong file main.py</p>
        <ul>
          <li>inputDirPath : Đường dẫn đến thư mục chứa input</li>
          <li>modelDirPath : Đường dẫn đến thư mục lưu model</li>
          <li>modelName : Tên model sẽ lưu</li>
          <li>epochs : Số lần train model</li>
          <li>classes : Số lớp input = Số tập ảnh train = Số thư mục trong thư mục Train</li>
        </ul>
    </li>
</ul>
