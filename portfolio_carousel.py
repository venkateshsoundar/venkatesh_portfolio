"""Production-safe section pager for the Streamlit portfolio."""

import streamlit as st


def render_section_carousel():
    """Show the seven portfolio sections one at a time with swipe navigation."""
    st.html(
        r"""
<script>
(() => {
  const sectionIds = [
    "about",
    "education",
    "experience",
    "certifications",
    "recognitions",
    "projects",
    "skills"
  ];
  const styleId = "portfolio-pager-styles";
  const sourceAttribute = "data-portfolio-pager-source";

  const pageDocument = document;
  const scriptElement = document.currentScript;
  const pagerHost = scriptElement?.closest(".stHtml");

  if (!pagerHost) {
    return;
  }

  if (typeof window.__portfolioCarouselCleanup === "function") {
    window.__portfolioCarouselCleanup();
    delete window.__portfolioCarouselCleanup;
  }
  if (typeof window.__portfolioPagerCleanup === "function") {
    window.__portfolioPagerCleanup();
  }
  pageDocument.getElementById("portfolio-section-carousel")?.remove();

  const pagerStyles = `
    [data-portfolio-section] {
      scroll-margin-top: 96px;
    }
    div[data-testid="stElementContainer"].portfolio-page-container-active {
      box-sizing: border-box;
      padding-top: 0 !important;
      padding-bottom: 30px !important;
    }
    [data-portfolio-section].portfolio-page-active {
      animation: portfolio-page-pop 0.52s cubic-bezier(0.22, 0.82, 0.32, 1);
      position: relative;
      top: 30px;
      transform-origin: center top;
    }
    .navbar a {
      position: relative;
      overflow: visible;
    }
    .navbar a::before {
      content: "";
      position: absolute;
      top: 50%;
      left: -15px;
      width: 20px;
      height: 2px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.3);
      transform: translateY(-50%);
      transition: background 0.24s ease, box-shadow 0.24s ease;
    }
    .navbar a:first-child::before {
      display: none;
    }
    .navbar a.portfolio-nav-complete {
      color: #ffe29a !important;
    }
    .navbar a.portfolio-nav-complete::before,
    .navbar a.portfolio-nav-active::before {
      background: #ffd166;
      box-shadow: 0 0 8px rgba(255, 209, 102, 0.72);
    }
    .navbar a.portfolio-nav-active {
      color: #ffffff !important;
      background: rgba(255, 209, 102, 0.16);
      box-shadow: inset 0 -3px 0 #ffd166;
    }
    .portfolio-pager-dots {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 0 16px 9px;
    }
    .portfolio-pager-dot {
      width: 8px;
      height: 8px;
      padding: 0;
      border: 1px solid rgba(255, 209, 102, 0.68);
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.34);
      cursor: pointer;
      transition:
        width 0.22s ease,
        background 0.22s ease,
        box-shadow 0.22s ease,
        transform 0.22s ease;
    }
    .portfolio-pager-dot:hover {
      background: rgba(255, 209, 102, 0.72);
      transform: scale(1.2);
    }
    .portfolio-pager-dot.is-complete {
      background: rgba(255, 209, 102, 0.62);
    }
    .portfolio-pager-dot.is-active {
      width: 26px;
      background: #ffd166;
      box-shadow: 0 0 9px rgba(255, 209, 102, 0.72);
    }
    .portfolio-pager-dot:focus-visible {
      outline: 2px solid #ffffff;
      outline-offset: 3px;
    }
    @media (hover: hover) and (pointer: fine) {
      [data-portfolio-section].portfolio-page-active {
        cursor: grab;
      }
    }
    @keyframes portfolio-page-pop {
      0% {
        opacity: 0.12;
        transform: translateX(var(--portfolio-entry-x, 28px)) translateY(16px) scale(0.95);
      }
      68% {
        opacity: 1;
        transform: translateX(0) translateY(-3px) scale(1.01);
      }
      100% {
        opacity: 1;
        transform: translateX(0) translateY(0) scale(1);
      }
    }
    @media (max-width: 700px) {
      div[data-testid="stElementContainer"].portfolio-page-container-active {
        padding-bottom: 20px !important;
      }
      [data-portfolio-section].portfolio-page-active {
        top: 20px;
      }
      .navbar a::before {
        display: none;
      }
      .portfolio-pager-dots {
        padding-bottom: 8px;
      }
    }
    @media (prefers-reduced-motion: reduce) {
      [data-portfolio-section].portfolio-page-active {
        animation: none;
      }
      .navbar a::before,
      .portfolio-pager-dot {
        transition: none;
      }
    }
  `;

  function installStyles() {
    let style = pageDocument.getElementById(styleId);
    if (!style) {
      style = pageDocument.createElement("style");
      style.id = styleId;
      pageDocument.head.appendChild(style);
    }
    style.textContent = pagerStyles;
  }

  function closestElementContainer(element) {
    return element?.closest('div[data-testid="stElementContainer"]') || null;
  }

  function rememberSource(node) {
    if (!node || node.getAttribute(sourceAttribute) === "true") {
      return;
    }
    node.dataset.portfolioPagerDisplay = node.style.display || "";
    node.setAttribute(sourceAttribute, "true");
  }

  function restoreSources() {
    pageDocument.querySelectorAll(`[${sourceAttribute}="true"]`).forEach((node) => {
      node.style.display = node.dataset.portfolioPagerDisplay || "";
      node.removeAttribute(sourceAttribute);
      delete node.dataset.portfolioPagerDisplay;
    });
    pageDocument.querySelectorAll("[data-portfolio-section]").forEach((root) => {
      root.classList.remove("portfolio-page-active");
      root.style.removeProperty("--portfolio-entry-x");
      root.removeAttribute("aria-hidden");
    });
    pageDocument.querySelectorAll(".portfolio-page-container-active").forEach((node) => {
      node.classList.remove("portfolio-page-container-active");
    });
    pageDocument.querySelectorAll(
      ".navbar a.portfolio-nav-active, .navbar a.portfolio-nav-complete"
    ).forEach((link) => {
      link.classList.remove("portfolio-nav-active", "portfolio-nav-complete");
      link.removeAttribute("aria-current");
    });
  }

  function buildPager(attempt = 0) {
    restoreSources();

    const anchors = sectionIds.map((id) =>
      pageDocument.querySelector(`a.section-anchor[name="${id}"]`)
    );
    const sectionRoots = sectionIds.map((id) =>
      pageDocument.querySelector(`[data-portfolio-section="${id}"]`)
    );

    if (
      anchors.some((anchor) => !anchor) ||
      sectionRoots.some((sectionRoot) => !sectionRoot)
    ) {
      if (attempt < 80) {
        window.setTimeout(() => buildPager(attempt + 1), 75);
      }
      return;
    }

    const anchorContainers = anchors.map(closestElementContainer);
    const sourceContainers = sectionRoots.map(closestElementContainer);
    const navbarContainer = pageDocument.querySelector(".navbar-container");

    if (
      anchorContainers.some((container) => !container) ||
      sourceContainers.some((container) => !container) ||
      !navbarContainer ||
      new Set(sourceContainers).size !== sectionIds.length
    ) {
      if (attempt < 80) {
        window.setTimeout(() => buildPager(attempt + 1), 75);
      }
      return;
    }

    installStyles();

    sourceContainers.forEach(rememberSource);
    anchorContainers.forEach((container) => {
      if (!sourceContainers.includes(container)) {
        rememberSource(container);
        container.style.display = "none";
      }
    });

    const dotNavigation = pageDocument.createElement("div");
    dotNavigation.className = "portfolio-pager-dots";
    dotNavigation.setAttribute("aria-label", "Portfolio pages");

    const navbarLinks = Array.from(
      pageDocument.querySelectorAll(".navbar a[href^='#']")
    );
    const dotButtons = sectionIds.map((id, index) => {
      const dot = pageDocument.createElement("button");
      const sectionName =
        navbarLinks.find((link) => link.getAttribute("href") === `#${id}`)
          ?.textContent?.trim() || id;
      dot.className = "portfolio-pager-dot";
      dot.type = "button";
      dot.title = sectionName;
      dot.setAttribute("aria-label", `View ${sectionName} section`);
      dotNavigation.appendChild(dot);
      return dot;
    });
    navbarContainer.appendChild(dotNavigation);

    let activeIndex = 0;
    let touchStartX = null;
    let touchStartY = null;
    let pointerStartX = null;
    let pointerStartY = null;
    let pointerId = null;

    function updateNavbar() {
      pageDocument.querySelectorAll(".navbar a[href^='#']").forEach((link) => {
        const targetIndex = sectionIds.indexOf(
          link.getAttribute("href")?.slice(1)
        );
        const isActive = targetIndex === activeIndex;
        const isComplete = targetIndex >= 0 && targetIndex < activeIndex;
        link.classList.toggle("portfolio-nav-active", isActive);
        link.classList.toggle("portfolio-nav-complete", isComplete);
        if (isActive) {
          link.setAttribute("aria-current", "page");
        } else {
          link.removeAttribute("aria-current");
        }
      });
    }

    function updateDots() {
      dotButtons.forEach((dot, dotIndex) => {
        const isActive = dotIndex === activeIndex;
        dot.classList.toggle("is-active", isActive);
        dot.classList.toggle("is-complete", dotIndex < activeIndex);
        if (isActive) {
          dot.setAttribute("aria-current", "page");
        } else {
          dot.removeAttribute("aria-current");
        }
      });
    }

    function resetPageScroll() {
      const scrollTargets = new Set([
        pageDocument.scrollingElement,
        pageDocument.documentElement,
        pageDocument.body,
        pageDocument.querySelector('[data-testid="stAppViewContainer"]'),
        pageDocument.querySelector('[data-testid="stMain"]'),
        pageDocument.querySelector(".stAppViewContainer"),
        pageDocument.querySelector(".main")
      ]);

      let ancestor = sourceContainers[activeIndex]?.parentElement;
      while (ancestor && ancestor !== pageDocument.body) {
        const overflowY = window.getComputedStyle(ancestor).overflowY;
        if (
          ["auto", "scroll", "overlay"].includes(overflowY) ||
          ancestor.scrollHeight > ancestor.clientHeight
        ) {
          scrollTargets.add(ancestor);
        }
        ancestor = ancestor.parentElement;
      }

      const moveToTop = () => {
        scrollTargets.forEach((target) => {
          if (!target) {
            return;
          }
          if (typeof target.scrollTo === "function") {
            target.scrollTo({ top: 0, left: 0, behavior: "auto" });
          }
          target.scrollTop = 0;
          target.scrollLeft = 0;
        });
        window.scrollTo({ top: 0, left: 0, behavior: "auto" });
      };

      moveToTop();
      window.requestAnimationFrame(moveToTop);
    }

    function activate(index, options = {}) {
      const {
        scroll = true,
        updateHash = true,
        direction = index >= activeIndex ? 1 : -1
      } = options;
      activeIndex =
        ((index % sectionIds.length) + sectionIds.length) % sectionIds.length;

      sourceContainers.forEach((container, sourceIndex) => {
        const isActive = sourceIndex === activeIndex;
        container.style.display =
          isActive
            ? container.dataset.portfolioPagerDisplay || ""
            : "none";
        container.classList.toggle("portfolio-page-container-active", isActive);
      });

      sectionRoots.forEach((root, rootIndex) => {
        const isActive = rootIndex === activeIndex;
        root.classList.remove("portfolio-page-active");
        root.setAttribute("aria-hidden", isActive ? "false" : "true");
        if (isActive) {
          root.style.setProperty(
            "--portfolio-entry-x",
            direction >= 0 ? "30px" : "-30px"
          );
          void root.offsetWidth;
          root.classList.add("portfolio-page-active");
        }
      });

      updateNavbar();
      updateDots();

      if (updateHash) {
        window.history.replaceState(null, "", `#${sectionIds[activeIndex]}`);
      }
      if (scroll) {
        resetPageScroll();
      }
    }

    function handleNavigationClick(event) {
      const link = event.target.closest(".navbar a[href^='#']");
      if (!link) {
        return;
      }
      const target = link.getAttribute("href")?.slice(1);
      const targetIndex = sectionIds.indexOf(target);
      if (targetIndex < 0) {
        return;
      }
      event.preventDefault();
      activate(targetIndex);
    }

    function handleKeydown(event) {
      const tagName = event.target?.tagName?.toLowerCase();
      if (
        ["input", "textarea", "select", "button"].includes(tagName) ||
        event.target?.isContentEditable
      ) {
        return;
      }
      if (event.key === "ArrowLeft") {
        event.preventDefault();
        activate(activeIndex - 1, { direction: -1 });
      } else if (event.key === "ArrowRight") {
        event.preventDefault();
        activate(activeIndex + 1, { direction: 1 });
      }
    }

    function handleTouchStart(event) {
      if (
        event.touches.length !== 1 ||
        !sectionRoots[activeIndex].contains(event.target) ||
        event.target.closest("a, button, input, textarea, select")
      ) {
        return;
      }
      touchStartX = event.touches[0].clientX;
      touchStartY = event.touches[0].clientY;
    }

    function navigateFromGesture(deltaX, deltaY, minimumDistance) {
      if (
        Math.abs(deltaX) < minimumDistance ||
        Math.abs(deltaX) <= Math.abs(deltaY) * 1.2
      ) {
        return;
      }
      if (deltaX > 0) {
        activate(activeIndex + 1, { direction: 1 });
      } else if (deltaX < 0) {
        activate(activeIndex - 1, { direction: -1 });
      }
    }

    function handleTouchEnd(event) {
      if (
        touchStartX === null ||
        touchStartY === null ||
        event.changedTouches.length !== 1
      ) {
        touchStartX = null;
        touchStartY = null;
        return;
      }
      const deltaX = event.changedTouches[0].clientX - touchStartX;
      const deltaY = event.changedTouches[0].clientY - touchStartY;
      touchStartX = null;
      touchStartY = null;
      navigateFromGesture(deltaX, deltaY, 55);
    }

    function handlePointerDown(event) {
      if (
        event.pointerType === "touch" ||
        event.button !== 0 ||
        !sectionRoots[activeIndex].contains(event.target) ||
        event.target.closest("a, button, input, textarea, select")
      ) {
        return;
      }
      pointerStartX = event.clientX;
      pointerStartY = event.clientY;
      pointerId = event.pointerId;
    }

    function handlePointerUp(event) {
      if (
        pointerStartX === null ||
        pointerStartY === null ||
        event.pointerId !== pointerId
      ) {
        return;
      }
      const deltaX = event.clientX - pointerStartX;
      const deltaY = event.clientY - pointerStartY;
      pointerStartX = null;
      pointerStartY = null;
      pointerId = null;
      navigateFromGesture(deltaX, deltaY, 65);
    }

    function handlePointerCancel() {
      pointerStartX = null;
      pointerStartY = null;
      pointerId = null;
    }

    function handleHashChange() {
      const targetIndex = sectionIds.indexOf(
        window.location.hash.replace("#", "")
      );
      if (targetIndex >= 0 && targetIndex !== activeIndex) {
        activate(targetIndex, { updateHash: false });
      }
    }

    dotButtons.forEach((dot, index) => {
      dot.addEventListener("click", () =>
        activate(index, { direction: index >= activeIndex ? 1 : -1 })
      );
    });

    pageDocument.addEventListener("click", handleNavigationClick);
    pageDocument.addEventListener("keydown", handleKeydown);
    pageDocument.addEventListener("touchstart", handleTouchStart, {
      passive: true
    });
    pageDocument.addEventListener("touchend", handleTouchEnd, {
      passive: true
    });
    pageDocument.addEventListener("pointerdown", handlePointerDown);
    pageDocument.addEventListener("pointerup", handlePointerUp);
    pageDocument.addEventListener("pointercancel", handlePointerCancel);
    window.addEventListener("hashchange", handleHashChange);

    window.__portfolioPagerCleanup = () => {
      pageDocument.removeEventListener("click", handleNavigationClick);
      pageDocument.removeEventListener("keydown", handleKeydown);
      pageDocument.removeEventListener("touchstart", handleTouchStart);
      pageDocument.removeEventListener("touchend", handleTouchEnd);
      pageDocument.removeEventListener("pointerdown", handlePointerDown);
      pageDocument.removeEventListener("pointerup", handlePointerUp);
      pageDocument.removeEventListener("pointercancel", handlePointerCancel);
      window.removeEventListener("hashchange", handleHashChange);
      dotNavigation.remove();
      restoreSources();
    };

    const requestedIndex = sectionIds.indexOf(
      window.location.hash.replace("#", "")
    );
    activate(requestedIndex >= 0 ? requestedIndex : 0, {
      scroll: false,
      updateHash: false,
      direction: 1
    });
  }

  buildPager();
})();
</script>
        """,
        unsafe_allow_javascript=True,
    )
