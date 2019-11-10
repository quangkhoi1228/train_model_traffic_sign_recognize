# trainmodeltrafficsignrecognize
Train model Nhận diện biển báo giao thông sử dụng deep learning
<h2>Yêu cầu:</h2>
<b>Python:</b><br>
<ul>
     <li>python 3.6.9</li>
</ul>
<br>
<b>Packages:</b><br>
<i>*Khuyến khích sử dụng Anaconda 3 để cài tất cả packages</i><br>
<ul>
    <li>notebook 6.0.1</li>
    <li>pandas 0.25.2</li>
    <li>numpy 1.17.2</li>
    <li>matplotlib 3.1.1</li>
	<li>tensorflow 2.0.0</li>
	<li>opencv 3.4.2</li>
    	<li>scikit-image 0.15.0</li>
	<li>scikit-learn 0.21.3</li>
	<li>pillow 6.2.1</li>
</ul>
<i>Lưu ý: phiên bản tensorflow 2.0.0 đã chứa cả packages keras, nên khi cài cả hai có thể gây lỗi "dead kernel ..."</i>
<b>Chuẩn bị input:</b><br>
<ol class="n">
  <li>Tải bộ ảnh input <a href="https://drive.google.com/drive/folders/1VrYO0eTlz4ZDvpiDd8qPiJjFIethaOU1?usp=sharing">tại đây</a></li>
  <li>Copy file Train.zip vào trong thư mục input</li>
  <li>Giải nén</li>
</ol>

<br>
<p>Source code thao khảo bài viết tại link: <a href="https://viblo.asia/p/nhan-dien-bien-bao-giao-thong-gAm5yWQXZdb">Nhận diện biển báo giao thông</a></p>

<h2>Run project:</h2>
Chạy Jupiter NoteBook với start folder là thư mục chứa Project train model
<pre>jupyter notebook --notebook-dir=ParentProjectDir/trainmodeltrafficsignrecognize/</pre>
Chọn thư mục main trong list
<img src="https://github.com/quangkhoiuit98/trainmodeltrafficsignrecognize/blob/master/static/image/guide1.png">
Chọn file main.ipynb
<img src="https://github.com/quangkhoiuit98/trainmodeltrafficsignrecognize/blob/master/static/image/guide2.png">
Sau khi chạy file main.ipynb chúng ta sẽ được file model.h5 trong thư mục model
<img src="https://github.com/quangkhoiuit98/trainmodeltrafficsignrecognize/blob/master/static/image/guide3.png">
