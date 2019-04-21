function upload() {
  let file = document.getElementById('picture').files[0];
  let image = document.getElementById('image');
  let reader = new FileReader();
  reader.onload = function () {
    image.src = reader.result;
  };
  reader.readAsDataURL(file);
}