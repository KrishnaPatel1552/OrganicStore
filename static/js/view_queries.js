async function fetchQuery(endpoint) {
    try {
        const res = await fetch(endpoint);
        const data = await res.json();
        $('#message').text('');
        renderTable(data);
    } catch(err) {
        console.error(err);
        $('#message').text('Failed to fetch query results.');
    }
}

function renderTable(data) {
    if (!data.length) {
        $('#resultsTable').hide();
        $('#message').text('No data found.');
        return;
    }
    $('#resultsTable').show();
    const thead = $('#tableHead').empty();
    const tbody = $('#tableBody').empty();
    const headers = Object.keys(data[0]);
    headers.forEach(h => thead.append(`<th>${h}</th>`));
    data.forEach(row => {
        const tr = $('<tr>');
        headers.forEach(h => tr.append(`<td>${row[h]}</td>`));
        tbody.append(tr);
    });
}

$(document).ready(() => { $('#resultsTable').hide(); });