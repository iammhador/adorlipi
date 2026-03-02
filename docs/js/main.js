document.addEventListener('DOMContentLoaded', async () => {
    const inputArea = document.getElementById('input-text');
    const outputArea = document.getElementById('output-text');
    const loadingInd = document.getElementById('loading-indicator');
    const readyInd = document.getElementById('ready-indicator');
    const copyBtn = document.getElementById('copy-btn');

    let adorlipi = null;

    try {
        // Fetch dictionaries and mapping rules
        const dictRes = await fetch('data/dictionary.json');
        const mappingRes = await fetch('data/mapping.json');

        // Fetch patterns.json if exists, else gracefully catch
        let patternsData = { patterns: [] };
        try {
            const patternRes = await fetch('data/patterns.json');
            if (patternRes.ok) patternsData = await patternRes.json();
        } catch (e) {
            console.log("No patterns.json found, skipping.");
        }

        const dictionaryData = await dictRes.json();
        const mappingData = await mappingRes.json();

        adorlipi = new Transliterator(dictionaryData, mappingData, patternsData);

        // UI Updates
        loadingInd.classList.add('hidden');
        readyInd.classList.remove('hidden');
        inputArea.disabled = false;
        inputArea.focus();

        // Listen to input and transliterate
        inputArea.addEventListener('input', () => {
            if (!adorlipi) return;
            const text = inputArea.value;
            const translated = adorlipi.transliterate(text);
            outputArea.value = translated;
        });

    } catch (err) {
        console.error("Failed to load engine data:", err);
        loadingInd.innerHTML = '⚠️ Failed to load engine files. Ensure data/ exists.';
    }

    // Copy action
    copyBtn.addEventListener('click', () => {
        outputArea.select();
        document.execCommand('copy');

        const originalHtml = copyBtn.innerHTML;
        copyBtn.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#22c55e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>';
        setTimeout(() => copyBtn.innerHTML = originalHtml, 2000);
    });
});
