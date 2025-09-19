document.getElementById("send").addEventListener("click", async () => {
  const url = document.getElementById("url").value;
  const format = document.getElementById("format").value || null;

  if (!url) {
    document.getElementById("status").textContent = "Enter a URL.";
    return;
  }

  try {
    const resp = await fetch("http://127.0.0.1:5000/download", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ url: url, format: format })
    });
    const data = await resp.json();
    document.getElementById("status").textContent = JSON.stringify(data);
  } catch (e) {
    document.getElementById("status").textContent = "Error: " + e;
  }
});

// Autofill with current tab URL
chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
  if (tabs[0]) {
    document.getElementById("url").value = tabs[0].url;
  }
});

