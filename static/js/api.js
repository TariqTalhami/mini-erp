const API_BASE = "";

async function apiGet(endpoint) {
    const response = await fetch(`${API_BASE}${endpoint}`);
    return response.json();
}

async function apiPost(endpoint, data) {
    const response = await fetch(`${API_BASE}${endpoint}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });
    return response.json();
}

async function apiDelete(endpoint) {
    const response = await fetch(`${API_BASE}${endpoint}`, {
        method: "DELETE"
    });
    return response.json();
}