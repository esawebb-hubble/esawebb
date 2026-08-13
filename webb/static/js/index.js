document.addEventListener("DOMContentLoaded", function(){
        
    // --- 1. Prevenir cierre al hacer click dentro del menú desplegable ---
    document.querySelectorAll('.dropdown-menu').forEach(function(element){
        element.addEventListener('click', function (e) {
          e.stopPropagation();
        });
    });

    // --- 2. Lógica para pantallas pequeñas (Móviles) con Doble Toque ---
    if (window.innerWidth < 992) {
        const menuLinks = document.querySelectorAll('.nav-item.dropdown > .nav-link, .dropdown-menu a');

        menuLinks.forEach(function(link) {
            link.addEventListener('click', function (e) {
                let nextEl = this.nextElementSibling;
                
                if (nextEl && (nextEl.classList.contains('dropdown-menu') || nextEl.classList.contains('submenu'))) {
                    let isOpen = this.getAttribute('data-mobile-open') === 'true';

                    if (!isOpen) {
                        // Primer toque: Prevenir salto, abrir menú y marcar estado
                        e.preventDefault(); 
                        nextEl.style.display = 'block'; 
                        this.setAttribute('data-mobile-open', 'true'); 
                        this.setAttribute('aria-expanded', 'true'); 
                    }
                    // En el segundo toque se ignora el preventDefault y viaja a la URL
                }
            });
        });

        // Limpieza de estados al cerrar todo el menú hamburguesa
        document.querySelectorAll('.navbar-collapse').forEach(function(collapse) {
            collapse.addEventListener('hidden.bs.collapse', function () {
                this.querySelectorAll('.dropdown-menu, .submenu').forEach(function(menu) {
                    menu.style.display = ''; 
                    let link = menu.previousElementSibling;
                    if(link) {
                        link.setAttribute('data-mobile-open', 'false');
                        link.setAttribute('aria-expanded', 'false');
                    }
                });
            });
        });
    }

    // --- 3. Manejo de foco para accesibilidad por teclado (Tabulador) ---
    
    // Variable para detectar si la interacción actual es con el ratón
    let isMouseInteraction = false;
    
    // Si el usuario usa el ratón, encendemos la bandera
    document.addEventListener('mousedown', function() {
        isMouseInteraction = true;
    });
    
    // Si el usuario usa la tecla Tab, apagamos la bandera
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            isMouseInteraction = false;
        }
    });

    const focusableToggles = document.querySelectorAll('.dropdown-toggle, .dropdown-item');
    focusableToggles.forEach(function(toggle) {
        toggle.addEventListener('focus', function() {
            // Si el foco provino de un clic del ratón, abortamos para no dañar el hover CSS
            if (isMouseInteraction) return; 
            
            let nextEl = this.nextElementSibling;
            if (nextEl && (nextEl.classList.contains('dropdown-menu') || nextEl.classList.contains('submenu'))) {
                nextEl.style.display = 'block';
                this.setAttribute('aria-expanded', 'true'); 
            }
        });
    });

    const dropdownContainers = document.querySelectorAll('.nav-item.dropdown, li');
    dropdownContainers.forEach(function(container) {
        container.addEventListener('focusout', function(e) {
            // Si el usuario está usando el ratón, abortamos
            if (isMouseInteraction) return; 

            if (!container.contains(e.relatedTarget)) {
                let subMenu = container.querySelector('.dropdown-menu, .submenu');
                let toggle = container.querySelector('.dropdown-toggle, .dropdown-item');
                
                if (subMenu) {
                    subMenu.style.display = ''; // Limpiamos para devolver control al CSS
                }
                if (toggle) {
                    toggle.setAttribute('aria-expanded', 'false');
                }
            }
        });
    });

    // Initialize Bootstrap Popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl)
})
});