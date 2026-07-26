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
    :root {
      --portfolio-navy: #0f1f3d;
      --portfolio-card: #243a5a;
      --portfolio-card-deep: #1b2e4b;
      --portfolio-blue: #006ac3;
      --portfolio-blue-soft: #4da3ff;
      --portfolio-gold: #ffcc33;
      --portfolio-text: #f8fafc;
      --portfolio-text-muted: #c7d2e1;
    }
    [data-portfolio-section] {
      scroll-margin-top: 96px;
    }
    div[data-testid="stElementContainer"].portfolio-page-container-active {
      box-sizing: border-box;
      padding-top: 0 !important;
      padding-bottom: 30px !important;
    }
    [data-portfolio-section].portfolio-page-active {
      animation: portfolio-page-slide-in 0.32s cubic-bezier(0.22, 0.61, 0.36, 1) both;
      position: relative;
      top: 30px;
      transform-origin: center top;
      will-change: opacity, transform;
    }
    .navbar a {
      position: relative;
      color: var(--portfolio-text) !important;
      overflow: visible;
    }
    .navbar-container {
      background:
        linear-gradient(rgba(9, 25, 53, 0.8), rgba(15, 31, 61, 0.92)),
        url("https://raw.githubusercontent.com/venkateshsoundar/venkatesh_portfolio/main/Welcome.gif")
          center/cover no-repeat !important;
    }
    .navbar {
      background: rgba(15, 31, 61, 0.72) !important;
    }
    .navbar a:hover {
      color: var(--portfolio-text) !important;
      background: rgba(0, 106, 195, 0.28) !important;
    }
    .navbar a::before {
      content: "";
      position: absolute;
      top: 50%;
      left: -15px;
      width: 20px;
      height: 2px;
      border-radius: 999px;
      background: rgba(77, 163, 255, 0.42);
      transform: translateY(-50%);
      transition: background 0.24s ease, box-shadow 0.24s ease;
    }
    .navbar a:first-child::before {
      display: none;
    }
    .navbar a.portfolio-nav-complete {
      color: #9dcbff !important;
    }
    .navbar a.portfolio-nav-complete::before {
      background: var(--portfolio-blue-soft);
      box-shadow: 0 0 8px rgba(77, 163, 255, 0.62);
    }
    .navbar a.portfolio-nav-active::before {
      background: var(--portfolio-gold);
      box-shadow: 0 0 8px rgba(255, 204, 51, 0.7);
    }
    .navbar a.portfolio-nav-active {
      color: var(--portfolio-gold) !important;
      background: rgba(0, 106, 195, 0.34);
      box-shadow: inset 0 -3px 0 var(--portfolio-gold);
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
      border: 1px solid rgba(77, 163, 255, 0.76);
      border-radius: 999px;
      background: rgba(199, 210, 225, 0.38);
      cursor: pointer;
      transition:
        width 0.22s ease,
        background 0.22s ease,
        box-shadow 0.22s ease,
        transform 0.22s ease;
    }
    .portfolio-pager-dot:hover {
      background: var(--portfolio-blue-soft);
      transform: scale(1.2);
    }
    .portfolio-pager-dot.is-complete {
      background: var(--portfolio-blue-soft);
    }
    .portfolio-pager-dot.is-active {
      width: 26px;
      animation: portfolio-dot-pulse 0.38s ease-out;
      border-color: var(--portfolio-gold);
      background: var(--portfolio-gold);
      box-shadow: 0 0 9px rgba(255, 204, 51, 0.7);
    }
    .portfolio-pager-dot:focus-visible {
      outline: 2px solid #ffffff;
      outline-offset: 3px;
    }
    .mobile-nav-toggle {
      color: var(--portfolio-gold) !important;
      background: rgba(15, 31, 61, 0.92) !important;
    }
    .hero-card,
    .card,
    .skills-section {
      border: 1px solid rgba(77, 163, 255, 0.2) !important;
      background:
        linear-gradient(135deg, var(--portfolio-navy), var(--portfolio-card)) !important;
      box-shadow: 0 10px 30px rgba(6, 18, 38, 0.28) !important;
    }
    .hero-left {
      background:
        linear-gradient(145deg, var(--portfolio-card-deep), var(--portfolio-navy)) !important;
    }
    .hero-contact-bar,
    .achievement-item,
    .exp-responsibilities-box {
      border: 1px solid rgba(77, 163, 255, 0.18) !important;
      background: rgba(27, 46, 75, 0.88) !important;
    }
    .edu-card,
    .exp-card,
    .cert-card,
    .award-card,
    .project-main-card,
    .skill-card {
      border: 1px solid rgba(77, 163, 255, 0.22) !important;
      background:
        linear-gradient(145deg, var(--portfolio-card-deep), var(--portfolio-card)) !important;
      box-shadow: 0 6px 18px rgba(6, 18, 38, 0.18) !important;
    }
    .section-title,
    .skills-header-title {
      color: var(--portfolio-gold) !important;
      background: var(--portfolio-card-deep) !important;
    }
    .hero-about-body,
    .edu-card-univ,
    .edu-research-summary,
    .exp-card-company,
    .exp-responsibilities-box,
    .cert-provider,
    .award-sub,
    .project-desc,
    .skill-list {
      color: var(--portfolio-text-muted) !important;
    }
    .project-img-holder {
      background: var(--portfolio-navy) !important;
    }
    .project-tool-badge,
    .skill-chip {
      border: 1px solid rgba(77, 163, 255, 0.45) !important;
      background: rgba(0, 106, 195, 0.32) !important;
      color: var(--portfolio-text) !important;
    }
    .hero-cta,
    .project-action {
      border-color: rgba(77, 163, 255, 0.72) !important;
      background: rgba(0, 106, 195, 0.2) !important;
      color: var(--portfolio-text) !important;
    }
    .hero-cta:hover,
    .project-action:hover {
      background: rgba(0, 106, 195, 0.42) !important;
    }
    .hero-cta.primary,
    .project-action.primary {
      border-color: var(--portfolio-gold) !important;
      background: var(--portfolio-gold) !important;
      color: var(--portfolio-navy) !important;
    }
    .hero-cta.primary:hover,
    .project-action.primary:hover {
      background: #ffe17a !important;
    }
    @media (hover: hover) and (pointer: fine) {
      [data-portfolio-section].portfolio-page-active {
        cursor: grab;
      }
    }
    @keyframes portfolio-page-slide-in {
      0% {
        opacity: 0;
        transform: translateX(var(--portfolio-entry-x, 28px));
      }
      100% {
        opacity: 1;
        transform: translateX(0);
      }
    }
    @keyframes portfolio-dot-pulse {
      0% {
        transform: scale(0.86);
      }
      58% {
        transform: scale(1.18);
      }
      100% {
        transform: scale(1);
      }
    }
    @media (max-width: 768px) {
      .navbar-container {
        height: calc(44px + env(safe-area-inset-top)) !important;
        min-height: calc(44px + env(safe-area-inset-top)) !important;
        padding: 0 !important;
        border-radius: 0 0 14px 14px !important;
        background: transparent !important;
        box-shadow: none !important;
        justify-content: center !important;
      }
      .navbar,
      .mobile-nav-toggle {
        display: none !important;
      }
      div[data-testid="stElementContainer"].portfolio-page-container-active {
        padding-top: calc(60px + env(safe-area-inset-top)) !important;
        padding-bottom: 20px !important;
      }
      [data-portfolio-section].portfolio-page-active {
        top: 0;
      }
      .navbar a::before {
        display: none;
      }
      .portfolio-pager-dots {
        position: fixed !important;
        top: 0 !important;
        right: 0 !important;
        left: 0 !important;
        z-index: 1100 !important;
        display: flex !important;
        box-sizing: border-box;
        width: 100vw !important;
        min-height: calc(44px + env(safe-area-inset-top));
        gap: 6px;
        margin: 0;
        padding:
          calc(10px + env(safe-area-inset-top))
          14px
          11px;
        visibility: visible !important;
        opacity: 1 !important;
        background: rgba(15, 31, 61, 0.96);
        box-shadow: 0 4px 14px rgba(6, 18, 38, 0.28);
        backdrop-filter: blur(10px);
        pointer-events: auto !important;
      }
      .portfolio-pager-dot {
        width: 9px;
        height: 9px;
      }
      .portfolio-pager-dot.is-active {
        width: 28px;
      }
    }
    @media (prefers-reduced-motion: reduce) {
      [data-portfolio-section].portfolio-page-active {
        animation: none;
      }
      .portfolio-pager-dot.is-active {
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
    const sectionNames = sectionIds.map((id) =>
      navbarLinks.find((link) => link.getAttribute("href") === `#${id}`)
        ?.textContent?.trim() || id
    );
    const dotButtons = sectionIds.map((id, index) => {
      const dot = pageDocument.createElement("button");
      const sectionName = sectionNames[index];
      dot.className = "portfolio-pager-dot";
      dot.type = "button";
      dot.title = sectionName;
      dot.setAttribute("aria-label", `View ${sectionName} section`);
      dotNavigation.appendChild(dot);
      return dot;
    });

    const mobileNavigationQuery = window.matchMedia("(max-width: 768px)");
    function placeDotNavigation() {
      const target = mobileNavigationQuery.matches
        ? pageDocument.body
        : navbarContainer;
      if (target && dotNavigation.parentElement !== target) {
        target.appendChild(dotNavigation);
      }
    }
    placeDotNavigation();
    if (typeof mobileNavigationQuery.addEventListener === "function") {
      mobileNavigationQuery.addEventListener("change", placeDotNavigation);
    } else if (typeof mobileNavigationQuery.addListener === "function") {
      mobileNavigationQuery.addListener(placeDotNavigation);
    }

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
      let activeRoot = null;

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
          activeRoot = root;
          root.style.setProperty(
            "--portfolio-entry-x",
            direction >= 0 ? "30px" : "-30px"
          );
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
      if (activeRoot) {
        void activeRoot.offsetWidth;
        activeRoot.classList.add("portfolio-page-active");
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
      const gestureTime = Date.now();
      if (gestureTime - (window.__portfolioPagerLastGestureAt || 0) < 450) {
        return;
      }
      window.__portfolioPagerLastGestureAt = gestureTime;
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
        event.isPrimary === false ||
        (event.pointerType === "mouse" && event.button !== 0) ||
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
      if (typeof mobileNavigationQuery.removeEventListener === "function") {
        mobileNavigationQuery.removeEventListener("change", placeDotNavigation);
      } else if (typeof mobileNavigationQuery.removeListener === "function") {
        mobileNavigationQuery.removeListener(placeDotNavigation);
      }
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
