async function updatePrice() {
    const iId = +$('#iId').val();
    const newPrice = +$('#newPrice').val();
    if (!iId || !newPrice) {
        $('#responseMessage').text('Please enter Item ID and New Price.');
        return;
    }
    try {
        const res = await fetch(`/update_price/${iId}`, {
            method: 'PUT',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({ Sprice: newPrice })
        });
        const json = await res.json();
        $('#responseMessage').text(json.message || json.error);
    } catch(err) {
        console.error(err);
        $('#responseMessage').text('Failed to update price.');
    }
}