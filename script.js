document.addEventListener("DOMContentLoaded", () => {
  const submitBtn = document.getElementById("submit-btn");
  const loader = document.getElementById("loader"); // Loader element
  const latestBlockElement = document.getElementById("latest-block-text");
  const whitelistCount = document.getElementById(
    "contract-whitelist-count-text"
  );
  const databaseCount = document.getElementById(
    "database-whitelist-count-text"
  );
  async function fetchLatestBlockNumber() {
    try {
      const response = await fetch("http://192.168.29.228:5000/latest_block", {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      });

      const data = await response.json();
      if (data.error) {
        console.error(data.error);
        return;
      }

      latestBlockElement.textContent = data.block_number;
    } catch (error) {
      console.error("Error fetching latest block number:", error);
    }
  }
  fetchLatestBlockNumber();
  setInterval(fetchLatestBlockNumber, 1000);

  submitBtn.addEventListener("click", async () => {
    const txHash = document.getElementById("tx_hash").value.trim();
    if (!txHash) {
      alert("Please enter a transaction hash.");
      return;
    }

    const tableBody = document.getElementById("transaction-table");
    tableBody.innerHTML = ""; // Clear previous data

    try {
      loader.style.display = "block"; // Show loader

      const response = await fetch("http://192.168.29.228:5000/get_data", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tx_hash: txHash }),
      });

      const data = await response.json();
      if (data.error) {
        alert(data.error);
        return;
      }

      // Add transaction hash row with copy button
      const txHashRow = `
        <tr>
          <td>Transaction Hash</td>
          <td>${txHash}</td>
          <td><button class="btn btn-sm btn-info copy-button" data-value="${txHash}"><i class="far fa-copy"></i></button></td>
        </tr>`;
      tableBody.insertAdjacentHTML("beforeend", txHashRow);

      // Process and display the retrieved data in the table
      for (const [key, value] of Object.entries(data)) {
        const row = `
          <tr>
            <td>${key}</td>
            <td>${value}</td>
            <td><button class="btn btn-sm btn-info copy-button" data-value="${value}"><i class="far fa-copy"></i></button></td>
          </tr>`;
        tableBody.insertAdjacentHTML("beforeend", row);
      }

      // Add event listeners to copy buttons
      const copyButtons = document.querySelectorAll(".copy-button");
      copyButtons.forEach((button) => {
        button.addEventListener("click", () => {
          const valueToCopy = button.getAttribute("data-value");
          navigator.clipboard
            .writeText(valueToCopy)
            .then(() => {
              // Display toast notification
              showNotification("Copied to clipboard");
            })
            .catch((err) => {
              console.error("Failed to copy:", err);
            });
        });
      });
    } catch (error) {
      console.error("Error fetching data:", error);
      alert("Failed to retrieve transaction data.");
    } finally {
      loader.style.display = "none"; // Hide loader
    }
  });

  async function fetchContractWhitelistCount() {
    try {
      const response = await fetch(
        "http://192.168.29.228:5000/contract_whitelist_count",
        {
          method: "GET",
          headers: { "Content-Type": "application/json" },
        }
      );

      const data = await response.json();
      if (data.error) {
        console.error(data.error);
        return;
      }
      whitelistCount.textContent = data.whitelist_count;
    } catch (error) {
      console.error("Error fetching whitelist count:", error);
    }
  }
  fetchContractWhitelistCount();
  setInterval(fetchContractWhitelistCount, 60000);

  async function fetchDatabaseWhitelistCount() {
    try {
      const response = await fetch(
        "http://192.168.29.228:5000/database_whitelist_count",
        {
          method: "GET",
          headers: { "Content-Type": "application/json" },
        }
      );

      const data = await response.json();
      if (data.error) {
        console.error(data.error);
        return;
      }
      databaseCount.textContent = data.whitelist_count - 1;
    } catch (error) {
      console.error("Error fetching database whitelist count:", error);
    }
  }
  fetchDatabaseWhitelistCount();
  setInterval(fetchDatabaseWhitelistCount, 60000);

  async function sendTelegramBotMessage() {
    if (whitelistCount.textContent != databaseCount.textContent && databaseCount.textContent != 'Loading...' && whitelistCount.textContent != 'Loading...') {
        try {
            const response = await fetch(
                "http://192.168.29.228:5000/telegram_bot",
                {
            method: "GET",
            headers: { "Content-Type": "application/json" },
          }
        );
        
        const data = await response.json();
        if (data.error) {
            console.error(data.error);
            return;
        }
      } catch (error) {
        console.error("Error sending message from telegram bot:", error);
      }
    }
  }

  sendTelegramBotMessage();
  setInterval(sendTelegramBotMessage, 300000);

  function showNotification(message) {
    const notification = document.createElement("div");
    notification.classList.add("notification");
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
      notification.remove();
    }, 3000);
  }
});
