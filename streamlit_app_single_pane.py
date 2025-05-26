st.markdown(
    """
    <style>
    .nav-bar {
        display: flex;
        justify-content: center;
        gap: 36px;
        background: rgba(44,62,80,0.90);
        padding: 16px 0 6px 0;
        border-radius: 0 0 20px 20px;
        position: sticky;
        top: 0;
        z-index: 99;
        margin-bottom: 28px;
    }
    .nav-link {
        background: linear-gradient(135deg, #1F2A44 0%, #324665 100%);
        color: #ffd166 !important;
        text-decoration: none;
        font-weight: bold;
        font-size: 1.13rem;
        letter-spacing: 1px;
        padding: 10px 26px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(44,62,80,0.15);
        transition: transform .3s cubic-bezier(.4,1.6,.6,1), box-shadow .3s, background .22s;
        display: inline-block;
        margin-bottom: 0;
    }
    .nav-link:hover, .nav-link:focus {
        transform: translateY(-5px) scale(1.07);
        box-shadow: 0 8px 16px rgba(0,0,0,0.24);
        background: linear-gradient(135deg, #406496 0%, #22304A 100%);
        color: #fff !important;
        text-decoration: none;
    }
    </style>
    <div class="nav-bar">
        <a class="nav-link" href="#about-me">About</a>
        <a class="nav-link" href="#projects-gallery">Projects</a>
        <a class="nav-link" href="#professional-experience">Experience</a>
        <a class="nav-link" href="#core-skills-tools">Skills</a>
        <a class="nav-link" href="#contact">Contact</a>
    </div>
    """,
    unsafe_allow_html=True,
)
