"""Horizontal section carousel for the Streamlit portfolio."""

import streamlit as st


def render_section_carousel():
    """Turn the static portfolio sections into a swipeable horizontal carousel."""
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
  const sectionLabels = [
    "About Me",
    "Education",
    "Experience",
    "Certifications",
    "Recognitions",
    "Featured Projects",
    "Skills"
  ];
  const styleId = "portfolio-carousel-styles";
  const shellId = "portfolio-section-carousel";
  const sourceAttribute = "data-portfolio-carousel-source";

  let parentDocument;
  try {
    parentDocument = window.parent.document;
  } catch (error) {
    return;
  }

  if (typeof window.parent.__portfolioCarouselCleanup === "function") {
    window.parent.__portfolioCarouselCleanup();
  }

  const carouselStyles = `
    #${shellId} {
      position: relative;
      width: 100%;
      margin: 0;
      scroll-margin-top: 86px;
    }
    #${shellId} .portfolio-carousel-controls {
      position: sticky;
      top: 76px;
      z-index: 35;
      display: grid;
      grid-template-columns: 48px minmax(0, 1fr) 48px;
      align-items: center;
      gap: 12px;
      margin: 0 4px 10px;
      padding: 8px 10px;
      border: 1px solid rgba(255, 209, 102, 0.28);
      border-radius: 14px;
      background: rgba(31, 42, 68, 0.92);
      box-shadow: 0 8px 24px rgba(17, 28, 52, 0.22);
      backdrop-filter: blur(12px);
    }
    #${shellId} .portfolio-carousel-arrow {
      width: 42px;
      height: 42px;
      border: 1px solid rgba(255, 209, 102, 0.55);
      border-radius: 50%;
      background: rgba(255, 209, 102, 0.10);
      color: #ffd166;
      font-size: 1.35rem;
      font-weight: 800;
      cursor: pointer;
      transition: transform 0.18s ease, background 0.18s ease, opacity 0.18s ease;
    }
    #${shellId} .portfolio-carousel-arrow:hover:not(:disabled) {
      transform: translateY(-2px) scale(1.04);
      background: rgba(255, 209, 102, 0.22);
    }
    #${shellId} .portfolio-carousel-arrow:disabled {
      cursor: default;
      opacity: 0.32;
    }
    #${shellId} .portfolio-carousel-status {
      min-width: 0;
      text-align: center;
    }
    #${shellId} .portfolio-carousel-title {
      display: block;
      color: #ffd166;
      font-size: 1rem;
      font-weight: 800;
      line-height: 1.25;
    }
    #${shellId} .portfolio-carousel-count {
      display: block;
      margin-top: 2px;
      color: rgba(255, 255, 255, 0.72);
      font-size: 0.76rem;
    }
    #${shellId} .portfolio-carousel-track {
      display: flex;
      width: 100%;
      gap: 0;
      overflow-x: auto;
      overflow-y: hidden;
      scroll-behavior: smooth;
      scroll-snap-type: x mandatory;
      overscroll-behavior-x: contain;
      scrollbar-width: none;
      transition: height 0.36s ease;
      touch-action: pan-x pan-y;
    }
    #${shellId} .portfolio-carousel-track::-webkit-scrollbar {
      display: none;
    }
    #${shellId} .portfolio-carousel-slide {
      flex: 0 0 100%;
      width: 100%;
      min-width: 100%;
      padding: 0 4px 6px;
      box-sizing: border-box;
      scroll-snap-align: start;
      scroll-snap-stop: always;
      transform-origin: center top;
    }
    #${shellId} .portfolio-carousel-slide.is-active {
      animation: portfolio-page-pop 0.52s cubic-bezier(0.22, 0.82, 0.32, 1);
    }
    #${shellId} .portfolio-carousel-dots {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 8px;
      padding: 12px 8px 2px;
    }
    #${shellId} .portfolio-carousel-dot {
      width: 9px;
      height: 9px;
      padding: 0;
      border: 0;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.38);
      cursor: pointer;
      transition: width 0.2s ease, background 0.2s ease, transform 0.2s ease;
    }
    #${shellId} .portfolio-carousel-dot.is-active {
      width: 28px;
      background: #ffd166;
    }
    #${shellId}:focus-visible {
      outline: 2px solid #ffd166;
      outline-offset: 4px;
    }
    @keyframes portfolio-page-pop {
      0% {
        opacity: 0.12;
        transform: translateY(20px) scale(0.94);
      }
      65% {
        opacity: 1;
        transform: translateY(-3px) scale(1.012);
      }
      100% {
        opacity: 1;
        transform: translateY(0) scale(1);
      }
    }
    @media (max-width: 700px) {
      #${shellId} .portfolio-carousel-controls {
        top: 68px;
        grid-template-columns: 42px minmax(0, 1fr) 42px;
        gap: 7px;
        margin-inline: 0;
      }
      #${shellId} .portfolio-carousel-arrow {
        width: 38px;
        height: 38px;
      }
      #${shellId} .portfolio-carousel-title {
        font-size: 0.92rem;
      }
      #${shellId} .portfolio-carousel-slide {
        padding-inline: 0;
      }
    }
    @media (prefers-reduced-motion: reduce) {
      #${shellId} .portfolio-carousel-track {
        scroll-behavior: auto;
        transition: none;
      }
      #${shellId} .portfolio-carousel-slide.is-active {
        animation: none;
      }
      #${shellId} .portfolio-carousel-arrow,
      #${shellId} .portfolio-carousel-dot {
        transition: none;
      }
    }
  `;

  function installStyles() {
    let style = parentDocument.getElementById(styleId);
    if (!style) {
      style = parentDocument.createElement("style");
      style.id = styleId;
      parentDocument.head.appendChild(style);
    }
    style.textContent = carouselStyles;
  }

  function restoreSources() {
    parentDocument.querySelectorAll(`[${sourceAttribute}="true"]`).forEach((node) => {
      node.style.display = node.dataset.portfolioCarouselDisplay || "";
      node.removeAttribute(sourceAttribute);
      delete node.dataset.portfolioCarouselDisplay;
    });
  }

  function closestElementContainer(element) {
    return element?.closest('div[data-testid="stElementContainer"]') || null;
  }

  function buildCarousel(attempt = 0) {
    restoreSources();
    parentDocument.getElementById(shellId)?.remove();

    const anchors = sectionIds.map((id) =>
      parentDocument.querySelector(`a.section-anchor[name="${id}"]`)
    );
    const endMarker = parentDocument.querySelector(".portfolio-carousel-end-marker");

    if (anchors.some((anchor) => !anchor) || !endMarker) {
      if (attempt < 80) {
        window.setTimeout(() => buildCarousel(attempt + 1), 75);
      }
      return;
    }

    const starts = anchors.map(closestElementContainer);
    const endContainer = closestElementContainer(endMarker);
    const sectionParent = starts[0]?.parentElement;

    if (
      !sectionParent ||
      !endContainer ||
      starts.some((start) => !start || start.parentElement !== sectionParent) ||
      endContainer.parentElement !== sectionParent
    ) {
      if (attempt < 80) {
        window.setTimeout(() => buildCarousel(attempt + 1), 75);
      }
      return;
    }

    installStyles();

    const shell = parentDocument.createElement("section");
    shell.id = shellId;
    shell.tabIndex = 0;
    shell.setAttribute("aria-label", "Portfolio section carousel");

    const controls = parentDocument.createElement("div");
    controls.className = "portfolio-carousel-controls";

    const previousButton = parentDocument.createElement("button");
    previousButton.className = "portfolio-carousel-arrow";
    previousButton.type = "button";
    previousButton.innerHTML = "&#8592;";
    previousButton.setAttribute("aria-label", "Previous portfolio section");
    previousButton.title = "Previous section";

    const status = parentDocument.createElement("div");
    status.className = "portfolio-carousel-status";
    status.setAttribute("aria-live", "polite");
    const title = parentDocument.createElement("span");
    title.className = "portfolio-carousel-title";
    const count = parentDocument.createElement("span");
    count.className = "portfolio-carousel-count";
    status.append(title, count);

    const nextButton = parentDocument.createElement("button");
    nextButton.className = "portfolio-carousel-arrow";
    nextButton.type = "button";
    nextButton.innerHTML = "&#8594;";
    nextButton.setAttribute("aria-label", "Next portfolio section");
    nextButton.title = "Next section";

    controls.append(previousButton, status, nextButton);

    const track = parentDocument.createElement("div");
    track.className = "portfolio-carousel-track";
    track.setAttribute("aria-label", "Swipe or use the arrows to view portfolio sections");

    const dots = parentDocument.createElement("div");
    dots.className = "portfolio-carousel-dots";
    dots.setAttribute("aria-label", "Choose a portfolio section");

    const slides = [];
    const dotButtons = [];

    starts.forEach((start, index) => {
      const stop = index + 1 < starts.length ? starts[index + 1] : endContainer;
      const slide = parentDocument.createElement("section");
      slide.className = "portfolio-carousel-slide";
      slide.dataset.sectionId = sectionIds[index];
      slide.setAttribute("aria-label", sectionLabels[index]);

      let node = start;
      while (node && node !== stop) {
        const clone = node.cloneNode(true);
        slide.appendChild(clone);
        node.dataset.portfolioCarouselDisplay = node.style.display || "";
        node.setAttribute(sourceAttribute, "true");
        node.style.display = "none";
        node = node.nextSibling;
      }

      const dot = parentDocument.createElement("button");
      dot.className = "portfolio-carousel-dot";
      dot.type = "button";
      dot.setAttribute("aria-label", `Show ${sectionLabels[index]}`);
      dot.title = sectionLabels[index];

      slides.push(slide);
      dotButtons.push(dot);
      track.appendChild(slide);
      dots.appendChild(dot);
    });

    shell.append(controls, track, dots);
    sectionParent.insertBefore(shell, starts[0]);

    let activeIndex = 0;
    let scrollTimer;

    function updateHeight() {
      window.requestAnimationFrame(() => {
        const activeSlide = slides[activeIndex];
        if (activeSlide) {
          track.style.height = `${Math.max(activeSlide.scrollHeight, 120)}px`;
        }
      });
    }

    function activate(index, shouldScroll = true, updateHash = true) {
      const boundedIndex = Math.max(0, Math.min(index, slides.length - 1));
      activeIndex = boundedIndex;

      slides.forEach((slide, slideIndex) => {
        const isActive = slideIndex === activeIndex;
        slide.classList.remove("is-active");
        slide.setAttribute("aria-hidden", isActive ? "false" : "true");
        if (isActive) {
          void slide.offsetWidth;
          slide.classList.add("is-active");
        }
      });

      dotButtons.forEach((dot, dotIndex) => {
        const isActive = dotIndex === activeIndex;
        dot.classList.toggle("is-active", isActive);
        dot.setAttribute("aria-current", isActive ? "true" : "false");
      });

      title.textContent = sectionLabels[activeIndex];
      count.textContent = `${activeIndex + 1} of ${slides.length}`;
      previousButton.disabled = activeIndex === 0;
      nextButton.disabled = activeIndex === slides.length - 1;

      if (shouldScroll) {
        track.scrollTo({
          left: slides[activeIndex].offsetLeft,
          behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches
            ? "auto"
            : "smooth"
        });
      }

      if (updateHash) {
        window.parent.history.replaceState(null, "", `#${sectionIds[activeIndex]}`);
      }

      updateHeight();
    }

    function showFromNavigation(index) {
      shell.scrollIntoView({
        behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches
          ? "auto"
          : "smooth",
        block: "start"
      });
      activate(index);
    }

    previousButton.addEventListener("click", () => activate(activeIndex - 1));
    nextButton.addEventListener("click", () => activate(activeIndex + 1));

    dotButtons.forEach((dot, index) => {
      dot.addEventListener("click", () => activate(index));
    });

    shell.addEventListener("keydown", (event) => {
      if (event.key === "ArrowLeft") {
        event.preventDefault();
        activate(activeIndex - 1);
      } else if (event.key === "ArrowRight") {
        event.preventDefault();
        activate(activeIndex + 1);
      }
    });

    track.addEventListener("scroll", () => {
      window.clearTimeout(scrollTimer);
      scrollTimer = window.setTimeout(() => {
        const nearestIndex = Math.round(track.scrollLeft / Math.max(track.clientWidth, 1));
        if (nearestIndex !== activeIndex) {
          activate(nearestIndex, false);
        }
      }, 90);
    });

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
      showFromNavigation(targetIndex);
    }

    parentDocument.addEventListener("click", handleNavigationClick);

    const resizeObserver = new ResizeObserver(updateHeight);
    slides.forEach((slide) => resizeObserver.observe(slide));
    slides.forEach((slide) => {
      slide.querySelectorAll("img").forEach((image) => {
        if (!image.complete) {
          image.addEventListener("load", updateHeight, { once: true });
        }
      });
    });

    function handleParentResize() {
      track.scrollTo({ left: slides[activeIndex].offsetLeft, behavior: "auto" });
      updateHeight();
    }

    window.parent.addEventListener("resize", handleParentResize);
    window.parent.__portfolioCarouselCleanup = () => {
      parentDocument.removeEventListener("click", handleNavigationClick);
      window.parent.removeEventListener("resize", handleParentResize);
      resizeObserver.disconnect();
      restoreSources();
      shell.remove();
    };

    const requestedIndex = sectionIds.indexOf(
      window.parent.location.hash.replace("#", "")
    );
    activate(requestedIndex >= 0 ? requestedIndex : 0, false, false);
    window.setTimeout(updateHeight, 120);
    window.setTimeout(updateHeight, 500);
  }

  buildCarousel();
})();
</script>
        """,
        unsafe_allow_javascript=True,
    )
