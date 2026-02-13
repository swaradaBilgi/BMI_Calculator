const form = document.getElementById("bmi-form");
const result = document.getElementById("result");
const recordsList = document.getElementById("records");

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

    const response = await fetch("/add-user", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    });

    const data = await response.json();

    result.innerText = `BMI: ${data.bmi} | Category: ${data.bmi_category}`;

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

        li.appendChild(deleteBtn);
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