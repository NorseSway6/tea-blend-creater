document.getElementById('id_avatar').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('avatarPreview').src = e.target.result;
        }
        reader.readAsDataURL(file);
    }
});
    
document.getElementById('avatarPreview').addEventListener('click', function() {
    document.getElementById('id_avatar').click();
});