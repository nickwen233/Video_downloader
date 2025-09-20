document.getElementById("download-btn").addEventListener("click", () => {
  const url = document.getElementById("video-url").value.trim();
  const mode = document.querySelector('input[name="mode"]:checked').value;
  const status = document.getElementById("status");

  if (!url) {
    status.textContent = "Please enter a URL.";
    return;
  }

  status.textContent = "Starting download...";

  fetch("http://127.0.0.1:5000/download", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url, mode })
  })
    .then(response => response.json())
    .then(data => {
      if (data.status === "started") {
        status.textContent = `Download started (${mode.toUpperCase()})`;
      } else {
        status.textContent = "Error: " + data.message;
      }
    })
    .catch(err => {
      console.error(err);
      status.textContent = "Error connecting to server.";
    });
});

