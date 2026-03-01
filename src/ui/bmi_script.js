const form = document.getElementById("bmi-form");
const result = document.getElementById("result");
const recordsList = document.getElementById("records");

isUpdating = false;
idToUpdate = 0;

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const payload = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        age: Number(document.getElementById("age").value),
        height_cm: Number(document.getElementById("height").value),
        weight_kg: Number(document.getElementById("weight").value),
        city: document.getElementById("city").value,
        state: document.getElementById("state").value
    };

    if (isUpdating) {
        console.log("Updating record with id:", idToUpdate);
        const response = await fetch(`/bmi/${idToUpdate}`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });
        console.log("PATCH response status:", response.status);

        isUpdating = false;
        const data = await response.json();
        result.innerText = `BMI: ${data.bmi} | Category: ${data.bmi_category}`;
    } 
    else {
        const response = await fetch("/add-user", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        result.innerText = `BMI: ${data.bmi} | Category: ${data.bmi_category}`;
    }

    loadRecords();
});

async function loadRecords() {
    const response = await fetch("/bmi");
    const records = await response.json();

    recordsList.innerHTML = "";

    records.forEach(record => {
        const li = document.createElement("li");
        li.innerText = `#${record.persons_id} - Name: ${record.name} - BMI: ${record.bmi} (${record.bmi_category}) - ${record.city}, ${record.state} `;

        const deleteBtn = document.createElement("button");
        deleteBtn.innerText = "Delete";
        deleteBtn.onclick = () => deleteRecord(record.persons_id);

        const updateBtn = document.createElement("button");
        updateBtn.innerText = "Update";
        updateBtn.onclick = () => 
            {
                isUpdating = true;
                idToUpdate = record.persons_id;
                prefillForm(record.persons_id);
            };

        li.appendChild(deleteBtn);
        li.appendChild(updateBtn);
        recordsList.appendChild(li);
    });
}

async function deleteRecord(id) {
    console.log("deleteRecord called with id:", id);
    const res = await fetch(`/bmi/${id}`, {
        method: "DELETE"
    });
    console.log("DELETE response status:", res.status);

    loadRecords();
}

async function prefillForm(id) {
    console.log("prefillForm called with id:", id);
    const response = await fetch(`/bmi/${id}`);
    const record = await response.json();

    document.getElementById("name").value = record.name;
    document.getElementById("email").value = record.email;
    document.getElementById("age").value = record.age;
    document.getElementById("height").value = record.height_cm;
    document.getElementById("weight").value = record.weight_kg;
    document.getElementById("city").value = record.city;
    document.getElementById("state").value = record.state;
    loadRecords();
}
