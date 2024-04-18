const submitBtn = document.getElementById("submit-btn");
const txHashInput = document.getElementById("tx_hash");
const dataContainer = document.getElementById("data-container");

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

    // Process and display the retrieved data
    console.log(data); // for debugging purposes (remove in production)
    // ... your code to display data in the table ...
  } catch (error) {
    console.error("Error fetching data:", error);
    alert("Failed to retrieve transaction data.");
  }
});
