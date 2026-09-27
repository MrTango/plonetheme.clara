/* clara.js — what the CSS-only .opener checkboxes cannot do: the close
 * gestures of the mega menu and of the on-demand search (outside click,
 * Escape, one open thing at a time), and focusing the opened search field.
 */
(function () {
  function init() {
    var nav = document.querySelector("#portal-globalnav");
    if (!nav) return;

    function openers() {
      return nav.querySelectorAll(":scope > .nav-item > .opener");
    }
    function closeAll(except) {
      openers().forEach(function (opener) {
        if (opener !== except) opener.checked = false;
      });
    }

    // only one panel at a time: opening a section closes its siblings
    nav.addEventListener("change", function (e) {
      if (e.target.matches(".opener") && e.target.checked) closeAll(e.target);
    });

    // click anywhere outside the nav closes the open panel
    document.addEventListener("click", function (e) {
      if (!nav.contains(e.target)) closeAll();
    });

    // Escape closes and hands focus back to the toggle
    document.addEventListener("keydown", function (e) {
      if (e.key !== "Escape") return;
      var open = nav.querySelector(":scope > .nav-item > .opener:checked");
      if (!open) return;
      closeAll();
      open.focus();
    });
  }

  function initSearch() {
    var box = document.querySelector(".searchbox-on-demand");
    var opener = box && box.querySelector("#portal-searchbox-opener");
    var field = box && box.querySelector("#searchGadget");
    if (!opener || !field) return;

    var nav = document.querySelector("#portal-globalnav");
    var menuOpener = document.querySelector(".element-globalnav > .opener");

    function close() {
      opener.checked = false;
    }

    // opening the search closes the panels and the narrow menu
    opener.addEventListener("change", function () {
      if (!opener.checked) return;
      if (nav) {
        nav.querySelectorAll(":scope > .nav-item > .opener").forEach(function (o) {
          o.checked = false;
        });
      }
      if (menuOpener) menuOpener.checked = false;
      field.focus();
    });

    // and they close the search
    if (nav) {
      nav.addEventListener("change", function (e) {
        if (e.target.matches(".opener") && e.target.checked) close();
      });
    }
    if (menuOpener) {
      menuOpener.addEventListener("change", function () {
        if (menuOpener.checked) close();
      });
    }

    document.addEventListener("click", function (e) {
      if (opener.checked && !box.contains(e.target)) close();
    });

    document.addEventListener("keydown", function (e) {
      if (e.key !== "Escape" || !opener.checked) return;
      close();
      opener.focus();
    });
  }

  function start() {
    init();
    initSearch();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
