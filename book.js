const API_URL = "http://127.0.0.1:8000";

const form = document.getElementById("booking-form");
const message = document.getElementById("message");
const serviceSelect = document.getElementById("service");
const baySelect = document.getElementById("bay");
const dateInput = document.getElementById("booking_date");
const startSelect = document.getElementById("start_hour");
const durationSelect = document.getElementById("duration_hours");

function showMessage(text, type) {
  message.textContent = text;
  message.className = type;
}

function addOption(select, value, label) {
  const option = document.createElement("option");
  option.value = value;
  option.textContent = label;
  select.append(option);
}

function formatHour(hour) {
  const suffix = hour >= 12 ? "PM" : "AM";
  const display = hour % 12 === 0 ? 12 : hour % 12;
  return `${display}:00 ${suffix}`;
}

function todayAsString() {
  const now = new Date();
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");
  return `${now.getFullYear()}-${month}-${day}`;
}

async function loadOptions() {
  try {
    const [servicesResponse, baysResponse] = await Promise.all([
      fetch(`${API_URL}/services`),
      fetch(`${API_URL}/bays`),
    ]);
    if (!servicesResponse.ok || !baysResponse.ok) {
      throw new Error("Could not load the booking options");
    }
    const services = await servicesResponse.json();
    const bays = await baysResponse.json();

    for (const service of services) {
      if (service.unit === "hour") {
        addOption(
          serviceSelect,
          service.id,
          `${service.name} ($${service.price} / hour)`
        );
      }
    }
    for (const bay of bays) {
      addOption(baySelect, bay.id, bay.name);
    }
  } catch (error) {
    console.error(error);
    showMessage(
      "Booking is unavailable right now. Please try again later.",
      "error"
    );
    form.querySelector("button").disabled = true;
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  showMessage("Sending your booking...", "");

  const booking = {
    customer_name: document.getElementById("customer_name").value.trim(),
    customer_email: document.getElementById("customer_email").value.trim(),
    service_id: Number(serviceSelect.value),
    bay_id: Number(baySelect.value),
    booking_date: dateInput.value,
    start_hour: Number(startSelect.value),
    duration_hours: Number(durationSelect.value),
  };

  try {
    const response = await fetch(`${API_URL}/bookings`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(booking),
    });
    const data = await response.json();

    if (response.status === 201) {
      showMessage(`Booked! Your booking number is ${data.id}.`, "success");
      form.reset();
    } else if (response.status === 409) {
      showMessage(
        "Sorry, that bay is already booked at that time. Please try another time or bay.",
        "error"
      );
    } else if (response.status === 422) {
      showMessage("Please check your details and try again.", "error");
    } else {
      showMessage(data.detail || "Something went wrong.", "error");
    }
  } catch (error) {
    console.error(error);
    showMessage(
      "Could not reach the server. Please try again later.",
      "error"
    );
  }
});

for (let hour = 8; hour <= 19; hour++) {
  addOption(startSelect, hour, formatHour(hour));
}
for (let hours = 1; hours <= 8; hours++) {
  addOption(durationSelect, hours, hours === 1 ? "1 hour" : `${hours} hours`);
}
dateInput.min = todayAsString();

loadOptions();