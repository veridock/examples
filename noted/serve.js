#!/usr/bin/env node

/**
 * Simple Note-Taking PWA Server (Node.js)
 * Serves a self-contained SVG-based note-taking application
 */

const express = require('express');
const fs = require('fs').promises;
const path = require('path');
const { spawn } = require('child_process');

const app = express();
const PORT = 8000;
const NOTES_FILE = 'notes.json';

// Middleware
app.use(express.json({ limit: '10mb' }));
app.use(express.static('public'));

// CORS headers
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
    res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    next();
});

// SVG PWA Application
const getSVGApp = () => {
    return `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="100%" height="100%" viewBox="0 0 1200 800">

  <defs>
    <!-- Embedded CSS -->
    <style type="text/css"><![CDATA[
      .toolbar { fill: #f5f5f5; stroke: #ddd; stroke-width: 1; }
      .button { fill: #2196f3; stroke: #1976d2; stroke-width: 1; cursor: pointer; }
      .button:hover { fill: #1976d2; }
      .button-text { fill: white; font-family: Arial, sans-serif; font-size: 12px; text-anchor: middle; dominant-baseline: middle; pointer-events: none; }
      .tool-active { fill: #ff9800 !important; }
      .canvas-area { fill: white; stroke: #ddd; stroke-width: 1; }
      .text-input { font-family: Arial, sans-serif; font-size: 14px; }
      .note-item { fill: #f9f9f9; stroke: #ddd; stroke-width: 1; cursor: pointer; }
      .note-item:hover { fill: #e3f2fd; }
      .status-text { font-family: Arial, sans-serif; font-size: 12px; fill: #666; }
    ]]></style>
  </defs>

  <!-- Background -->
  <rect width="100%" height="100%" fill="#fafafa"/>

  <!-- Header Toolbar -->
  <rect class="toolbar" x="0" y="0" width="1200" height="60"/>

  <!-- Tool Buttons -->
  <g id="toolbar">
    <!-- Pen Tool -->
    <rect class="button tool-active" id="pen-btn" x="10" y="10" width="60" height="40" rx="4"/>
    <text class="button-text" x="40" y="30">Pen</text>

    <!-- Eraser Tool -->
    <rect class="button" id="eraser-btn" x="80" y="10" width="60" height="40" rx="4"/>
    <text class="button-text" x="110" y="30">Eraser</text>

    <!-- Text Tool -->
    <rect class="button" id="text-btn" x="150" y="10" width="60" height="40" rx="4"/>
    <text class="button-text" x="180" y="30">Text</text>

    <!-- Clear -->
    <rect class="button" id="clear-btn" x="220" y="10" width="60" height="40" rx="4"/>
    <text class="button-text" x="250" y="30">Clear</text>

    <!-- Save -->
    <rect class="button" id="save-btn" x="290" y="10" width="60" height="40" rx="4"/>
    <text class="button-text" x="320" y="30">Save</text>

    <!-- Load -->
    <rect class="button" id="load-btn" x="360" y="10" width="60" height="40" rx="4"/>
    <text class="button-text" x="390" y="30">Load</text>

    <!-- New Note -->
    <rect class="button" id="new-btn" x="430" y="10" width="60" height="40" rx="4"/>
    <text class="button-text" x="460" y="30">New</text>

    <!-- Color Picker -->
    <circle id="color-picker" cx="520" cy="30" r="15" fill="#000000" stroke="#ddd" stroke-width="2"/>

    <!-- Brush Size -->
    <text class="button-text" x="560" y="25" style="fill: #333;">Size:</text>
    <circle id="size-indicator" cx="590" cy="30" r="3" fill="#333"/>

    <!-- Status -->
    <text id="status-text" class="status-text" x="630" y="35">Ready</text>
  </g>

  <!-- Main Content Area -->
  <g id="main-content">
    <!-- Drawing Canvas -->
    <rect class="canvas-area" id="canvas" x="20" y="80" width="800" height="600"/>
    <g id="drawing-layer"></g>
    <g id="text-layer"></g>

    <!-- Notes Panel -->
    <rect class="toolbar" x="840" y="80" width="340" height="600"/>
    <text x="860" y="105" style="font-family: Arial; font-size: 16px; font-weight: bold; fill: #333;">Saved Notes</text>
    <line x1="860" y1="110" x2="1160" y2="110" stroke="#ddd" stroke-width="1"/>
    <g id="notes-list" transform="translate(850, 120)"></g>
  </g>

  <!-- Hidden Elements -->
  <foreignObject x="0" y="0" width="1" height="1" style="overflow: hidden;">
    <input type="color" id="color-input" style="opacity: 0; pointer-events: none;"/>
    <input type="range" id="size-input" min="1" max="20" value="3" style="opacity: 0; pointer-events: none;"/>
  </foreignObject>

  <script type="text/javascript"><![CDATA[
    // PWA Registration
    if ('serviceWorker' in navigator) {
      const swCode = \`
        const CACHE_NAME = 'notepwa-v1';
        self.addEventListener('install', (e) => {
          e.waitUntil(
            caches.open(CACHE_NAME).then((cache) => {
              return cache.addAll(['/']);
            })
          );
        });
        self.addEventListener('fetch', (e) => {
          e.respondWith(
            caches.match(e.request).then((response) => {
              return response || fetch(e.request);
            })
          );
        });
      \`;
      const blob = new Blob([swCode], { type: 'application/javascript' });
      const swUrl = URL.createObjectURL(blob);
      navigator.serviceWorker.register(swUrl);
    }

    // App State
    let currentTool = 'pen';
    let isDrawing = false;
    let currentPath = null;
    let currentColor = '#000000';
    let currentSize = 3;
    let textMode = false;
    let notes = [];
    let currentNoteId = null;

    // Elements
    const canvas = document.getElementById('canvas');
    const drawingLayer = document.getElementById('drawing-layer');
    const textLayer = document.getElementById('text-layer');
    const notesList = document.getElementById('notes-list');
    const statusText = document.getElementById('status-text');

    // Status updates
    function updateStatus(message, isError = false) {
      statusText.textContent = message;
      statusText.setAttribute('fill', isError ? '#f44336' : '#666');
      setTimeout(() => {
        statusText.textContent = 'Ready';
        statusText.setAttribute('fill', '#666');
      }, 3000);
    }

    // Tool Selection
    function selectTool(tool) {
      currentTool = tool;
      textMode = (tool === 'text');

      // Update button states
      document.querySelectorAll('.button').forEach(btn => {
        btn.classList.remove('tool-active');
      });
      document.getElementById(tool + '-btn').classList.add('tool-active');

      // Update cursor
      canvas.style.cursor = textMode ? 'text' : 'crosshair';
      updateStatus(\`\${tool.charAt(0).toUpperCase() + tool.slice(1)} tool selected\`);
    }

    // Drawing Functions
    function startDrawing(e) {
      if (currentTool === 'text') return;

      isDrawing = true;
      const rect = canvas.getBoundingClientRect();
      const svgRect = document.querySelector('svg').getBoundingClientRect();
      const x = e.clientX - svgRect.left - 20;
      const y = e.clientY - svgRect.top - 80;

      currentPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      currentPath.setAttribute('d', \`M \${x} \${y}\`);
      currentPath.setAttribute('fill', 'none');
      currentPath.setAttribute('stroke', currentTool === 'eraser' ? 'white' : currentColor);
      currentPath.setAttribute('stroke-width', currentTool === 'eraser' ? currentSize * 3 : currentSize);
      currentPath.setAttribute('stroke-linecap', 'round');
      currentPath.setAttribute('stroke-linejoin', 'round');

      drawingLayer.appendChild(currentPath);
    }

    function draw(e) {
      if (!isDrawing || currentTool === 'text') return;

      const rect = canvas.getBoundingClientRect();
      const svgRect = document.querySelector('svg').getBoundingClientRect();
      const x = e.clientX - svgRect.left - 20;
      const y = e.clientY - svgRect.top - 80;

      const d = currentPath.getAttribute('d');
      currentPath.setAttribute('d', d + \` L \${x} \${y}\`);
    }

    function stopDrawing() {
      isDrawing = false;
      currentPath = null;
    }

    // Text Functions
    function addText(e) {
      if (currentTool !== 'text') return;

      const rect = canvas.getBoundingClientRect();
      const svgRect = document.querySelector('svg').getBoundingClientRect();
      const x = e.clientX - svgRect.left - 20;
      const y = e.clientY - svgRect.top - 80;

      const text = prompt('Enter text:');
      if (text && text.trim()) {
        const textElement = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        textElement.setAttribute('x', x);
        textElement.setAttribute('y', y);
        textElement.setAttribute('fill', currentColor);
        textElement.setAttribute('font-size', currentSize * 4);
        textElement.setAttribute('font-family', 'Arial, sans-serif');
        textElement.textContent = text;
        textLayer.appendChild(textElement);
        updateStatus('Text added');
      }
    }

    // Save/Load Functions
    function saveNote() {
      const drawingData = drawingLayer.innerHTML;
      const textData = textLayer.innerHTML;
      const timestamp = new Date().toISOString();

      let title = prompt('Note title:', currentNoteId !== null ? notes[currentNoteId]?.title : \`Note \${notes.length + 1}\`);
      if (!title) return;

      const noteData = {
        drawing: drawingData,
        text: textData,
        timestamp: timestamp,
        title: title.trim()
      };

      updateStatus('Saving...');

      fetch('/api/notes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(noteData)
      })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'saved') {
          updateStatus(\`Note "\${title}" saved successfully\`);
          currentNoteId = data.id;
          loadNotes();
        } else {
          updateStatus('Error saving note', true);
        }
      })
      .catch(error => {
        console.error('Error saving note:', error);
        updateStatus('Failed to save note', true);
      });
    }

    function loadNotes() {
      fetch('/api/notes')
      .then(response => response.json())
      .then(data => {
        notes = data;
        renderNotesList();
        updateStatus(\`Loaded \${notes.length} notes\`);
      })
      .catch(error => {
        console.error('Error loading notes:', error);
        updateStatus('Failed to load notes', true);
      });
    }

    function renderNotesList() {
      notesList.innerHTML = '';

      if (notes.length === 0) {
        const emptyText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        emptyText.setAttribute('x', '10');
        emptyText.setAttribute('y', '30');
        emptyText.setAttribute('font-family', 'Arial, sans-serif');
        emptyText.setAttribute('font-size', '12');
        emptyText.setAttribute('fill', '#999');
        emptyText.textContent = 'No saved notes yet';
        notesList.appendChild(emptyText);
        return;
      }

      notes.forEach((note, index) => {
        const noteItem = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        noteItem.setAttribute('transform', \`translate(0, \${index * 70})\`);

        const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        rect.setAttribute('class', 'note-item');
        rect.setAttribute('width', '320');
        rect.setAttribute('height', '60');
        rect.setAttribute('rx', '4');
        if (currentNoteId === index) {
          rect.setAttribute('fill', '#e8f5e8');
          rect.setAttribute('stroke', '#4caf50');
        }

        const title = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        title.setAttribute('x', '10');
        title.setAttribute('y', '20');
        title.setAttribute('font-family', 'Arial, sans-serif');
        title.setAttribute('font-size', '14');
        title.setAttribute('font-weight', 'bold');
        title.textContent = note.title || 'Untitled Note';

        const date = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        date.setAttribute('x', '10');
        date.setAttribute('y', '35');
        date.setAttribute('font-family', 'Arial, sans-serif');
        date.setAttribute('font-size', '10');
        date.setAttribute('fill', '#666');
        date.textContent = new Date(note.timestamp).toLocaleString();

        const deleteBtn = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        deleteBtn.setAttribute('x', '295');
        deleteBtn.setAttribute('y', '20');
        deleteBtn.setAttribute('font-family', 'Arial, sans-serif');
        deleteBtn.setAttribute('font-size', '12');
        deleteBtn.setAttribute('fill', '#f44336');
        deleteBtn.setAttribute('cursor', 'pointer');
        deleteBtn.textContent = '✕';

        noteItem.appendChild(rect);
        noteItem.appendChild(title);
        noteItem.appendChild(date);
        noteItem.appendChild(deleteBtn);

        // Event listeners
        rect.addEventListener('click', () => loadNote(index));
        title.addEventListener('click', () => loadNote(index));
        date.addEventListener('click', () => loadNote(index));
        deleteBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          if (confirm(\`Delete note "\${note.title}"?\`)) {
            deleteNote(index);
          }
        });

        notesList.appendChild(noteItem);
      });
    }

    function loadNote(index) {
      const note = notes[index];
      drawingLayer.innerHTML = note.drawing || '';
      textLayer.innerHTML = note.text || '';
      currentNoteId = index;
      renderNotesList(); // Re-render to show selection
      updateStatus(\`Loaded note: \${note.title}\`);
    }

    function deleteNote(index) {
      fetch(\`/api/notes/\${index}\`, {
        method: 'DELETE'
      })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'deleted') {
          updateStatus('Note deleted');
          if (currentNoteId === index) {
            newNote();
          } else if (currentNoteId > index) {
            currentNoteId--;
          }
          loadNotes();
        }
      })
      .catch(error => {
        console.error('Error deleting note:', error);
        updateStatus('Failed to delete note', true);
      });
    }

    function newNote() {
      clearCanvas();
      currentNoteId = null;
      renderNotesList();
      updateStatus('New note created');
    }

    function clearCanvas() {
      drawingLayer.innerHTML = '';
      textLayer.innerHTML = '';
    }

    // Touch support for mobile
    function getTouchPos(e) {
      const rect = canvas.getBoundingClientRect();
      const svgRect = document.querySelector('svg').getBoundingClientRect();
      return {
        x: e.touches[0].clientX - svgRect.left - 20,
        y: e.touches[0].clientY - svgRect.top - 80
      };
    }

    // Event Listeners
    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('click', addText);

    // Touch events for mobile
    canvas.addEventListener('touchstart', (e) => {
      e.preventDefault();
      const touch = e.touches[0];
      const mouseEvent = new MouseEvent('mousedown', {
        clientX: touch.clientX,
        clientY: touch.clientY
      });
      canvas.dispatchEvent(mouseEvent);
    });

    canvas.addEventListener('touchmove', (e) => {
      e.preventDefault();
      const touch = e.touches[0];
      const mouseEvent = new MouseEvent('mousemove', {
        clientX: touch.clientX,
        clientY: touch.clientY
      });
      canvas.dispatchEvent(mouseEvent);
    });

    canvas.addEventListener('touchend', (e) => {
      e.preventDefault();
      const mouseEvent = new MouseEvent('mouseup', {});
      canvas.dispatchEvent(mouseEvent);
    });

    // Tool buttons
    document.getElementById('pen-btn').addEventListener('click', () => selectTool('pen'));
    document.getElementById('eraser-btn').addEventListener('click', () => selectTool('eraser'));
    document.getElementById('text-btn').addEventListener('click', () => selectTool('text'));
    document.getElementById('clear-btn').addEventListener('click', clearCanvas);
    document.getElementById('save-btn').addEventListener('click', saveNote);
    document.getElementById('load-btn').addEventListener('click', loadNotes);
    document.getElementById('new-btn').addEventListener('click', newNote);

    // Color picker
    document.getElementById('color-picker').addEventListener('click', () => {
      const input = document.getElementById('color-input');
      input.click();
      input.addEventListener('change', (e) => {
        currentColor = e.target.value;
        document.getElementById('color-picker').setAttribute('fill', currentColor);
        updateStatus(\`Color changed to \${currentColor}\`);
      }, { once: true });
    });

    // Size control
    document.getElementById('size-indicator').addEventListener('click', () => {
      const input = document.getElementById('size-input');
      input.style.opacity = '1';
      input.style.position = 'absolute';
      input.style.left = '570px';
      input.style.top = '20px';
      input.style.pointerEvents = 'all';
      input.focus();

      input.addEventListener('input', (e) => {
        currentSize = parseInt(e.target.value);
        document.getElementById('size-indicator').setAttribute('r', Math.max(2, currentSize));
        updateStatus(\`Brush size: \${currentSize}\`);
      });

      input.addEventListener('blur', () => {
        input.style.opacity = '0';
        input.style.position = 'static';
        input.style.pointerEvents = 'none';
      }, { once: true });
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
      if (e.ctrlKey || e.metaKey) {
        switch(e.key) {
          case 's':
            e.preventDefault();
            saveNote();
            break;
          case 'n':
            e.preventDefault();
            newNote();
            break;
          case 'l':
            e.preventDefault();
            loadNotes();
            break;
        }
      }

      // Tool shortcuts
      switch(e.key) {
        case '1':
          selectTool('pen');
          break;
        case '2':
          selectTool('eraser');
          break;
        case '3':
          selectTool('text');
          break;
      }
    });

    // Initialize
    loadNotes();
    selectTool('pen');
    updateStatus('NotePWA loaded successfully');

    // PWA Install prompt
    let deferredPrompt;
    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault();
      deferredPrompt = e;
      updateStatus('App can be installed');
    });
  ]]></script>
</svg>`;
};

// PWA Manifest
const getManifest = () => {
    return {
        name: "NotePWA",
        short_name: "NotePWA",
        description: "Simple note-taking and drawing app",
        start_url: "/",
        display: "standalone",
        background_color: "#ffffff",
        theme_color: "#2196f3",
        icons: [
            {
                src: "data:image/svg+xml;base64," + Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 192 192"><rect width="192" height="192" fill="#2196f3"/><path d="M48 48h96v96H48z" fill="white"/><path d="M64 64h64v8H64zm0 16h64v8H64zm0 16h48v8H64z" fill="#2196f3"/></svg>`).toString('base64'),
                sizes: "192x192",
                type: "image/svg+xml"
            }
        ]
    };
};

// Load notes from file
async function loadNotes() {
    try {
        const data = await fs.readFile(NOTES_FILE, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        // File doesn't exist, return empty array
        return [];
    }
}

// Save notes to file
async function saveNotes(notes) {
    try {
        await fs.writeFile(NOTES_FILE, JSON.stringify(notes, null, 2));
        return true;
    } catch (error) {
        console.error('Error saving notes:', error);
        return false;
    }
}

// Routes
app.get('/', async (req, res) => {
    try {
        const svgContent = await getSVGApp();
        res.setHeader('Content-Type', 'image/svg+xml');
        res.setHeader('Cache-Control', 'no-cache');
        res.send(svgContent);
    } catch (error) {
        console.error('Error serving SVG app:', error);
        res.status(500).send('Error loading application');
    }
});

app.get('/api/info', (req, res) => {
    res.json({
        backend: 'Node.js',
        version: '1.0.0',
        framework: 'Express.js'
    });
});

app.get('/manifest.json', (req, res) => {
    res.json(getManifest());
});

// API Routes
app.get('/api/notes', async (req, res) => {
    try {
        const notes = await loadNotes();
        res.json(notes);
    } catch (error) {
        res.status(500).json({ error: 'Failed to load notes' });
    }
});

app.post('/api/notes', async (req, res) => {
    try {
        const noteData = req.body;
        const notes = await loadNotes();

        // Add timestamp and ID
        noteData.timestamp = new Date().toISOString();
        noteData.id = notes.length;

        // Save note
        notes.push(noteData);
        const saved = await saveNotes(notes);

        if (saved) {
            res.json({ status: 'saved', id: noteData.id });
        } else {
            res.status(500).json({ error: 'Failed to save note' });
        }
    } catch (error) {
        console.error('Error saving note:', error);
        res.status(500).json({ error: 'Failed to save note' });
    }
});

app.delete('/api/notes/:id', async (req, res) => {
    try {
        const noteId = parseInt(req.params.id);
        const notes = await loadNotes();

        if (noteId >= 0 && noteId < notes.length) {
            notes.splice(noteId, 1);

            // Update IDs for remaining notes
            notes.forEach((note, index) => {
                note.id = index;
            });

            const saved = await saveNotes(notes);

            if (saved) {
                res.json({ status: 'deleted' });
            } else {
                res.status(500).json({ error: 'Failed to delete note' });
            }
        } else {
            res.status(404).json({ error: 'Note not found' });
        }
    } catch (error) {
        console.error('Error deleting note:', error);
        res.status(500).json({ error: 'Failed to delete note' });
    }
});

// Error handling
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Something went wrong!' });
});

// 404 handler
app.use((req, res) => {
    res.status(404).json({ error: 'Not found' });
});

// Function to open browser
function openBrowser() {
    setTimeout(() => {
        const url = `http://localhost:${PORT}`;

        // Try different ways to open browser based on platform
        const start = process.platform === 'darwin' ? 'open' :
                     process.platform === 'win32' ? 'start' : 'xdg-open';

        spawn(start, [url], { stdio: 'ignore', detached: true }).unref();
    }, 1000);
}

// Start server
app.listen(PORT, () => {
    console.log('🚀 Starting NotePWA Server...');
    console.log(`📱 Server running at http://localhost:${PORT}`);
    console.log('📝 Features: Drawing, Text notes, Save/Load, PWA support');
    console.log('⌨️  Keyboard shortcuts: Ctrl+S (save), Ctrl+N (new), Ctrl+L (load)');
    console.log('🔧 Tool shortcuts: 1 (pen), 2 (eraser), 3 (text)');
    console.log('📱 Mobile touch support enabled');
    console.log('💾 Notes saved to: notes.json');
    console.log('Press Ctrl+C to stop the server\n');

    // Open browser
    openBrowser();
});

// Graceful shutdown
process.on('SIGTERM', () => {
    console.log('\n🛑 Shutting down server...');
    process.exit(0);
});

process.on('SIGINT', () => {
    console.log('\n🛑 Shutting down server...');
    process.exit(0);
});

module.exports = app;