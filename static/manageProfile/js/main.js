const faqDiv = document.querySelectorAll('.faq');
faqDiv.forEach((div) => {
    div.addEventListener('click', (e) => {
        e.target.closest('.faq').classList.toggle('active');
    });
 });