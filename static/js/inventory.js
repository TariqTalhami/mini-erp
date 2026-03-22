// Load products when page opens
document.addEventListener("DOMContentLoaded", loadProducts);


// ================= LOAD PRODUCTS =================
async function loadProducts() {
    const response = await fetch("/api/products");
    const products = await response.json();

    const select = document.getElementById("product-select");
    select.innerHTML = "";

    products.forEach(product => {
        select.innerHTML += `
            <option value="${product.id}">
                ${product.name}
            </option>
        `;
    });
}


// ================= LOAD INVENTORY =================
async function loadInventory() {
    const productId = document.getElementById("product-select").value;

    // Get stock
    const stockRes = await fetch(`/api/inventory/${productId}`);
    const stockData = await stockRes.json();

    document.getElementById("stock-value").innerText = stockData.stock;

    // Get history
    const historyRes = await fetch(`/api/inventory/history/${productId}`);
    const history = await historyRes.json();

    const tableBody = document.getElementById("history-table-body");
    tableBody.innerHTML = "";

    history.forEach(item => {
        tableBody.innerHTML += `
            <tr>
                <td>${item.id}</td>
                <td>${item.quantity}</td>
                <td>${item.movement_type}</td>
                <td>${item.reference_id || ""}</td>
                <td>${new Date(item.created_at).toLocaleString()}</td>
            </tr>
        `;
    });
}


// ================= ADD STOCK =================
async function addStock() {
    const productId = document.getElementById("product-select").value;
    const quantity = parseFloat(document.getElementById("quantity").value);
    const reference = document.getElementById("reference").value;

    await fetch("/api/inventory/add", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            product_id: productId,
            quantity: quantity,
            reference_id: reference
        })
    });

    // Refresh data
    loadInventory();
}


// ================= REMOVE STOCK =================
async function removeStock() {
    const productId = document.getElementById("product-select").value;
    const quantity = parseFloat(document.getElementById("quantity").value);
    const reference = document.getElementById("reference").value;

    await fetch("/api/inventory/remove", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            product_id: productId,
            quantity: quantity,
            reference_id: reference
        })
    });

    // Refresh data
    loadInventory();
}