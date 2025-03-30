async function axiosRequest({ method, url, data = null, params = null, headers = null, responseType = null }) {
    let _headers = {
        'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content'),
    };

    if (headers) {
        Object.assign(_headers, headers);
    } else {
        _headers["Accept"] = "application/json";
        _headers["Content-Type"] = "application/json";
    }

    const config = {
        method,    // HTTP method (GET, POST, PUT, DELETE)
        url,
        data,      // Body
        params,
        headers: _headers,
        responseType,
    };
    console.log("request server ->", config);

    return await axios(config)
        .then(response => {
            console.log("response server Success <-", response);
            return response;
        })
        .catch(error => {
            console.log("response server Error <-", error);
            throw error;
        });
}

function showSpinner() {
    spinner.classList.remove("d-none");
}

function hideSpinner() {
    spinner.classList.add("d-none");
}

function showToast({message = null, title = 'Повідомлення', type = 'primary', delay = 5000}) {
    const toastContainer = document.getElementById('toastContainer');
    const toastElement = document.createElement('div');
    toastElement.className = 'toast';
    toastElement.setAttribute('role', 'alert');
    toastElement.setAttribute('aria-live', 'assertive');
    toastElement.setAttribute('aria-atomic', 'true');
    toastElement.setAttribute('data-bs-delay', delay);

    toastElement.innerHTML = `
        <div class="toast-header bg-${type} text-white">
            <strong class="me-auto">${title}</strong>
            <small class="text-muted"></small>
            <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Закрити"></button>
        </div>
    `;

    toastContainer.appendChild(toastElement);

    const toast = new bootstrap.Toast(toastElement);
    toast.show();

    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}

export {axiosRequest, showToast, showSpinner, hideSpinner}