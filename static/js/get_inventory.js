async function fetchInventory() {
    const storeId = +$('#storeId').val();
    if (!storeId) {
        $('#message').text('Please enter Store ID.');
        return;
    }
    try {
        const res = await fetch(`/get_inventory/${storeId}`);
        const data = await res.json();
        $('#message').text('');
        if (data.length > 0) {
            $('#inventoryTable').show();
            const tbody = $('#inventoryBody').empty();
            data.forEach(item => {
                tbody.append(
                    `<tr><td>${item.Iname}</td><td>$${parseFloat(item.Sprice).toFixed(2)}</td><td>${item.Scount}</td></tr>`
                );
            });
        } else {
            $('#inventoryTable').hide();
            $('#message').text('No inventory found for this store.');
        }
    } catch(err) {
        console.error(err);
        $('#message').text('Failed to fetch inventory.');
    }
}