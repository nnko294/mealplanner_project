async function checkSession() {
    const response = await fetch("http://127.0.0.1:5000/check_session", {
        credentials: "include"
    });
    if (response.ok) {
        const data = await response.json();
        document.getElementById("welcome").textContent = `Welcome, ${data.username}`;
    } else {
        window.location.href = "../templates/index.html";
    }
}

async function logout() {
    await fetch("http://127.0.0.1:5000/logout", {
        method: "POST",
        credentials: "include"
    });
    window.location.href = "../templates/index.html";
}

async function getRecommendations() {
    const disease = document.getElementById("disease").value;
    const response = await fetch("http://127.0.0.1:5000/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ disease })
    });
    const data = await response.json();

    const list = document.getElementById("results");
    list.innerHTML = "";
    if (data.meals && data.meals.length > 0) {
        data.meals.forEach(meal => {
            const li = document.createElement("li");
            li.textContent = meal.meal_name + ": " + meal.description;
            list.appendChild(li);
        });
    } else {
        list.textContent = data.message || "No meals found.";
    }

    const aiBox = document.getElementById("ai-results");
    aiBox.textContent = data.ai || "No AI suggestions.";
}

window.onload = checkSession;