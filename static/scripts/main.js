// async function fetchAndParseXML(url) {
//     const response = await fetch(url);
//     const text = await response.text(); // Получаем XML как строку
//
//     const parser = new DOMParser();
//     const xmlDoc = parser.parseFromString(text, "text/xml"); // Парсим XML в DOM-объект
//
//     return xmlDoc;
// }
//
// // Использование
// fetchAndParseXML("https://products.mti.ua/api/?action=loadContent&key=Sqceh4xB9PvL&cat_id=216").then(xmlDoc => {
//     const products = xmlDoc.querySelectorAll("product");
//
//     products.forEach(product => {
//         const id = product.getAttribute("id");
//         const name = product.querySelector("param[code='name']").textContent;
//         console.log(`ID: ${id}, Name: ${name}`);
//     });
// });
//



function createModal({modalId: modalId, title: title, cardPicture: cardPicture, cardPhotos: cardPhotos, cardAttributes: cardAttributes}) {
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

function addBtnEvent(idd) {
    const buttonsCard = document.querySelector(`#btn-card-${idd}`);
    createModal({
        modalId: idd,
        title: buttonsCard.dataset.name,
        cardPicture: buttonsCard.dataset.picture,
        cardPhotos: parseData(buttonsCard.dataset.photos),
        cardAttributes: parseData(buttonsCard.dataset.attributes)
    });
}

function parseData(data) {
    try {
        console.log("data befor ->", data);
        if (data) {
            const newData = JSON5.parse(data.replace(/None/g, null));
            console.log("data after ->", newData);
            return newData
        } else {
            return null;
        }
    } catch (error) {
        console.error("Помилка парсингу JSON:", error);
        return null;
    }
}