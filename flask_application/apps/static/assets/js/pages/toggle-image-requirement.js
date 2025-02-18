// Toggle Image Requirement based on Item Type
function toggleImageRequirement() {
    const itemType = document.getElementById('item_type').value;
    const foodImage = document.getElementById('food_image');
    const imageHelpText = document.getElementById('image-help');

    if (itemType.toLowerCase() === 'grocery') {
        foodImage.setAttribute('required', 'required');
        imageHelpText.textContent = 'Image is required when Item Type is Grocery';
        imageHelpText.classList.add('text-danger');
    } else {
        foodImage.removeAttribute('required');
        imageHelpText.textContent = 'Required if Item Type is Grocery';
        imageHelpText.classList.remove('text-danger');
    }
}

// Show Spinner on Form Submission
function handleFormSubmission() {
    const overlay = document.getElementById('loading-overlay');
    // Show overlay spinner
    overlay.style.display = 'flex';
}

// Ensure functionality on DOM Load
document.addEventListener('DOMContentLoaded', () => {
    toggleImageRequirement();
    document.getElementById('item_type').addEventListener('change', toggleImageRequirement);

    const form = document.getElementById('donation-form');
    form.addEventListener('submit', handleFormSubmission);
});
