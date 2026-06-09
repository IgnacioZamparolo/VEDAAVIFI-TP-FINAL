/* ============================================================
   PARRILLA — JavaScript principal
   Estructura: static/js/main.js
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

  /* --------------------------------------------------
     1. HAMBURGER / MENÚ MOBILE
  -------------------------------------------------- */
  const hamburger = document.querySelector('.hamburger');
  const mobileNav = document.querySelector('.mobile-nav');

  if (hamburger && mobileNav) {
    hamburger.addEventListener('click', () => {
      hamburger.classList.toggle('open');
      mobileNav.classList.toggle('open');
    });
    document.addEventListener('click', (e) => {
      if (!hamburger.contains(e.target) && !mobileNav.contains(e.target)) {
        hamburger.classList.remove('open');
        mobileNav.classList.remove('open');
      }
    });
  }

  /* --------------------------------------------------
     2. LINK ACTIVO EN NAVBAR
  -------------------------------------------------- */
  const pagina = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a, .mobile-nav a').forEach(link => {
    if (link.getAttribute('href') === pagina) link.classList.add('activo');
  });

  /* --------------------------------------------------
     3. TABS DEL MENÚ
  -------------------------------------------------- */
  const tabs = document.querySelectorAll('.menu-tab');
  const secciones = document.querySelectorAll('.cat-seccion');

  if (tabs.length) {
    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('activo'));
        secciones.forEach(s => s.classList.remove('activo'));
        tab.classList.add('activo');
        const target = document.getElementById(tab.dataset.target);
        if (target) {
          target.classList.add('activo');
          if (window.innerWidth < 700) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    });
    if (!document.querySelector('.menu-tab.activo')) {
      tabs[0]?.classList.add('activo');
      secciones[0]?.classList.add('activo');
    }
  }

  /* --------------------------------------------------
     4. FORMULARIO DE RESERVA (Configuración Nativa)
  -------------------------------------------------- */
  const form = document.getElementById('reservaFormNativo');

  if (form) {
    // Fecha mínima = hoy
    const fechaInput = document.getElementById('fecha');
    if (fechaInput) fechaInput.setAttribute('min', new Date().toISOString().split('T')[0]);

    function validarCampo(campo) {
      const grupo = campo.closest('.form-grupo');
      const msg   = grupo?.querySelector('.error-msg');
      let ok = true, texto = '';

      if (campo.required && !campo.value.trim()) {
        ok = false; texto = 'Este campo es obligatorio.';
      } else if (campo.type === 'email' && campo.value) {
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(campo.value)) {
          ok = false; texto = 'Ingresá un email válido.';
        }
      } else if (campo.id === 'fecha' && campo.value) {
        const sel = new Date(campo.value + 'T00:00:00');
        const hoy = new Date(); hoy.setHours(0,0,0,0);
        if (sel < hoy) { ok = false; texto = 'La fecha no puede ser en el pasado.'; }
      }

      campo.classList.toggle('error', !ok);
      if (msg) { msg.textContent = texto; msg.classList.toggle('show', !ok); }
      return ok;
    }

    form.querySelectorAll('.form-control').forEach(campo => {
      campo.addEventListener('blur', () => validarCampo(campo));
      campo.addEventListener('input', () => { if (campo.classList.contains('error')) validarCampo(campo); });
    });

    form.addEventListener('submit', (e) => {
      let todo_ok = true;
      form.querySelectorAll('.form-control').forEach(campo => { if (!validarCampo(campo)) todo_ok = false; });
      
      // Si las validaciones del navegador fallan, frenamos el envío
      if (!todo_ok) {
        e.preventDefault();
        return;
      }

      // Si todo está correcto, no llamamos a e.preventDefault().
      // Deshabilitamos el botón para evitar doble submit y dejamos que viaje la petición.
      const btn = form.querySelector('[type="submit"]');
      btn.disabled = true;
      btn.innerHTML = '⏳ Procesando reserva…';
    });
  }

  /* --------------------------------------------------
     5. ANIMACIÓN DE APARICIÓN (Intersection Observer)
  -------------------------------------------------- */
  const animados = document.querySelectorAll(
    '.info-card, .plato-card, .combo-card, .reseña-card, .servicio-card'
  );
  if ('IntersectionObserver' in window && animados.length) {
    const obs = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.style.opacity = '1';
          e.target.style.transform = 'translateY(0)';
          obs.unobserve(e.target);
        }
      });
    }, { threshold: 0.08 });
    animados.forEach(el => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(18px)';
      el.style.transition = 'opacity .45s ease, transform .45s ease';
      obs.observe(el);
    });
  }

});