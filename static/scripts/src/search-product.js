const searchInput = document.getElementById('searchInput');
const cards = document.querySelectorAll('.card');
searchInput.addEventListener('input', function() {
  const searchTerm = searchInput.value.toLowerCase();
  console.log(searchTerm)
  cards.forEach(card => {
    const titleElement = card.querySelector('.card-title');
    const idElement = card.querySelector('.card-text');
    if (titleElement || idElement) {
      const title = titleElement.textContent.toLowerCase();
      const idd = idElement.textContent.toLowerCase();
      if (title.includes(searchTerm) || idd.includes(searchTerm)) {
        card.parentNode.classList.remove('d-none'); // Показать карточку

      } else {
        card.parentNode.classList.add('d-none'); // Скрыть карточку
      }
    }
  });
});
