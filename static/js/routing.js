let steps = [];

async function loadProducts() {
    const res = await fetch('/api/finishedProducts');
    const data = await res.json();

    const select = document.getElementById('productSelect');
    select.innerHTML = '';

    data.forEach(p => {
        const option = document.createElement('option');
        option.value = p.id;
        option.textContent = p.name;
        select.appendChild(option);
    });
}

let materials = [];

async function loadMaterials() {
    const res = await fetch('/api/materials');
    materials = await res.json();
}

async function loadRouting() {
    const productId = document.getElementById('productSelect').value;

    const res = await fetch(`/api/routing/${productId}`);
    const data = await res.json();

    steps = data.steps || [];
    renderSteps();
}

function renderSteps() {
    const table = document.getElementById('stepsTable');
    table.innerHTML = '';

    steps.forEach((step, index) => {
        const row = document.createElement('tr');

        row.innerHTML = `
            <td>${index + 1}</td>
            <td><input value="${step.step_name || ''}" oninput="updateStep(${index}, 'step_name', this.value)"></td>
            <td><input value="${step.work_center || ''}" oninput="updateStep(${index}, 'work_center', this.value)"></td>
            <td>
                <select onchange="updateStep(${index}, 'material_id', this.value)">
                    <option value="" ${!step.material_id ? 'selected' : ''}>-- No Material --</option>
                    ${renderMaterialOptions(step.material_id)}
                </select>
            </td>
            <td>
                <select onchange="updateStep(${index}, 'material_id', this.value)">
                    <option value="" ${!step.material_id ? 'selected' : ''}>-- No Material --</option>
                    ${renderMaterialOptions(step.material_id)}
                </select>
            </td>
            <td><input type="number" value="${step.estimated_time || 0}" oninput="updateStep(${index}, 'estimated_time', this.value)"></td>
            <td><button onclick="deleteStep(${index})">X</button></td>
        `;

        table.appendChild(row);
    });
}

function renderMaterialOptions(selectedId) {
    return materials.map(m => `
        <option value="${m.id}" ${m.id == selectedId ? 'selected' : ''}>
            ${m.name}
        </option>
    `).join('');
}

function addStep() {
    steps.push({
        step_number: steps.length + 1,
        step_name: '',
        work_center: '',
        estimated_time: 0,
        material_id: null
    });

    renderSteps();
}

function deleteStep(index) {
    steps.splice(index, 1);
    renderSteps();
}

function updateStep(index, field, value) {
    if (field === 'material_id') {
        steps[index][field] = value === "" ? null : Number(value);
    } else if (field === 'estimated_time') {
        steps[index][field] = Number(value);
    } else {
        steps[index][field] = value;
    }
}

async function saveRouting() {
    const productId = document.getElementById('productSelect').value;

    await fetch('/api/routing', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            product_id: Number(productId),
            steps: steps.map((s, i) => ({
                step_number: i + 1,
                step_name: s.step_name,
                work_center: s.work_center,
                estimated_time: Number(s.estimated_time || 0),
                material_id: s.material_id ? Number(s.material_id) : null
            }))
        })
    });

    alert('Saved!');
}

async function init() {
    await loadProducts();
    await loadMaterials();
}

init();