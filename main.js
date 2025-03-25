async function fetchAndParseXML(url) {
    const response = await fetch(url);
    const text = await response.text(); // Получаем XML как строку

    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(text, "text/xml"); // Парсим XML в DOM-объект

    return xmlDoc;
}

// Использование
fetchAndParseXML("https://products.mti.ua/api/?action=loadContent&key=Sqceh4xB9PvL&cat_id=216").then(xmlDoc => {
    const products = xmlDoc.querySelectorAll("product");
    
    products.forEach(product => {
        const id = product.getAttribute("id");
        const name = product.querySelector("param[code='name']").textContent;
        console.log(`ID: ${id}, Name: ${name}`);
    });
});