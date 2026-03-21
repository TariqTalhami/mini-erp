// Wait until the HTML page is fully loaded before running any JS
document.addEventListener("DOMContentLoaded", loadCustomers);


// =========================
// LOAD CUSTOMERS (READ)
// =========================
async function loadCustomers() {

    // Send GET request to backend API
    const response = await fetch("/api/customers");

    // If server returns error (e.g. 500, 404), log and stop
    if (!response.ok) {
        console.error("Server error");
        return;
    }

    // Convert response JSON into JavaScript object
    const customers = await response.json();

    // Get table body element where rows will be inserted
    const tableBody = document.getElementById("customers-table-body");

    // Clear existing table content before reloading
    tableBody.innerHTML = "";

    // Loop through customers and create table rows dynamically
    customers.forEach(customer => {
        tableBody.innerHTML += `
            <tr>
                <td>${customer.id}</td>
                <td>${customer.name}</td>
                <td>${customer.address}</td>
                <td>${customer.phoneNumber}</td>
                <td>
                    <!-- Edit button passes customer data to modal -->
                    <button onclick="openEditCustomer(${customer.id}, '${customer.name}', '${customer.address}', '${customer.phoneNumber}')">Edit</button>

                    <!-- Delete button calls delete function -->
                    <button onclick="deleteCustomer(${customer.id})">Delete</button>
                </td>
            </tr>
        `;
    });
}


// =========================
// ADD CUSTOMER (CREATE)
// =========================
async function addCustomer(event) {

    // Prevent page reload on form submit
    event.preventDefault();

    // Get values from input fields
    const name = document.getElementById("name").value;
    const address = document.getElementById("address").value;
    const phoneNumber = document.getElementById("phoneNumber").value;

    // Send POST request to backend with customer data
    const response = await fetch("/api/customers", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: name,
            address: address,
            phoneNumber: phoneNumber
        })
    });

    // Handle server error
    if (!response.ok) {
        console.error("Server error");
        return;
    }

    const result = await response.json();
    console.log(result); // Debug response

    // Reload customer list after adding new customer
    loadCustomers();
}


// =========================
// OPEN EDIT MODAL
// =========================
function openEditCustomer(id, name, address, phoneNumber) {

    // Fill modal form fields with existing customer data
    document.getElementById("edit-id").value = id;
    document.getElementById("edit-name").value = name;
    document.getElementById("edit-address").value = address;
    document.getElementById("edit-phoneNumber").value = phoneNumber;

    // Show modal (make it visible)
    document.getElementById("edit-customer-modal").style.display = "block";

    console.log("inside open function");
}


// =========================
// OPTIONAL: FORM LISTENER
// (only runs if form exists in DOM)
// =========================
const editForm = document.getElementById("edit-customer-form");

if (editForm) {
    editForm.addEventListener("submit", updateCustomer);
}


// =========================
// CLOSE EDIT MODAL
// =========================
function closeEditCustomer() {
    document.getElementById("edit-customer-modal").style.display = "none";
}


// =========================
// UPDATE CUSTOMER (UPDATE)
// =========================
async function updateCustomer(event) {

    event.preventDefault();

    // Get customer ID and updated values
    const id = document.getElementById("edit-id").value;

    const name = document.getElementById("edit-name").value;
    const address = document.getElementById("edit-address").value;
    const phoneNumber = document.getElementById("edit-phoneNumber").value;

    // Send PUT request to update customer
    await fetch(`/api/customers/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name,
            address,
            phoneNumber
        })
    });

    // Hide modal after update
    document.getElementById("edit-customer-modal").style.display = "none";

    // Reload updated data
    loadCustomers();
}


// =========================
// DELETE CUSTOMER (DELETE)
// =========================
async function deleteCustomer(id) {

    // Send DELETE request
    await fetch(`/api/customers/${id}`, {
        method: "DELETE"
    });

    // Reload table after deletion
    loadCustomers();
}