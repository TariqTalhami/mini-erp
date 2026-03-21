document.addEventListener("DOMContentLoaded", loadInventory);

async function loadInventory() {
    const response = await fetch("/api/products");

    if (!response.ok) {
        console.error("Server error");
        return;
    }

    const products = await response.json();

    console.log(products)

    const tableBody = document.getElementById("products-table-body");
    tableBody.innerHTML = "";

    products.forEach(product => {
        tableBody.innerHTML += `
            <tr>
                <td>${product.id}</td>
                <td>${product.name}</td>
                <td>${product.product_type}</td>
                <td>${product.unit}</td>
                <td>Actual Stock</td>
                <td>
                    <button onclick="openEditProduct(${product.id}, '${product.name}', '${product.product_type}', '${product.unit}')">Add Log</button>
                </td>
            </tr>
        `;
    });
}

async function addProduct(event) {

    event.preventDefault();

    const name = document.getElementById("name").value;
    const product_type = document.getElementById("product_type").value;
    const unit = document.getElementById("unit").value;

    const response = await fetch("/api/products", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: name,
            product_type: product_type,
            unit: unit
        })
    });

    if (!response.ok) {
        console.error("Server error");
        return;
    }

    const result = await response.json();
    console.log(result);

    loadProducts();
}

function openEditProduct(id, name, product_type, unit) {

    document.getElementById("edit-id").value = id;
    document.getElementById("edit-name").value = name;
    document.getElementById("edit-product_type").value = product_type;
    document.getElementById("edit-unit").value = unit;

    document.getElementById("edit-product-modal").style.display = "block";

    console.log("inside open function");

}

const editForm = document.getElementById("edit-product-form");

if (editForm) {
    editForm.addEventListener("submit", updateProduct);
}

function closeEditProduct() {
    document.getElementById("edit-product-modal").style.display = "none";
}

async function updateProduct(event) {

    event.preventDefault();

    const id = document.getElementById("edit-id").value;

    const name = document.getElementById("edit-name").value;
    const product_type = document.getElementById("edit-product_type").value;
    const unit = document.getElementById("edit-unit").value;

    await fetch(`/api/products/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name,
            product_type,
            unit
        })
    });

    document.getElementById("edit-product-modal").style.display = "none";

    loadProducts();
}

async function deleteProduct(id) {

    await fetch(`/api/products/${id}`, {
        method: "DELETE"
    });

    loadProducts();
}