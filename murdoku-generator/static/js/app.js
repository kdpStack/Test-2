/**
 * Murdoku Generator - Frontend JavaScript
 * Handles user interactions and API communication
 */

// Current puzzle state
let currentPuzzle = null;
let currentStory = null;

// Tab switching functionality
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        // Remove active class from all tabs
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        
        // Add active class to clicked tab
        btn.classList.add('active');
        document.getElementById(btn.dataset.tab).classList.add('active');
    });
});

// Generate single puzzle
document.getElementById('btn-generate').addEventListener('click', async () => {
    const size = parseInt(document.getElementById('grid-size').value);
    const difficulty = document.getElementById('difficulty').value;
    const storyCategory = document.getElementById('story-category').value;
    const customCategories = document.getElementById('custom-categories').value;
    
    const categories = customCategories ? customCategories.split(',').map(c => c.trim()) : null;
    
    const btn = document.getElementById('btn-generate');
    btn.disabled = true;
    btn.innerHTML = '<span class="loading"></span> Generating...';
    
    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                size,
                difficulty,
                story_category: storyCategory,
                categories
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentPuzzle = data.puzzle;
            currentStory = data.story;
            
            displayPuzzle(data);
        } else {
            alert('Failed to generate puzzle');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while generating the puzzle');
    } finally {
        btn.disabled = false;
        btn.textContent = 'Generate Puzzle';
    }
});

// Display generated puzzle
function displayPuzzle(data) {
    const resultPanel = document.getElementById('puzzle-result');
    const storyInfo = document.getElementById('story-info');
    const puzzleGrid = document.getElementById('puzzle-grid');
    const cluesList = document.getElementById('clues-list');
    const verificationStatus = document.getElementById('verification-status');
    
    // Story info
    storyInfo.innerHTML = `
        <h4>${data.story.title || 'Logic Puzzle'}</h4>
        <p>${data.story.intro || ''}</p>
        <p><strong>Context:</strong> ${data.story.context || ''}</p>
    `;
    
    // Grid display
    const size = data.puzzle.size;
    const categories = data.puzzle.categories;
    
    let gridHtml = '<div class="grid-display" style="grid-template-columns: repeat(' + (size + 1) + ', 1fr);">';
    
    // Header row
    gridHtml += '<div class="grid-cell grid-header"></div>';
    for (let i = 0; i < size; i++) {
        gridHtml += `<div class="grid-cell grid-header">${i + 1}</div>`;
    }
    
    // Data rows
    for (let cat = 0; cat < size; cat++) {
        gridHtml += `<div class="grid-cell grid-header">${categories[cat] || `Cat ${cat + 1}`}</div>`;
        for (let val = 0; val < size; val++) {
            gridHtml += `<div class="grid-cell">${val + 1}</div>`;
        }
    }
    
    gridHtml += '</div>';
    puzzleGrid.innerHTML = gridHtml;
    
    // Clues list
    const clues = data.puzzle.clues || [];
    let cluesHtml = '<h4>Clues (' + clues.length + ')</h4><div style="max-height: 300px; overflow-y: auto;">';
    clues.forEach((clue, index) => {
        const typeClass = `clue-type-${clue.type || 'direct'}`;
        cluesHtml += `<div class="clue-item ${typeClass}"><strong>${index + 1}.</strong> ${clue.text}</div>`;
    });
    cluesHtml += '</div>';
    cluesList.innerHTML = cluesHtml;
    
    // Verification status
    const statusClass = data.verified ? 'status-valid' : 'status-invalid';
    const statusIcon = data.verified ? '✓' : '✗';
    verificationStatus.innerHTML = `
        <div class="${statusClass}">
            ${statusIcon} ${data.verification_message}
        </div>
    `;
    
    resultPanel.style.display = 'block';
    resultPanel.scrollIntoView({ behavior: 'smooth' });
}

// Export buttons
document.getElementById('btn-export-pdf').addEventListener('click', () => exportPuzzle('pdf'));
document.getElementById('btn-export-png').addEventListener('click', () => exportPuzzle('png'));
document.getElementById('btn-export-json').addEventListener('click', () => exportPuzzle('json'));

async function exportPuzzle(format) {
    if (!currentPuzzle) {
        alert('Please generate a puzzle first');
        return;
    }
    
    try {
        const response = await fetch('/api/export', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                puzzle: currentPuzzle,
                story: currentStory,
                format: format,
                filename: `puzzle-${Date.now()}`
            })
        });
        
        const data = await response.json();
        
        if (data.success && data.download_url) {
            window.location.href = data.download_url;
        } else {
            alert('Export failed');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while exporting');
    }
}

// Bulk generation
document.getElementById('btn-bulk-generate').addEventListener('click', async () => {
    const quantity = parseInt(document.getElementById('bulk-quantity').value);
    const size = parseInt(document.getElementById('bulk-size').value);
    const difficulty = document.getElementById('bulk-difficulty').value;
    const category = document.getElementById('bulk-category').value;
    const format = document.getElementById('bulk-format').value;
    
    const btn = document.getElementById('btn-bulk-generate');
    const progressPanel = document.getElementById('bulk-progress');
    const progressFill = document.getElementById('progress-fill');
    const progressText = document.getElementById('progress-text');
    
    btn.disabled = true;
    progressPanel.style.display = 'block';
    progressFill.style.width = '0%';
    
    try {
        // Simulate progress
        let progress = 0;
        const interval = setInterval(() => {
            progress += 5;
            if (progress > 90) progress = 90;
            progressFill.style.width = progress + '%';
            progressText.textContent = `Generating puzzles... ${Math.floor(progress)}%`;
        }, 200);
        
        const response = await fetch('/api/bulk-generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                quantity,
                size,
                difficulty,
                story_category: category,
                export_format: format
            })
        });
        
        clearInterval(interval);
        progressFill.style.width = '100%';
        progressText.textContent = 'Complete!';
        
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('bulk-count').textContent = 
                `Successfully generated ${data.count} verified puzzles`;
            
            const downloadLink = document.getElementById('bulk-download');
            downloadLink.href = data.download_url;
            downloadLink.textContent = `Download ${format.toUpperCase()}`;
            
            document.getElementById('bulk-result').style.display = 'block';
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred during bulk generation');
    } finally {
        btn.disabled = false;
    }
});

// Verify puzzle
document.getElementById('btn-verify').addEventListener('click', async () => {
    const input = document.getElementById('verify-input').value;
    
    try {
        const puzzleData = JSON.parse(input);
        
        const response = await fetch('/api/verify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ puzzle: puzzleData })
        });
        
        const data = await response.json();
        
        const resultPanel = document.getElementById('verify-result');
        const statusDiv = document.getElementById('verify-status');
        const messageDiv = document.getElementById('verify-message');
        
        const statusClass = data.valid ? 'status-valid' : 'status-invalid';
        const statusIcon = data.valid ? '✓' : '✗';
        
        statusDiv.className = statusClass;
        statusDiv.textContent = `${statusIcon} Verification ${data.valid ? 'Passed' : 'Failed'}`;
        messageDiv.textContent = data.message || '';
        
        resultPanel.style.display = 'block';
    } catch (error) {
        alert('Invalid JSON format');
    }
});

// Export from export tab
document.getElementById('btn-export').addEventListener('click', async () => {
    const puzzleJson = document.getElementById('export-puzzle-json').value;
    const storyJson = document.getElementById('export-story-json').value;
    const format = document.getElementById('export-format').value;
    const filename = document.getElementById('export-filename').value;
    
    try {
        const puzzle = JSON.parse(puzzleJson);
        let story = {};
        
        if (storyJson) {
            story = JSON.parse(storyJson);
        }
        
        const response = await fetch('/api/export', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                puzzle,
                story,
                format,
                filename
            })
        });
        
        const data = await response.json();
        
        if (data.success && data.download_url) {
            window.location.href = data.download_url;
        } else {
            alert('Export failed');
        }
    } catch (error) {
        alert('Invalid JSON format');
    }
});

// Load story categories on page load
async function loadStoryCategories() {
    try {
        const response = await fetch('/api/story-categories');
        const data = await response.json();
        
        if (data.success) {
            // Could populate dropdown dynamically
            console.log('Available categories:', data.categories);
        }
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

loadStoryCategories();

console.log('Murdoku Generator loaded successfully');
