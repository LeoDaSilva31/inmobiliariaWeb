// django_inmobiliaria/static/js/main.js

document.addEventListener('DOMContentLoaded', function() {
    console.log("¡JavaScript de la inmobiliaria cargado! (Bootstrap edition)");

    // Ejemplo: un script simple para un botón de "scroll to top"
    const scrollToTopBtn = document.createElement('button');
    scrollToTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>'; // Icono de FontAwesome
    scrollToTopBtn.classList.add('btn', 'btn-info', 'rounded-circle', 'shadow', 'position-fixed', 'bottom-0', 'end-0', 'm-3', 'd-none'); // Clases de Bootstrap
    scrollToTopBtn.style.width = '50px';
    scrollToTopBtn.style.height = '50px';
    scrollToTopBtn.style.lineHeight = '50px';
    scrollToTopBtn.style.fontSize = '1.5rem';
    document.body.appendChild(scrollToTopBtn);

    window.addEventListener('scroll', function() {
        if (window.scrollY > 200) {
            scrollToTopBtn.classList.remove('d-none');
        } else {
            scrollToTopBtn.classList.add('d-none');
        }
    });

    scrollToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
});