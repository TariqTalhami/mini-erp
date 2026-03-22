let selectedProductId = null;


// ================= LOAD PRODUCTS WITH STOCK =================
document.addEventListener("DOMContentLoaded", loadProductsWithStock);

async function loadProductsWithStock() {

    // You need an endpoint that returns products + stock
    const response = await fetch("/api/products-with-stock");
    const products = await response.json();

    const tableBody = document.getElementById("products-table-body");
    tableBody.innerHTML = "";

    products.forEach(product => {
        tableBody.innerHTML += `
            <tr onclick="selectProduct(${product.id}, '${product.name}', this)">
                <td>${product.id}</td>
                <td>${product.name}</td>
                <td>${product.type}</td>
                <td>${product.stock}</td>
            </tr>
        `;
    });
}

// ================= SELECT PRODUCT =================
function selectProduct(id, name, rowElement) {

    selectedProductId = id;

    // Update UI
    document.getElementById("selected-product-name").innerText = name;

    // Highlight selected row
    document.querySelectorAll("#products-table-body tr")
        .forEach(row => row.classList.remove("selected-row"));

    rowElement.classList.add("selected-row");

    // Load details
    loadInventoryDetails();
}


// ================= LOAD RIGHT SIDE =================
async function loadInventoryDetails() {

    if (!selectedProductId) return;

    // Load stock
    const stockRes = await fetch(`/api/inventory/${selectedProductId}`);
    const stockData = await stockRes.json();

    document.getElementById("stock-value").innerText = stockData.stock;

    // Load history
    const historyRes = await fetch(`/api/inventory/history/${selectedProductId}`);
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

    if (!selectedProductId) {
        alert("Select a product first");
        return;
    }

    const quantity = parseFloat(document.getElementById("quantity").value);
    const reference = document.getElementById("reference").value || null;

    if (!quantity || quantity <= 0) {
        alert("Enter valid quantity");
        return;
    }

    await fetch("/api/inventory/add", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            product_id: selectedProductId,
            quantity,
            reference_id: reference
        })
    });

    clearInputs();
    reloadAll();
}


// ================= REMOVE STOCK =================
async function removeStock() {

    if (!selectedProductId) {
        alert("Select a product first");
        return;
    }

    const quantity = parseFloat(document.getElementById("quantity").value);
    const reference = document.getElementById("reference").value || null;

    if (!quantity || quantity <= 0) {
        alert("Enter valid quantity");
        return;
    }

    await fetch("/api/inventory/remove", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            product_id: selectedProductId,
            quantity,
            reference_id: reference
        })
    });

    clearInputs();
    reloadAll();
}


// ================= HELPERS =================
function clearInputs() {
    document.getElementById("quantity").value = "";
    document.getElementById("reference").value = "";
}

function reloadAll() {
    loadProductsWithStock();
    loadInventoryDetails();
}