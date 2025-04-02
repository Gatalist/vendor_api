import {axiosRequest, showToast, showSpinner, hideSpinner} from "./utils.js";

const spinner = document.getElementById('loading-spinner');
const productIdd = document.getElementById('product-idd');

const url = "/product-files/";
const productId = productIdd.dataset.cardid;
const categoryId = productIdd.dataset.categoryid;
const subcategoryId = productIdd.dataset.subcategoryid;

const instruction = document.getElementById('instruction');
if (instruction) {
    const spinnerInstruction = document.getElementById('spinner-instruction');
    instruction.addEventListener('click', async function () {
        console.log("instruction");
        spinnerInstruction.classList.remove('d-none')
        let data = {
            option: "getInstruction",
            productId: productId,
            categoryId: categoryId,
            subcategoryId: subcategoryId
        };
        await btnEvent(data);
        spinnerInstruction.classList.add('d-none')
    });
}

const imageOrigin = document.getElementById('image-origin');
if (imageOrigin) {
    const spinnerImageOrigin = document.getElementById('spinner-image-origin');
    imageOrigin.addEventListener('click', async function () {
        console.log("imageOrigin");
        spinnerImageOrigin.classList.remove('d-none')
        let data = {
            option: "getImageOrigin",
            productId: productId,
            categoryId: categoryId,
            subcategoryId: subcategoryId
        };
        await btnEvent(data);
        spinnerImageOrigin.classList.add('d-none')
    });
}

const imageWebp = document.getElementById('image-webp');
if (imageWebp) {
    const spinnerImageWebp = document.getElementById('spinner-image-webp');
    imageWebp.addEventListener('click', async function () {
        console.log("imageWebp");
        spinnerImageWebp.classList.remove('d-none')
        let data = {
            option: "getImageWebp",
            productId: productId,
            categoryId: categoryId,
            subcategoryId: subcategoryId
        };
        await btnEvent(data);
        spinnerImageWebp.classList.add('d-none')
    });
}

async function btnEvent(data) {
    const response = await axiosRequest({
        method: "post", url: url, data: data, responseType: 'blob'
    });
    let fileName = productId;
    const contentDisposition = response.headers['content-disposition'];
    const match = contentDisposition.match(/filename="?([^"]+)"?/);
    if (match && match[1]) {
        fileName = match[1]; // Извлекаем имя файла
    }
    // console.log(fileName)
    const newUrl = window.URL.createObjectURL(response.data);
    const link = document.createElement('a');
    link.href = newUrl;
    link.setAttribute('download', fileName);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

const copyToClipboard = document.querySelectorAll('[id^="copyToClipboard-"]');
copyToClipboard.forEach(button => {
    button.addEventListener('click', async function (event) {
        const clickedButton = event.target.parentNode.parentNode;
        const textToCopy = clickedButton.querySelector('[id^="copyText-"]');
        const text = textToCopy.innerText;
        console.log(textToCopy.innerText)
        try {
            await navigator.clipboard.writeText(text);
            showToast({title: 'Текст скопійовано', type: 'success', delay: 3000})
        } catch (err) {
            showToast({title: 'Помилка копиювання', type: 'danger', delay: 3000})
        }
    })
})
