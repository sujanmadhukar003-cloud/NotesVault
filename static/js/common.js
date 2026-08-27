document.addEventListener('DOMContentLoaded', function () {
    if (typeof renderMathInElement === 'function') {
        renderMathInElement(document.body, {
            delimiters: [
                { left: '$$', right: '$$', display: true },
                { left: '\\(', right: '\\)', display: false }
            ]
        });
    }

    const dropdowns = document.querySelectorAll('[data-dropdown-toggle]');
    dropdowns.forEach((button) => {
        button.addEventListener('click', function () {
            const target = document.getElementById(this.getAttribute('data-dropdown-toggle'));
            if (!target) return;
            const isHidden = target.classList.contains('hidden');
            document.querySelectorAll('[data-dropdown-panel]').forEach((panel) => {
                if (panel !== target) panel.classList.add('hidden');
            });
            target.classList.toggle('hidden', !isHidden);
        });
    });
});

function toggleTopic(element) {
    const content = element.nextElementSibling;
    const icon = element.querySelector('.toggle-icon');
    if (!content) return;

    const isHidden = content.classList.contains('hidden');
    content.classList.toggle('hidden', !isHidden);
    if (icon) {
        icon.style.transform = isHidden ? 'rotate(180deg)' : 'rotate(0deg)';
    }
}

function openFullscreen(id) {
    const element = document.getElementById(id);
    if (!element) return;
    if (element.requestFullscreen) {
        element.requestFullscreen();
    } else if (element.webkitRequestFullscreen) {
        element.webkitRequestFullscreen();
    } else if (element.msRequestFullscreen) {
        element.msRequestFullscreen();
    }
}
