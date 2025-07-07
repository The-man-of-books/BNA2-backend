document.getElementById('carForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append('year', document.getElementById('year').value);
    formData.append('make', document.getElementById('make').value);
    formData.append('description', document.getElementById('description').value);
    formData.append('price', document.getElementById('price').value);
    formData.append('imageFile', document.getElementById('image').files[0]); // ✅ match Flask

    try {
        const response = await fetch('/add_car', { // ✅ match Flask route
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Failed to submit car data');
        }

        // Since Flask redirects, you won't get JSON here — just reload
        window.location.href = '/dashboard';
    } catch (error) {
        console.error('Error:', error);
        alert('Something went wrong. Please try again.');
    }
});