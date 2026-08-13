document.addEventListener("DOMContentLoaded", function(){
        
    document.querySelectorAll('.dropdown-menu').forEach(function(element){
        element.addEventListener('click', function (e) {
          e.stopPropagation();
        });
    });


    if (window.innerWidth < 992) {
        const menuLinks = document.querySelectorAll('.nav-item.dropdown > .nav-link, .dropdown-menu a');

        menuLinks.forEach(function(link) {
            link.addEventListener('click', function (e) {
                let nextEl = this.nextElementSibling;
                
                if (nextEl && (nextEl.classList.contains('dropdown-menu') || nextEl.classList.contains('submenu'))) {
                    
                   
                    let isOpen = this.dataset.mobileOpen === 'true';

                    if (!isOpen) {
                        e.preventDefault(); 
                        nextEl.style.display = 'block'; 
                        
                        
                        this.dataset.mobileOpen = 'true'; 
                        this.setAttribute('aria-expanded', 'true'); 
                    }
                }
            });
        });

        document.querySelectorAll('.navbar-collapse').forEach(function(collapse) {
            collapse.addEventListener('hidden.bs.collapse', function () {
                this.querySelectorAll('.dropdown-menu, .submenu').forEach(function(menu) {
                    menu.style.display = ''; 
                    let link = menu.previousElementSibling;
                    if(link) {
                        
                        link.dataset.mobileOpen = 'false';
                        link.setAttribute('aria-expanded', 'false');
                    }
                });
            });
        });
    }

    
    
    let isMouseInteraction = false;
    
    document.addEventListener('mousedown', function() {
        isMouseInteraction = true;
    });
    
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            isMouseInteraction = false;
        }
    });

    const focusableToggles = document.querySelectorAll('.dropdown-toggle, .dropdown-item');
    focusableToggles.forEach(function(toggle) {
        toggle.addEventListener('focus', function() {
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
            if (isMouseInteraction) return; 

            if (!container.contains(e.relatedTarget)) {
                let subMenu = container.querySelector('.dropdown-menu, .submenu');
                let toggle = container.querySelector('.dropdown-toggle, .dropdown-item');
                
                if (subMenu) {
                    subMenu.style.display = ''; 
                }
                if (toggle) {
                    toggle.setAttribute('aria-expanded', 'false');
                    
                    toggle.dataset.mobileOpen = 'false'; 
                }
            }
        });
    });

    // Initialize Bootstrap Popovers
    const popoverTriggerList = Array.from(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.forEach(function (popoverTriggerEl) {
      bootstrap.Popover.getOrCreateInstance(popoverTriggerEl);
    });
});
