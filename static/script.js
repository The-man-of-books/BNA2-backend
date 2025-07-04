document.getElementById('carForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const car = {
        name: document.getElementById('carName').value,
        price: document.getElementById('price').value,
        image: document.getElementById('image').value
    };

    const response = await fetch('/add-car', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(car)
    });

    const result = await response.json();
    alert(result.message);
    window.location.reload();
});