function previewImage(event) {
    var input = event.target;
    var reader = new FileReader();
    reader.onload = function(){
        var dataURL = reader.result;
        var img = document.getElementById('uploadedImage');
        img.src = dataURL;
        img.style.display = 'block'; 
    };
    reader.readAsDataURL(input.files[0]);
}