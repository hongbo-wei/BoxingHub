(function () {
  const container = document.querySelector("#affirmations");
  const affirmationEl = document.querySelector("#affirmation");
  const button = document.querySelector("#getNewAffirmation");

  if (!container || !affirmationEl || !button) {
    return;
  }

  const endpoint =
    container.dataset.affirmationEndpoint || "/affirmations/api/affirmation/";

  function setLoading(isLoading) {
    button.disabled = isLoading;
    if (isLoading) {
      affirmationEl.innerHTML = '<div class="loading-spinner"></div>';
    }
  }

  function setError(message) {
    affirmationEl.textContent = message;
  }

  async function fetchAffirmation() {
    setLoading(true);

    try {
      const response = await fetch(endpoint, {
        headers: {
          "Accept": "application/json",
        },
      });

      if (!response.ok) {
        const errorPayload = await response.json().catch(() => ({}));
        const details = errorPayload.details || response.statusText;
        throw new Error(`${errorPayload.error || "Request failed"}: ${details}`);
      }

      const data = await response.json();
      if (!data.affirmation) {
        throw new Error("No affirmation returned.");
      }

      affirmationEl.textContent = data.affirmation;
    } catch (error) {
      setError(String(error));
    } finally {
      setLoading(false);
    }
  }

  button.addEventListener("click", fetchAffirmation);
  fetchAffirmation();
})();
