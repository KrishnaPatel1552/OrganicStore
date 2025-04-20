async function addProduct() {
    const data = {
        vId: +$('#vId').val(),
        Vname: $('#Vname').val(),
        Street: $('#Street').val(),
        City: $('#City').val(),
        StateAb: $('#StateAb').val(),
        ZipCode: $('#ZipCode').val(),
        iId: +$('#iId').val(),
        Iname: $('#Iname').val(),
        Sprice: +$('#Sprice').val(),
        Category: $('#Category').val(),
        sId: +$('#sId').val(),
        Scount: +$('#Scount').val()
    };
    try {
        const res = await fetch('/add_product', {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify(data)
        });
        const json = await res.json();
        $('#responseMessage').text(json.message || json.error);
    } catch(err) {
        console.error(err);
        $('#responseMessage').text('Failed to add product');
    }
}