const searchInput = document.getElementById('searchInput');
const cards = document.querySelectorAll('.category-card');
searchInput.addEventListener('input', function() {
  const searchTerm = searchInput.value.toLowerCase();
  console.log(searchTerm)
  cards.forEach(card => {
      const title = card.textContent.toLowerCase();
      if (title.includes(searchTerm)) {
        card.classList.remove('d-none'); // Показать карточку

      } else {
        card.classList.add('d-none'); // Скрыть карточку
      }
  });
});