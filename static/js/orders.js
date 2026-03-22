// Load everything on page load
document.addEventListener("DOMContentLoaded", async () => {
    loadOrders();
    loadCustomers();
    loadProducts();
    await loadProducts();
    addItemRow(); // start with one row
});

// Store products globally for dropdown reuse
let products = [];

// =======================
// LOAD ORDERS LIST
// =======================
async function loadOrders() {
    const res = await fetch("/api/orders");
    const orders = await res.json();

    const table = document.getElementById("orders-table-body");
    table.innerHTML = "";

    orders.forEach(order => {
        table.innerHTML += `
            <tr onclick="loadOrderDetails(${order.id})" style="cursor:pointer;">
                <td>${order.id}</td>
                <td>${order.customer}</td>
                <td>${order.order_date}</td>
                <td>${order.status}</td>
            </tr>
        `;
    });
}

// =======================
// LOAD ORDER DETAILS
// =======================
async function loadOrderDetails(orderId) {
    const res = await fetch(`/api/orders/${orderId}`);
    const items = await res.json();

    const table = document.getElementById("order-items-body");
    table.innerHTML = "";

    items.forEach(item => {
        table.innerHTML += `
            <tr>
                <td>${item.product}</td>
                <td>${item.quantity}</td>
            </tr>
        `;
    });
}

// =======================
// LOAD CUSTOMERS
// =======================
async function loadCustomers() {
    const res = await fetch("/api/customers");
    const customers = await res.json();

    const select = document.getElementById("customer-select");
    select.innerHTML = "";

    customers.forEach(c => {
        select.innerHTML += `<option value="${c.id}">${c.name}</option>`;
    });
}

// =======================
// LOAD PRODUCTS
// =======================
async function loadProducts() {
    const res = await fetch("/api/products");
    products = await res.json();
}

// =======================
// ADD ITEM ROW
// =======================

function addItemRow() {
    const table = document.getElementById("items-table-body");

    const row = document.createElement("tr");

    // Product dropdown
    const productCell = document.createElement("td");
    const select = document.createElement("select");
    select.className = "product-select";

    products.forEach(p => {
        const option = document.createElement("option");
        option.value = p.id;
        option.textContent = p.name;
        select.appendChild(option);
    });

    productCell.appendChild(select);

    // Quantity input
    const qtyCell = document.createElement("td");
    const input = document.createElement("input");
    input.type = "number";
    input.className = "quantity-input";
    input.value = 1;
    input.min = 1;

    qtyCell.appendChild(input);

    // Remove button
    const actionCell = document.createElement("td");
    const btn = document.createElement("button");
    btn.textContent = "Remove";
    btn.type = "button";

    btn.onclick = () => row.remove();

    actionCell.appendChild(btn);

    // Assemble row
    row.appendChild(productCell);
    row.appendChild(qtyCell);
    row.appendChild(actionCell);

    table.appendChild(row);
}

/*function addItemRow() {
    const table = document.getElementById("items-table-body");

    let options = "";
    products.forEach(p => {
        options += `<option value="${p.id}">${p.name}</option>`;
    });
    console.log("in additemrow");

    table.innerHTML += `
        <tr>
            <td>
                <select class="product-select">
                    ${options}
                </select>
            </td>
            <td>
                <input type="number" class="quantity-input" value="1" min="1">
            </td>
            <td>
                <button type="button" onclick="removeRow(this)">Remove</button>
            </td>
        </tr>
    `;
}*/

// =======================
// REMOVE ITEM ROW
// =======================
function removeRow(btn) {
    btn.parentElement.parentElement.remove();
}

// =======================
// CREATE ORDER
// =======================
async function createOrder(event) {
    event.preventDefault();

    const customer_id = document.getElementById("customer-select").value;
    const order_date = document.getElementById("order-date").value;

    const rows = document.querySelectorAll("#items-table-body tr");

    let items = [];

    rows.forEach(row => {
        const product_id = row.querySelector(".product-select").value;
        const quantity = row.querySelector(".quantity-input").value;

        items.push({
            product_id: parseInt(product_id),
            quantity: parseFloat(quantity)
        });
    });

    const res = await fetch("/api/orders", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            customer_id,
            order_date,
            items
        })
    });

    if (!res.ok) {
        alert("Error creating order");
        return;
    }

    alert("Order created!");

    loadOrders();

    // Reset form
    document.getElementById("items-table-body").innerHTML = "";
    addItemRow();
}