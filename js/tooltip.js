document.addEventListener('DOMContentLoaded', () => {

    // --- Definitions for Tooltip ---
    const definitions = {
        'ml': {
            word: 'Machine Learning',
            type: 'Noun',
            phonetic: '/məˌʃiːn ˈlɜː.nɪŋ/',
            def: 'The remarkable process by which computers, after being meticulously trained with vast amounts of data and complex algorithms designed by humans, are celebrated for "learning on their own"—all while requiring constant tuning, retraining, and debugging.'
        }
        
    };

    // --- Tooltip Logic ---
    const tooltipBubble = document.getElementById('tooltip-bubble');
    const triggers = document.querySelectorAll('.tooltip-trigger');

    if (tooltipBubble && triggers.length > 0) {
        triggers.forEach(trigger => {
            let timeoutId = null;

            trigger.addEventListener('mouseenter', (event) => {
                clearTimeout(timeoutId); // Clear any lingering hide timeout
                const term = trigger.getAttribute('data-term');
                const definitionData = definitions[term];

                if (definitionData) {
                    // Populate tooltip
                    tooltipBubble.innerHTML = `
                    <span class="tooltip-word">${definitionData.word}</span>
                    ${definitionData.type ? `<span class="tooltip-type">${definitionData.type}</span>` : ''}
                    ${definitionData.phonetic ? `<span class="tooltip-phonetic">${definitionData.phonetic}</span>` : ''}
                    <span class="tooltip-def">${definitionData.def}</span>
                `;

                    // Position tooltip
                    const triggerRect = trigger.getBoundingClientRect();
                    const bubbleRect = tooltipBubble.getBoundingClientRect(); // Get initial size estimation

                    let top = triggerRect.top + window.scrollY - bubbleRect.height - 10; // 10px spacing above
                    let left = triggerRect.left + window.scrollX + (triggerRect.width / 2) - (bubbleRect.width / 2);

                    const viewportWidth = document.documentElement.clientWidth;
                    if (left < 10) {
                        left = 10; // Minimum left padding
                    } else if (left + bubbleRect.width > viewportWidth - 10) {
                        left = viewportWidth - bubbleRect.width - 10; // Adjust from right edge
                    }

                    if (top < window.scrollY + 10) {
                        top = triggerRect.bottom + window.scrollY + 10;
                    }


                    tooltipBubble.style.top = `${top}px`;
                    tooltipBubble.style.left = `${left}px`;

                    // Show tooltip
                    tooltipBubble.classList.add('visible');
                }
            });

            trigger.addEventListener('mouseleave', () => {
                // Delay hiding to allow mouse movement into the tooltip
                timeoutId = setTimeout(() => {
                    tooltipBubble.classList.remove('visible');
                }, 100); // Small delay before hiding
            });
        });

        // Hide tooltip if clicked outside (though mouseleave usually covers it)
        document.addEventListener('click', (event) => {
            if (!event.target.classList.contains('tooltip-trigger')) {
                tooltipBubble.classList.remove('visible');
            }
        });

    } else {
        if (!tooltipBubble) console.warn("Tooltip bubble element not found.");
        if (triggers.length === 0) console.log("No tooltip triggers found on this page.");
    }

});