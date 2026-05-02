// Grant Management System
// Main JavaScript functionality

// Application state
const AppState = {
    currentFinancialYear: '2026-2027',
    sidebarOpen: true,
    notifications: []
};

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-ZM', {
        style: 'currency',
        currency: 'ZMW',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount).replace('ZMW', 'K');
}

function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-ZM', options);
}

function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 fade-in ${
        type === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
    }`;
    notification.innerHTML = `
        <div class="flex items-center">
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'} mr-2"></i>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Data validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    
    for (const input of inputs) {
        if (!input.value.trim()) {
            input.focus();
            showNotification(`Please fill in the ${input.previousElementSibling.textContent} field`, 'error');
            return false;
        }
    }
    
    return true;
}

// Loading states
function setLoading(element, loading = true) {
    if (loading) {
        element.disabled = true;
        element.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Loading...';
    } else {
        element.disabled = false;
        element.innerHTML = element.getAttribute('data-original-text') || 'Submit';
    }
}

// API helpers
async function apiRequest(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        showNotification(`API Error: ${error.message}`, 'error');
        throw error;
    }
}

// Export functions
function exportToJSON(data, filename) {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function exportToCSV(data, filename) {
    if (!data || data.length === 0) {
        showNotification('No data to export', 'error');
        return;
    }
    
    const headers = Object.keys(data[0]);
    const csvContent = [
        headers.join(','),
        ...data.map(row => headers.map(header => `"${row[header] || ''}"`).join(','))
    ].join('\n');
    
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Print functionality
function printElement(elementId, reportTitle) {
    const element = document.getElementById(elementId);
    const printWindow = window.open('', '_blank');
    
    // Get report title from page or use provided title
    const pageTitle = reportTitle || document.title.split(' - ')[0] || 'Report';
    
    printWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>${pageTitle}</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                table { width: 100%; border-collapse: collapse; margin: 20px 0; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                .header { text-align: center; margin-bottom: 30px; }
                .footer { margin-top: 30px; text-align: center; font-size: 12px; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>${pageTitle}</h1>
                <p>Financial Year: ${AppState.currentFinancialYear}</p>
                <p>Generated: ${new Date().toLocaleDateString()}</p>
            </div>
            ${element.innerHTML}
            <div class="footer">
                <p>Generated by Grant Management System</p>
            </div>
        </body>
        </html>
    `);
    
    printWindow.document.close();
    printWindow.print();
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + S to save (prevent default browser save)
    if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        const activeElement = document.activeElement;
        if (activeElement && activeElement.form) {
            activeElement.form.dispatchEvent(new Event('submit'));
        }
    }
    
    // Escape to close modals
    if (e.key === 'Escape') {
        const modals = document.querySelectorAll('.fixed.inset-0');
        modals.forEach(modal => {
            if (!modal.classList.contains('hidden')) {
                modal.classList.add('hidden');
            }
        });
    }
    
    // Ctrl/Cmd + K for quick search (if implemented)
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        // Implement quick search functionality
    }
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Set initial financial year from URL or default
    const urlParams = new URLSearchParams(window.location.search);
    AppState.currentFinancialYear = urlParams.get('financial_year') || '2026-2027';
    
    // Initialize tooltips
    const tooltipElements = document.querySelectorAll('[title]');
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            // Simple tooltip implementation
        });
    });
    
    // Auto-save draft functionality
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('input', function() {
                // Save to localStorage as draft
                const draftKey = `draft_${form.id}_${input.name}`;
                localStorage.setItem(draftKey, input.value);
            });
        });
    });
    
    console.log('Grant Management System initialized');
});

// Cleanup on page unload
window.addEventListener('beforeunload', function() {
    // Clear any temporary data
    const tempKeys = Object.keys(localStorage).filter(key => key.startsWith('temp_'));
    tempKeys.forEach(key => localStorage.removeItem(key));
});

// Export global functions for use in templates
window.AppState = AppState;
window.formatCurrency = formatCurrency;
window.formatDate = formatDate;
window.showNotification = showNotification;
window.confirmAction = confirmAction;
window.validateForm = validateForm;
window.setLoading = setLoading;
window.apiRequest = apiRequest;
window.exportToJSON = exportToJSON;
window.exportToCSV = exportToCSV;
window.printElement = printElement;
