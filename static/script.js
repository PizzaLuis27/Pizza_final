document.addEventListener("DOMContentLoaded", function () {
    const slots = document.querySelectorAll(".time-slot");

    slots.forEach(slot => {
        slot.addEventListener("click", function () {
            if (slot.classList.contains("red")) {
                alert("Dieses Feld wurde schon reserviert!");
                return;
            }

            const time = slot.dataset.time;
            const name = prompt("Bitte geben Sie Ihren Namen ein:");
            if (!name) return;

            const pizzas = prompt("Wie viele Pizzen möchten Sie bestellen?");
            if (!pizzas || isNaN(pizzas) || pizzas <= 0) {
                alert("Ungültige Anzahl von Pizzen!");
                return;
            }

            const contact = prompt("Bitte geben Sie Ihre Kontaktdaten ein (E-Mail oder Telefonnummer):");
            if (!contact) {
                alert("Kontaktdaten sind erforderlich!");
                return;
            }

            fetch("/book", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ time: time, name: name, pizzas: pizzas, contact: contact }) // Fix: contact wird explizit gesendet
})

            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    slot.classList.remove("green");
                    slot.classList.add("red");
                }
                alert(data.message);
            });
        });
    });

    document.getElementById("admin-button").addEventListener("click", function () {
        const password = prompt("Bitte geben Sie das Admin-Passwort ein:");
        fetch("/admin", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ password })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                let bookings = "Buchungen:\n";
                for (const [time, info] of Object.entries(data.bookings)) {
    bookings += `${time}: ${info.name} - ${info.pizzas} Pizzen - Kontakt: ${info.contact || "Keine Kontaktdaten"}\n`;
}
                alert(bookings);
            } else {
                alert(data.message);
            }
        });
    });
});
