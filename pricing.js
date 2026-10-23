const API_URL = "http://127.0.0.1:8000";

async function loadPrices() {
  const container = document.getElementById("price-list");

  try {
    const response = await fetch(`${API_URL}/services`);
    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }
    const services = await response.json();

    container.innerHTML = "";
    for (const service of services) {
      const card = document.createElement("div");
      card.className = "card";

      const title = document.createElement("h3");
      title.textContent = service.name;

      const price = document.createElement("p");
      price.className = "price";
      price.textContent = `$${service.price} / ${service.unit}`;

      const description = document.createElement("p");
      description.textContent = service.description;

      card.append(title, price, description);
      container.append(card);
    }
  } catch (error) {
    console.error("Could not load prices from the API:", error);
  }
}

loadPrices();