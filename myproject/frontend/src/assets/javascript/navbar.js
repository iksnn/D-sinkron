export function toggleMenu() {
    const menuIcon = document.getElementById('menu-icon');
    const mainNav = document.getElementById('main-nav');
  
    menuIcon.classList.toggle('bx-x');
    mainNav.classList.toggle('open');
  }