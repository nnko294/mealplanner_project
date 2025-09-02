function showForm(type) {
    document.getElementById("login-form").classList.add("hidden");
    document.getElementById("register-form").classList.add("hidden");
    document.querySelectorAll(".tabs button").forEach(btn => btn.classList.remove("active"));
    if (type === "login") {
        document.getElementById("login-form").classList.remove("hidden");
        document.querySelector(".tabs button:nth-child(1)").classList.add("active");
    } else {
        document.getElementById("register-form").classList.remove("hidden");
        document.querySelector(".tabs button:nth-child(2)").classList.add("active");
    }
}

async function login() {
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;

    const response = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();
    alert(data.message || data.error);
    if (response.ok) {
        window.location.href = "../templates/mealplanner.html";
    }
}

async function register() {
    try {
        const username = document.getElementById("register-username").value;
        const password = document.getElementById("register-password").value;

        const response = await fetch("http://127.0.0.1:5000/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();
        alert(data.message || data.error);

        if (response.ok) {
            window.location.href = "../templates/mealplanner.html";
        }
    } catch (err) {
        console.error("Register error:", err);
        alert("Something went wrong. Check console for details.");
    }
}

document.getElementById("paystack-btn").addEventListener("click", function () {
    let handler = PaystackPop.setup({
        key: "pk_test_edfe2a26989735bfb53af4780992852363cb9410", // Replace with your Paystack public key
        email: "currentUser.email", // Ideally dynamically from your session/user
        amount: 5000 * 100, // Amount in kobo (₦50.00 = 5000 kobo)
        currency: "NGN",
        ref: "" + Math.floor(Math.random() * 1000000000 + 1), // Unique reference
        callback: function(response) {
            alert('Payment complete! Reference: ' + response.reference);
            // Here you can call your backend to mark the user as premium
        },
        onClose: function() {
            alert('Payment window closed.');
        }
    });
    handler.openIframe();
});

