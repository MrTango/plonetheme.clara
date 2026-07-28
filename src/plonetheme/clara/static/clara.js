/* clara.js — the ONE tiny JS sprinkle the CSS-only mega menu cannot do itself
 * (see theme/scss/_clara-megamenu.scss): the dlr.de / Volto-light-theme close
 * gestures. Opening, closing via the item, and all styling stay pure CSS on
 * the native .opener checkboxes; this only unchecks them when the user
 * clicks outside the nav, presses Escape, or opens another section.
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

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
