document.addEventListener("DOMContentLoaded", loadCustomers);

async function loadCustomers() {
    const response = await fetch("/api/customers");

    if (!response.ok) {
        console.error("Server error");
        return;
    }

    const customers = await response.json();

    console.log(customers)

    const tableBody = document.getElementById("customers-table-body");
    tableBody.innerHTML = "";

    customers.forEach(customer => {
        tableBody.innerHTML += `
            <tr>
                <td>${customer.id}</td>
                <td>${customer.name}</td>
                <td>${customer.address}</td>
                <td>${customer.phoneNumber}</td>
                <td>
                    <button onclick="openEditCustomer(${customer.id}, '${customer.name}', '${customer.address}', '${customer.phoneNumber}')">Edit</button>
                    <button onclick="deleteCustomer(${customer.id})">Delete</button>
                </td>
            </tr>
        `;
    });
}

async function addCustomer(event) {

    event.preventDefault();

    const name = document.getElementById("name").value;
    const address = document.getElementById("address").value;
    const phoneNumber = document.getElementById("phoneNumber").value;

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

    if (!response.ok) {
        console.error("Server error");
        return;
    }

    const result = await response.json();
    console.log(result);

    loadCustomers();
}

function openEditCustomer(id, name, address, phoneNumber) {

    document.getElementById("edit-id").value = id;
    document.getElementById("edit-name").value = name;
    document.getElementById("edit-address").value = address;
    document.getElementById("edit-phoneNumber").value = phoneNumber;

    document.getElementById("edit-customer-modal").style.display = "block";

    console.log("inside open function");

}

const editForm = document.getElementById("edit-customer-form");

if (editForm) {
    editForm.addEventListener("submit", updateCustomer);
}

function closeEditCustomer() {
    document.getElementById("edit-customer-modal").style.display = "none";
}

async function updateCustomer(event) {

    event.preventDefault();

    const id = document.getElementById("edit-id").value;

    const name = document.getElementById("edit-name").value;
    const address = document.getElementById("edit-address").value;
    const phoneNumber = document.getElementById("edit-phoneNumber").value;

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

    document.getElementById("edit-customer-modal").style.display = "none";

    loadCustomers();
}

async function deleteCustomer(id) {

    await fetch(`/api/customers/${id}`, {
        method: "DELETE"
    });

    loadCustomers();
}