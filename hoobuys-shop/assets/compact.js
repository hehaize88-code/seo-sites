(() => {
  'use strict';
  const menu = document.getElementById('menuBtn');
  const nav = document.getElementById('nav');
  const closeMenu = () => {
    if (!menu || !nav) return;
    nav.classList.remove('open');
    menu.setAttribute('aria-expanded', 'false');
  };
  if (menu && nav) {
    menu.addEventListener('click', () => {
      const open = nav.classList.toggle('open');
      menu.setAttribute('aria-expanded', String(open));
    });
    nav.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && nav.classList.contains('open')) { closeMenu(); menu.focus(); }
    });
    document.addEventListener('click', event => { if (!event.target.closest('.site-header')) closeMenu(); });
  }
  const mobile = window.matchMedia('(max-width: 760px)');
  const sections = [...document.querySelectorAll('.reading-section')];
  const toggle = document.querySelector('.reading-toggle');
  const refreshToggle = () => {
    if (!toggle) return;
    const allOpen = sections.every(section => section.open);
    toggle.textContent = allOpen ? toggle.dataset.collapse : toggle.dataset.expand;
    toggle.setAttribute('aria-expanded', String(allOpen));
  };
  const setMode = () => {
    sections.forEach(section => { section.open = !mobile.matches; });
    document.querySelectorAll('.compact-faq').forEach(section => { section.open = !mobile.matches; });
    if (mobile.matches) document.querySelectorAll('.faq-item[open]').forEach(section => { section.open = false; });
    refreshToggle();
  };
  setMode();
  mobile.addEventListener('change', setMode);
  sections.forEach(section => section.addEventListener('toggle', refreshToggle));
  if (toggle) toggle.addEventListener('click', () => {
    const open = !sections.every(section => section.open);
    sections.forEach(section => { section.open = open; });
    refreshToggle();
  });
  const revealFragment = hash => {
    if (!hash || hash === '#') return;
    let id;
    try { id = decodeURIComponent(hash.slice(1)); } catch { return; }
    const target = document.getElementById(id);
    if (!target) return;
    let section = target.closest('details');
    while (section) { section.open = true; section = section.parentElement.closest('details'); }
    requestAnimationFrame(() => target.scrollIntoView({block: 'start'}));
  };
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href^="#"]');
    if (!link) return;
    revealFragment(link.getAttribute('href'));
    const toc = link.closest('.reading-toc');
    if (toc) toc.open = false;
  });
  window.addEventListener('hashchange', () => revealFragment(location.hash));
  revealFragment(location.hash);
  let printState;
  window.addEventListener('beforeprint', () => {
    printState = sections.map(section => section.open);
    sections.forEach(section => { section.open = true; });
  });
  window.addEventListener('afterprint', () => {
    if (printState) sections.forEach((section, index) => { section.open = printState[index]; });
  });
})();
