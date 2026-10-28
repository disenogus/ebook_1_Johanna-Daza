// Ajusta el tamaño de las páginas al ancho de la pantalla (solo visualización; no afecta la impresión/PDF).
(function () {
  function fit() {
    var w = document.documentElement.clientWidth - 24;
    var z = Math.min(1, w / 816);
    document.documentElement.style.setProperty('--zoom', z);
  }
  fit();
  window.addEventListener('resize', fit);
  // ?final en la URL oculta etiquetas de borrador y textos de placeholder
  if (/[?&]final/.test(location.search)) document.body.classList.add('final');
})();
