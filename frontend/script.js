async function shortenUrl() {
    const urlInput = document.getElementById("urlInput").value;
    const resultDiv = document.getElementById("result");
    
    if (!urlInput) {
        resultDiv.innerHTML = '<span class="error">Por favor ingresa una URL válida.</span>';
        return;
    }

    resultDiv.innerHTML = 'Generando enlace...';

    try {
        const response = await fetch("http://<IP_EC2>:8000/shorten", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ original_url: urlInput })
        });

        if (!response.ok) {
            throw new Error("El backend devolvió un error");
        }

        const data = await response.json();
        resultDiv.innerHTML = `
            <p>Tu enlace corto:</p>
            <a href="${data.short_url}" target="_blank" id="shortLink">${data.short_url}</a>
            <br><br>
            <button onclick="navigator.clipboard.writeText('${data.short_url}')">Copiar Enlace</button>
        `;
    } catch (error) {
        resultDiv.innerHTML = '<span class="error">Error de conexión. Verifica que el backend en EC2 esté encendido y la IP sea correcta.</span>';
    }
}