// File upload preview
document.addEventListener('DOMContentLoaded', function() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const fileName = e.target.files[0]?.name;
            const preview = input.parentElement.querySelector('.file-preview');
            if (preview) {
                preview.textContent = fileName || 'No file selected';
            }
        });
    });
});

// Flash message auto-hide
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('[role="alert"]');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 300);
        }, 5000);
    });
});

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;

    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            field.classList.add('border-red-500');
            
            const errorMessage = field.parentElement.querySelector('.error-message');
            if (!errorMessage) {
                const error = document.createElement('p');
                error.className = 'error-message';
                error.textContent = 'This field is required';
                field.parentElement.appendChild(error);
            }
        } else {
            field.classList.remove('border-red-500');
            const errorMessage = field.parentElement.querySelector('.error-message');
            if (errorMessage) {
                errorMessage.remove();
            }
        }
    });

    return isValid;
}

// Loading state handler
function showLoading(buttonId) {
    const button = document.getElementById(buttonId);
    if (button) {
        button.disabled = true;
        button.innerHTML = '<svg class="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24"></svg>Loading...';
    }
}

// AI Tool response handlers
function handleAIResponse(response, outputId) {
    const outputElement = document.getElementById(outputId);
    if (outputElement) {
        outputElement.innerHTML = response;
        outputElement.scrollIntoView({ behavior: 'smooth' });
    }
}