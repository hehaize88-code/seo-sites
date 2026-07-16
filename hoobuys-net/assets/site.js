(() => {
  const setState = (button, open) => {
    button.setAttribute('aria-expanded', String(open));
    const openLabel = button.dataset.openLabel || 'Open navigation';
    const closeLabel = button.dataset.closeLabel || 'Close navigation';
    button.setAttribute('aria-label', open ? closeLabel : openLabel);
  };

  const button = document.getElementById('menuBtn');
  const nav = document.getElementById('nav');
  if (button && nav) {
    button.addEventListener('click', () => {
      const open = !nav.classList.contains('open');
      nav.classList.toggle('open', open);
      setState(button, open);
    });
    nav.addEventListener('click', event => {
      if (event.target.closest('a')) {
        nav.classList.remove('open');
        setState(button, false);
      }
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape') {
        nav.classList.remove('open');
        setState(button, false);
        button.focus();
      }
    });
  }

  const checkbox = document.getElementById('m');
  const toggle = document.querySelector('label.menu[for="m"]');
  const close = document.querySelector('.drawer label[for="m"]');
  if (checkbox && toggle) {
    toggle.tabIndex = 0;
    toggle.setAttribute('role', 'button');
    toggle.setAttribute('aria-controls', 'mobile-drawer');
    toggle.setAttribute('aria-expanded', String(checkbox.checked));
    const sync = () => toggle.setAttribute('aria-expanded', String(checkbox.checked));
    checkbox.addEventListener('change', sync);
    toggle.addEventListener('keydown', event => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        checkbox.checked = !checkbox.checked;
        sync();
      }
    });
    close?.setAttribute('tabindex', '0');
    close?.setAttribute('role', 'button');
    close?.addEventListener('keydown', event => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        checkbox.checked = false;
        sync();
        toggle.focus();
      }
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && checkbox.checked) {
        checkbox.checked = false;
        sync();
        toggle.focus();
      }
    });
  }
})();
