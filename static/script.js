// Handle URL Shortening
document.getElementById('shortenForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const urlInput = document.getElementById('urlInput').value;
    const resultContainer = document.getElementById('result');
    const shortenedUrl = document.getElementById('shortenedUrl');
    const errorContainer = document.getElementById('error');

    try {
        const response = await fetch('/shorten', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: urlInput }),
        });
        const data = await response.json();

        if (response.ok) {
            resultContainer.classList.remove('d-none');
            shortenedUrl.href = `/shorten/${data.short_code}`;
            shortenedUrl.textContent = `${window.location.origin}/shorten/${data.short_code}`;
            errorContainer.classList.add('d-none');
        } else {
            throw new Error(data.error || 'Failed to shorten URL');
        }
    } catch (error) {
        resultContainer.classList.add('d-none');
        errorContainer.textContent = error.message;
        errorContainer.classList.remove('d-none');
    }
});



// Update URL
async function updateUrl() {
    const shortCode = document.getElementById('updateShortCode').value;
    const newUrl = document.getElementById('updateUrl').value;
    if (!shortCode || !newUrl) {
        alert("Please fill both fields");
        return;
    }
    try {
        const response = await fetch(`/shorten/${shortCode}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: newUrl })
        });
        const data = await response.json();
        alert(data.message || data.error);
    } catch (error) {
        console.error("Error updating URL:", error);
        alert("Failed to update URL");
    }
}

// Delete URL
async function deleteUrl() {
    const shortCode = document.getElementById('deleteInput').value;
    if (!shortCode) {
        alert("Please enter a short code");
        return;
    }
    try {
        const response = await fetch(`/shorten/${shortCode}`, { method: 'DELETE' });
        if (response.status === 204) {
            alert("URL deleted successfully");
        } else {
            const data = await response.json();
            alert(data.error || "Failed to delete URL");
        }
    } catch (error) {
        console.error("Error deleting URL:", error);
        alert("Failed to delete URL");
    }
}

// Handle Stats Retrieval
async function getStats() {
    const shortCode = document.getElementById('statsInput').value;
    const statsContainer = document.getElementById('statsContainer');

    try {
        const response = await fetch(`/shorten/${shortCode}/stats`);
        const data = await response.json();

        if (response.ok) {
            statsContainer.classList.remove('d-none');
            document.getElementById('originalUrl').textContent = data.original_url;
            document.getElementById('statsShortCode').textContent = data.short_code;
            document.getElementById('createdAt').textContent = new Date(data.created_at).toLocaleString();
            document.getElementById('updatedAt').textContent = new Date(data.updated_at).toLocaleString();
            document.getElementById('accessCount').textContent = data.access_count;
        } else {
            throw new Error(data.error || 'Failed to retrieve stats');
        }
    } catch (error) {
        alert(error.message);
        statsContainer.classList.add('d-none');
    }
}
