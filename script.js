const submitBtn = document.getElementById("submit-btn");
const txHashInput = document.getElementById("tx_hash");
const dataContainer = document.getElementById("data-container");
const tableBody = document.querySelector("#transaction-table tbody");

submitBtn.addEventListener("click", async () => {
  const txHash = txHashInput.value.trim();
  if (!txHash) {
    alert("Please enter a transaction hash.");
    return;
  }

  try {
    const response = await fetch("http://localhost:5000/get_data", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ tx_hash: txHash }),
    });

    const data = await response.json();
    if (data.error) {
      alert(data.error);
      return;
    }

    // Clear previous data
    tableBody.innerHTML = "";

    // Process and display the retrieved data in the table
    for (const [key, value] of Object.entries(data)) {
      const row = `
        <tr>
          <td>${key}</td>
          <td>${value} <button class="copy-button" data-value="${value}"><i class="far fa-copy"></i> Copy</button></td>
        </tr>`;
      tableBody.insertAdjacentHTML("beforeend", row);
    }

    // Add event listeners to copy buttons
    const copyButtons = document.querySelectorAll(".copy-button");
    copyButtons.forEach(button => {
      button.addEventListener("click", () => {
        const valueToCopy = button.getAttribute("data-value");
        navigator.clipboard.writeText(valueToCopy)
          .then(() => {
            // Display toast notification
            showNotification("Copied to clipboard");
          })
          .catch(err => {
            console.error('Failed to copy:', err);
          });
      });
    });
  } catch (error) {
    console.error("Error fetching data:", error);
    alert("Failed to retrieve transaction data.");
  }
});

function showNotification(message) {
  const notification = document.createElement("div");
  notification.classList.add("notification");
  notification.textContent = message;
  document.body.appendChild(notification);

  // Remove notification after 3 seconds
  setTimeout(() => {
    notification.remove();
  }, 3000);
}
