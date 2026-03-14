function showPage(page) {
    const content = document.getElementById("content");

    fetch(`pages/${page}.html`)
        .then(response => response.text())
        .then(html => {
            content.innerHTML = html;

            // Load module JS logic after page loads
            if (page === "products") {
                loadProducts();
            }

            if (page === "customers") {
                loadCustomers();
            }

            if (page === "production") {
                loadProduction();
            }

            if (page === "orders") {
                loadOrders();
            }
        });
}