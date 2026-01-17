function setupAlerts() {
    document.querySelectorAll('.alert .btn-close').forEach(button => {
        button.addEventListener('click', function() {
            this.closest('.alert').remove();
        });
    });
    
    setTimeout(() => {
        document.querySelectorAll('.alert').forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
}

document.addEventListener('DOMContentLoaded', function() {
    setupAlerts();
});

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { setupAlerts };
}