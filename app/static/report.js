function navigateTo(event, path) {
    event.preventDefault(); // Prevent default link behavior
    window.location.href = path;
  }
  
  function validateForm() {
    const urlField = document.getElementById('url');
    const urlPattern = /^(ftp|http|https):\/\/[^ "]+$/;
    if (!urlPattern.test(urlField.value)) {
      alert('Please enter a valid URL.');
      return false;
    }
    document.getElementById('successMessage').style.display = 'block';
    return true;
  }
  
  function resetForm() {
    document.getElementById('reportForm').reset();
    document.getElementById('successMessage').style.display = 'none';
  }