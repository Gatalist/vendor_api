function createCard(product) {
    const cardId = `${product.id}`;
    const card = document.createElement('div');
    card.className = 'col-sm-4';
    card.innerHTML = `
        <div class="card mb-4">
            <img class="card-img-top fixed-height-img" src="${product.detail_picture}" alt="Card image">
            <div class="card-body">
                <h5 class="card-title">${product.name}</h5>
                <div class="col align-self-center">
                    <p class="card-text">id: ${cardId}</p>
                    <div class="d-flex justify-content-center">
                        <button type="button" class="btn btn-secondary me-2" id="btn-img-${cardId}" onclick="btnEventImg(${cardId})"> 
                            Завантажити фото
                        </button>
                        <button type="button" class="btn btn-success" id="btn-card-${cardId}" onclick="btnEventAttrs(${cardId})"> 
                            Характеристики
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    return card;
}

function createModal({modalId: modalId, title: title, cardAttributes: cardAttributes}) {
    const existingModal = document.getElementById(modalId);
    if (existingModal) {
        existingModal.remove();
    }
    const modalHTML = `
        <div class="modal fade bd-example-modal-lg" id="${modalId}" tabindex="-1" role="dialog" aria-labelledby="${modalId}Label" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="${modalId}Label">${title}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-header">
                        <h7 class="modal-title">id: ${modalId}</h7>
                    </div>
                    <div class="modal-body">
                        ${createAttributeTable(cardAttributes)}
                    </div>
                    <div class="modal-footer d-flex justify-content-center">
                        <button type="button" class="btn btn-secondary" id="${modalId}-cencel-delete" data-bs-dismiss="modal">Закрити</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    const modal = new bootstrap.Modal(document.getElementById(modalId));
    modal.show();
    const acceptDelete = document.getElementById(`${modalId}-cencel-delete`);
    acceptDelete.addEventListener('click', function () {
        modal.hide();
    });
}

function createAttributeTable(cardAttributes) {
    const container = document.createElement('div');
    container.className = "container";

    cardAttributes.forEach(item => {
        const row = document.createElement('div');
        row.className = "row";

        const rowAttr = document.createElement('div');
        rowAttr.className = "col-5 border-bottom mt-2";
        if (item.code_value) {
            rowAttr.innerText = item.code_value;
        } else {
            rowAttr.innerText = item.code_name;
        }

        const rowVal = document.createElement('div');
        rowVal.className = "col-7 border-bottom mt-2";
        rowVal.innerText = item.value;

        row.appendChild(rowAttr);
        row.appendChild(rowVal);
        container.appendChild(row);
    });
    return container.innerHTML;
}

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

export {axiosRequest, createModal, createCard}