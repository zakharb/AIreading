/*!
* Start Bootstrap - Agency v7.0.11 (https://startbootstrap.com/theme/agency)
* Copyright 2013-2022 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-agency/blob/master/LICENSE)
*/
//
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }

    };

    // Shrink the navbar 
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            offset: 74,
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

});

//vocabulary
function createVocabulary(e) {
    e.disabled = true;
    let words = document.querySelector('#vocabulary_words').value
    let vocabulary_button = document.querySelector('#vocabulary_button')
    let button_html = vocabulary_button.innerHTML;
    let file = e.files[0];
    let formData = new FormData();
    formData.append("file", file);
    vocabulary_button.innerHTML = `
        <span 
        class="spinner-border spinner-border-sm" 
        role="status" 
        aria-hidden="true">
        </span>
        Loading...`; 
    formData.append("words", words);
    fetch(e.dataset.url, {
        method: "POST",
        body: formData,
    })
    .then((response) => response.blob())
    .then((b) => {
        var a = document.createElement("a");
        a.href = URL.createObjectURL(b);
        a.setAttribute("download", 'vocabulary.xlsx');
        a.click();
        vocabulary_button.innerHTML = button_html;
        e.disabled = false;
})
}
  
function createBrevity(e) {
    let file = e.files[0];
    let formData = new FormData();
    let modal = document.querySelector('#modal')

    myModal = new bootstrap.Modal(modal)
    let modal_body = modal.querySelector('.modal-body')
    let modal_title = modal.querySelector('.modal-title')
    modal_title.innerHTML = "The short description of the Text";
    modal_body.innerHTML = "Loading...";
    myModal.show()

    formData.append("file", file);
    fetch(e.dataset.url, {
        method: "POST",
        body: formData,
    })
    .then((response) => response.text())
    .then((data) => {
        modal_body.innerHTML = data.replace(/\\n/g, "<br />");
})
}
  
  
function createSimilarity(e) {
    let file = e.files[0];
    let formData = new FormData();
    let modal = document.querySelector('#modal')

    myModal = new bootstrap.Modal(modal)
    let modal_body = modal.querySelector('.modal-body')
    let modal_title = modal.querySelector('.modal-title')
    modal_title.innerHTML = "The list of similar texts";
    modal_body.innerHTML = "Loading...";
    myModal.show()

    formData.append("file", file);
    fetch(e.dataset.url, {
        method: "POST",
        body: formData,
    })
    .then((response) => response.text())
    .then((data) => {
        modal_body.innerHTML = data.replace(/\\n/g, "<br />");
})
}
  
