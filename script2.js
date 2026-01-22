<script>
document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("contact-form");
    const sendBtn = document.getElementById("send-btn");

    form.addEventListener("submit", async function(e) {
        e.preventDefault();

        sendBtn.innerText = "Sending...";
        sendBtn.disabled = true;

        const name = document.getElementById("name").value;
        const email = document.getElementById("email").value;
        const message = document.getElementById("message").value;

        try {
            const res = await fetch("http://127.0.0.1:5000/api/contact", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    name: name,
                    email: email,
                    message: message
                })
            });

            const data = await res.json();

            if (data.status === "success") {
                alert("Message sent successfully!");
                form.reset();
            } else {
                alert("Error: " + data.message);
            }

        } catch (err) {
            console.error("Server error:", err);
            alert("Server not running!");
        }

        sendBtn.innerText = "Send Message";
        sendBtn.disabled = false;
    });

});
</script>
