async function deleteItem() {
    const iId = +$('#iId').val();
    if (!iId) {
        $('#responseMessage').text('Please enter an Item ID.');
        return;
    }
    if (!confirm('Are you sure you want to delete this item?')) return;
    try {
        const res = await fetch(`/delete_item/${iId}`, { method: 'DELETE' });
        const json = await res.json();
        $('#responseMessage').text(json.message || json.error);
    } catch(err) {
        console.error(err);
        $('#responseMessage').text('Failed to delete item.');
    }
}