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
      padding-top: 20px !important;
    }
    [data-portfolio-section].portfolio-page-active {
      animation: portfolio-page-pop 0.52s cubic-bezier(0.22, 0.82, 0.32, 1);
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
    .portfolio-pager-side {
      position: fixed;
      top: 50%;
      z-index: 999;
      width: 48px;
      height: 48px;
      border: 1px solid rgba(255, 209, 102, 0.72);
      border-radius: 50%;
      background: rgba(31, 42, 68, 0.94);
      color: #ffd166;
      box-shadow: 0 8px 26px rgba(17, 28, 52, 0.32);
      backdrop-filter: blur(12px);
      font-size: 1.45rem;
      font-weight: 900;
      line-height: 1;
      cursor: pointer;
      transform: translateY(-50%);
      transition: transform 0.18s ease, background 0.18s ease, opacity 0.18s ease;
    }
    .portfolio-pager-side:hover:not(:disabled) {
      background: #ffd166;
      color: #22304a;
      transform: translateY(-50%) scale(1.07);
    }
    .portfolio-pager-side:disabled {
      cursor: default;
      opacity: 0.28;
    }
    .portfolio-pager-previous {
      left: 14px;
    }
    .portfolio-pager-next {
      right: 14px;
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
      .portfolio-pager-side {
        top: auto;
        bottom: 17px;
        width: 42px;
        height: 42px;
        transform: none;
      }
      .portfolio-pager-side:hover:not(:disabled) {
        transform: scale(1.05);
      }
      .portfolio-pager-previous {
        left: 10px;
      }
      .portfolio-pager-next {
        right: 10px;
      }
      div[data-testid="stElementContainer"].portfolio-page-container-active {
        padding-top: 14px !important;
      }
      .navbar a::before {
        display: none;
      }
    }
    @media (prefers-reduced-motion: reduce) {
      [data-portfolio-section].portfolio-page-active {
        animation: none;
      }
      .portfolio-pager-side,
      .navbar a::before {
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

    if (
      anchorContainers.some((container) => !container) ||
      sourceContainers.some((container) => !container) ||
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

    const previousButton = pageDocument.createElement("button");
    previousButton.className = "portfolio-pager-side portfolio-pager-previous";
    previousButton.type = "button";
    previousButton.innerHTML = "&#8592;";
    previousButton.setAttribute("aria-label", "Previous portfolio section");
    previousButton.title = "Previous section";

    const nextButton = pageDocument.createElement("button");
    nextButton.className = "portfolio-pager-side portfolio-pager-next";
    nextButton.type = "button";
    nextButton.innerHTML = "&#8594;";
    nextButton.setAttribute("aria-label", "Next portfolio section");
    nextButton.title = "Next section";

    pagerHost.insertBefore(previousButton, scriptElement);
    pagerHost.insertBefore(nextButton, scriptElement);

    let activeIndex = 0;
    let touchStartX = null;
    let touchStartY = null;

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

    function updateFooter() {
      const footerContainer = closestElementContainer(
        pageDocument.querySelector("footer.portfolio-footer")
      );
      if (!footerContainer) {
        return;
      }
      rememberSource(footerContainer);
      footerContainer.style.display =
        activeIndex === sectionIds.length - 1
          ? footerContainer.dataset.portfolioPagerDisplay || ""
          : "none";
    }

    function activate(index, options = {}) {
      const {
        scroll = true,
        updateHash = true,
        direction = index >= activeIndex ? 1 : -1
      } = options;
      const boundedIndex = Math.max(0, Math.min(index, sectionIds.length - 1));
      activeIndex = boundedIndex;

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

      previousButton.disabled = activeIndex === 0;
      nextButton.disabled = activeIndex === sectionIds.length - 1;
      updateNavbar();
      updateFooter();

      if (updateHash) {
        window.history.replaceState(null, "", `#${sectionIds[activeIndex]}`);
      }
      if (scroll) {
        sectionRoots[activeIndex].scrollIntoView({
          behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches
            ? "auto"
            : "smooth",
          block: "start"
        });
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
      if (Math.abs(deltaX) < 55 || Math.abs(deltaX) <= Math.abs(deltaY) * 1.2) {
        return;
      }
      if (deltaX < 0) {
        activate(activeIndex + 1, { direction: 1 });
      } else {
        activate(activeIndex - 1, { direction: -1 });
      }
    }

    function handleHashChange() {
      const targetIndex = sectionIds.indexOf(
        window.location.hash.replace("#", "")
      );
      if (targetIndex >= 0 && targetIndex !== activeIndex) {
        activate(targetIndex, { updateHash: false });
      }
    }

    previousButton.addEventListener("click", () =>
      activate(activeIndex - 1, { direction: -1 })
    );
    nextButton.addEventListener("click", () =>
      activate(activeIndex + 1, { direction: 1 })
    );

    pageDocument.addEventListener("click", handleNavigationClick);
    pageDocument.addEventListener("keydown", handleKeydown);
    pageDocument.addEventListener("touchstart", handleTouchStart, {
      passive: true
    });
    pageDocument.addEventListener("touchend", handleTouchEnd, {
      passive: true
    });
    window.addEventListener("hashchange", handleHashChange);

    window.__portfolioPagerCleanup = () => {
      pageDocument.removeEventListener("click", handleNavigationClick);
      pageDocument.removeEventListener("keydown", handleKeydown);
      pageDocument.removeEventListener("touchstart", handleTouchStart);
      pageDocument.removeEventListener("touchend", handleTouchEnd);
      window.removeEventListener("hashchange", handleHashChange);
      previousButton.remove();
      nextButton.remove();
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
