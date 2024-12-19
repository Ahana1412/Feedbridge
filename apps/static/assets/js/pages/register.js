// handles role based field display

document.addEventListener('DOMContentLoaded', function () {
    const roleSelector = document.getElementById('role_selector'); // Dropdown for role selection
    const fields = {
        donor: document.getElementById('donor_fields'), // Donor-specific fields container
        food_bank: document.getElementById('food_bank_fields'), // Food bank-specific fields container
        volunteer: document.getElementById('volunteer_fields'), // Volunteer-specific fields container
    };

    function toggleFields() {
        const selectedRole = roleSelector.value; // Get selected role

        // Hide all role-specific fields initially
        Object.values(fields).forEach(fieldSet => {
            fieldSet.style.display = 'none';
            // Remove 'required' attribute for all fields inside the hidden container
            fieldSet.querySelectorAll('[required]').forEach(input => {
                input.removeAttribute('required');
            });
        });

        // Show fields for the selected role and add 'required' to the visible fields
        if (fields[selectedRole]) {
            fields[selectedRole].style.display = 'block';
            fields[selectedRole].querySelectorAll('input, select').forEach(input => {
                input.setAttribute('required', true);
            });
        }
    }

    // Attach event listener to the role selector dropdown
    roleSelector.addEventListener('change', toggleFields);

    // Call toggleFields on page load to handle pre-filled values (if any)
    toggleFields();
});
