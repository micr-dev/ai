document.addEventListener('DOMContentLoaded', () => {
  const rawCodeElement = document.getElementById('raw-agents-code');
  const lineNumbersContainer = document.getElementById('editor-line-numbers');
  const openRenderedBtn = document.getElementById('open-rendered-btn');
  const closeRenderedBtn = document.getElementById('close-modal-btn');
  const agentsModal = document.getElementById('agents-modal');
  const renderedContainer = document.getElementById('rendered-agents-container');
  
  let agentsMarkdownContent = '';

  // 1. FETCH & PROCESS AGENTS.MD FOR THE CODE BOX
  fetch('AGENTS.md')
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to fetch AGENTS.md');
      }
      return response.text();
    })
    .then(text => {
      agentsMarkdownContent = text;
      
      // Escape HTML tags to prevent execution in code view
      const escapedText = text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
      
      rawCodeElement.innerHTML = escapedText;
      
      // Generate IDE line numbers
      const lines = text.split('\n');
      let lineNumsHtml = '';
      for (let i = 1; i <= lines.length; i++) {
        lineNumsHtml += `<div>${i}</div>`;
      }
      lineNumbersContainer.innerHTML = lineNumsHtml;
    })
    .catch(error => {
      console.error(error);
      rawCodeElement.textContent = 'Failed to load AGENTS.md. Ensure the file is present in the workspace root.';
    });

  // 2. LIGHTWEIGHT MARKDOWN TO HTML RENDERER
  function renderMarkdown(md) {
    if (!md) return '<p>No content available.</p>';
    
    let html = md;
    
    // Style Redactions [REDACTED] or ███████
    html = html.replace(/\[REDACTED\]/g, '<span class="redacted-text">[REDACTED]</span>');
    html = html.replace(/███████/g, '<span class="redacted-block">███████</span>');
    
    // GitHub style alerts: > [!IMPORTANT]
    // Matches blockquotes starting with an alert label
    html = html.replace(/^>\s*\[!(IMPORTANT|NOTE|WARNING|TIP|CAUTION)\]\s*\n([\s\S]*?)(?=^\s*---|^\s*#|^\s*$)/gm, (match, type, content) => {
      const cleanContent = content.trim().replace(/^>\s*/gm, '');
      return `<div class="gh-alert alert-${type.toLowerCase()}"><strong>[${type}]</strong><br>${cleanContent}</div>`;
    });
    
    // Blockquotes (standard)
    html = html.replace(/^>\s+(.+)$/gm, '<blockquote>$1</blockquote>');
    
    // Headers (# -> h1, ## -> h2, ### -> h3)
    html = html.replace(/^#\s+(.+)$/gm, '<h1>$1</h1>');
    html = html.replace(/^##\s+(.+)$/gm, '<h2>$1</h2>');
    html = html.replace(/^###\s+(.+)$/gm, '<h3>$1</h3>');
    
    // Code blocks (```json ... ```)
    html = html.replace(/```(\w+)?\n([\s\S]*?)\n```/gm, (match, lang, code) => {
      const escapedCode = code.replace(/</g, '&lt;').replace(/>/g, '&gt;');
      return `<pre><code class="language-${lang || 'text'}">${escapedCode}</code></pre>`;
    });
    
    // Unordered Lists (- item)
    // Wrap consecutive list items in <ul>...</ul>
    html = html.replace(/^\s*-\s+(.+)$/gm, '<li>$1</li>');
    html = html.replace(/(<li>.*<\/li>)/gms, '<ul>$1</ul>');
    html = html.replace(/<\/ul>\s*<ul>/g, ''); // consolidate adjacent lists
    
    // Inline bold, italic, code
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
    html = html.replace(/`(.*?)`/g, '<code>$1</code>');
    
    // Horizontal Rules
    html = html.replace(/^---$/gm, '<hr>');
    
    // Split into paragraphs (avoiding blocks already formatted)
    const paragraphs = html.split(/\n\n+/);
    html = paragraphs.map(p => {
      const trimmed = p.trim();
      if (!trimmed) return '';
      // If it starts with an HTML block element, do not wrap in <p>
      if (trimmed.startsWith('<h') || 
          trimmed.startsWith('<ul') || 
          trimmed.startsWith('<pre') || 
          trimmed.startsWith('<div') || 
          trimmed.startsWith('<hr') || 
          trimmed.startsWith('<li') || 
          trimmed.startsWith('<blockquote>')) {
        return trimmed;
      }
      return `<p>${trimmed}</p>`;
    }).join('\n');
    
    return html;
  }

  // 3. INSTANT MODAL OVERLAY (NO FADES)
  function openModal() {
    renderedContainer.innerHTML = renderMarkdown(agentsMarkdownContent);
    agentsModal.style.display = 'flex';
  }

  function closeModal() {
    agentsModal.style.display = 'none';
  }

  openRenderedBtn.addEventListener('click', openModal);
  closeRenderedBtn.addEventListener('click', closeModal);
  
  // Close on backdrop click
  agentsModal.addEventListener('click', (e) => {
    if (e.target === agentsModal) {
      closeModal();
    }
  });

  // Close on Escape key press
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && agentsModal.style.display === 'flex') {
      closeModal();
    }
  });

  // 4. INTERACTIVE SKILL CONSTELLATION MAP
  const constellationData = {
    'claude-3-5-sonnet': {
      type: 'primary model',
      title: 'claude 3.5 sonnet (v2)',
      description: 'default language model for system design, deep logic, and structural refactoring.',
      why: 'exhibits superior comprehension of complex codebase context and high adherence to strict system instructions.',
      link: 'https://www.anthropic.com/claude/sonnet'
    },
    'gemini-1-5-pro': {
      type: 'secondary model',
      title: 'gemini 1.5 pro',
      description: 'secondary model utilized for codebase-wide repository indexing and multimodality verification.',
      why: 'leverages an expansive 2-million token window to ingest full codebase directories without context fragmentation.',
      link: 'https://deepmind.google/technologies/gemini/'
    },
    'cursor': {
      type: 'primary harness',
      title: 'cursor',
      description: 'ai-native editor acting as the primary system developer interface.',
      why: 'provides deep integration of inline ai prompting, composer agents, and local codebase indexing.',
      link: 'https://www.cursor.com/'
    },
    'aider': {
      type: 'secondary harness',
      title: 'aider',
      description: 'cli-driven autonomous git-pairing assistant for rapid feature iterations.',
      why: 'excels at executing multi-file surgical modifications directly from terminal shell environments.',
      link: 'https://aider.chat/'
    },
    'agents-md': {
      type: 'agent operating manual',
      title: 'agents.md',
      description: 'committed public, redacted rendering of the global operating manual.',
      why: 'formulated strict agent sandbox controls and redaction boundaries to secure public repository publishing.',
      link: '#agents-section'
    }
  };

  const detailsPanel = document.getElementById('constellation-details-panel');
  const constellationNodes = document.querySelectorAll('.constellation-node');
  const constellationLines = document.querySelectorAll('.constellation-line');

  function updateDetailsPanel(node) {
    const isHttpLink = node.link.startsWith('http');
    detailsPanel.innerHTML = `
      <div class="constellation-detail-card font-sans">
        <span class="constellation-detail-type">${node.type}</span>
        <div class="constellation-detail-title-row">
          <a href="${node.link}" ${isHttpLink ? 'target="_blank" rel="noopener noreferrer"' : ''} class="constellation-detail-title">
            <span>${node.title}</span>
            ${isHttpLink ? `
            <svg class="link-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true" style="width: 14px; height: 14px; display: inline-block;">
              <path d="M11 3a1 1 0 100 2h2.586l-6.293 6.293a1 1 0 101.414 1.414L15 6.414V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z"></path>
              <path d="M5 5a2 2 0 00-2 2v8a2 2 0 002 2h8a2 2 0 002-2v-3a1 1 0 10-2 0v3H5V7h3a1 1 0 000-2H5z"></path>
            </svg>` : ''}
          </a>
        </div>
        <p class="constellation-detail-desc">${node.description}</p>
        <p class="constellation-detail-why">${node.why}</p>
      </div>
    `;

    const titleLink = detailsPanel.querySelector('.constellation-detail-title');
    if (titleLink && !isHttpLink) {
      titleLink.addEventListener('click', (e) => {
        e.preventDefault();
        if (node.link === '#agents-section') {
          const section = document.getElementById('agents-section');
          if (section) {
            section.scrollIntoView({ behavior: 'auto' });
          }
        }
      });
    }
  }

  function resetDetailsPanel() {
    detailsPanel.innerHTML = `
      <div class="constellation-default-state font-sans">
        <p>hover over any node in the skill constellation above to inspect the specific models, harnesses, and operating manuals governing this system.</p>
      </div>
    `;
  }

  constellationNodes.forEach(nodeEl => {
    const nodeId = nodeEl.getAttribute('data-id');
    const nodeData = constellationData[nodeId];

    nodeEl.addEventListener('mouseenter', () => {
      nodeEl.classList.add('active');

      constellationLines.forEach(line => {
        if (line.classList.contains(`line-${nodeId}`)) {
          line.classList.add('active');
        } else {
          line.classList.add('inactive');
        }
      });

      if (nodeData) {
        updateDetailsPanel(nodeData);
      }
    });

    nodeEl.addEventListener('mouseleave', () => {
      nodeEl.classList.remove('active');

      constellationLines.forEach(line => {
        line.classList.remove('active');
        line.classList.remove('inactive');
      });

      resetDetailsPanel();
    });

    nodeEl.addEventListener('click', () => {
      if (nodeId === 'agents-md') {
        openModal();
      } else if (nodeData && nodeData.link.startsWith('http')) {
        window.open(nodeData.link, '_blank', 'noopener,noreferrer');
      }
    });
  });

  // 5. CROSS-HIGHLIGHTING: CHANGELOG HOVER DYNAMIC LINKING (NO FADES)
  const changeEntries = document.querySelectorAll('.change-entry');
  
  changeEntries.forEach(entry => {
    entry.addEventListener('mouseenter', () => {
      const targetsString = entry.getAttribute('data-targets');
      if (!targetsString) return;
      
      const targets = targetsString.split(',');
      targets.forEach(targetId => {
        const stackElement = document.getElementById(targetId);
        if (stackElement) {
          if (stackElement.classList.contains('constellation-node')) {
            // Highlight node and active lines
            stackElement.classList.add('active');
            
            constellationLines.forEach(line => {
              if (line.classList.contains(`line-${targetId}`)) {
                line.classList.add('active');
              } else {
                line.classList.add('inactive');
              }
            });

            // Update details panel
            const nodeData = constellationData[targetId];
            if (nodeData) {
              updateDetailsPanel(nodeData);
            }
          } else {
            // Highlight stack entries with a subtle, sharp hacker-green indicator
            stackElement.style.borderLeft = '2px solid var(--color-accent)';
            stackElement.style.paddingLeft = '0.75rem';
            stackElement.style.marginLeft = '-0.75rem';
            
            // Flash the text color instantly
            const nameEl = stackElement.querySelector('.entry-name');
            if (nameEl) {
              nameEl.style.color = 'var(--color-accent)';
            }
          }
        }
      });
    });
    
    entry.addEventListener('mouseleave', () => {
      const targetsString = entry.getAttribute('data-targets');
      if (!targetsString) return;
      
      const targets = targetsString.split(',');
      targets.forEach(targetId => {
        const stackElement = document.getElementById(targetId);
        if (stackElement) {
          if (stackElement.classList.contains('constellation-node')) {
            // Reset node active state
            stackElement.classList.remove('active');
            
            constellationLines.forEach(line => {
              line.classList.remove('active');
              line.classList.remove('inactive');
            });

            // Reset details panel
            resetDetailsPanel();
          } else {
            // Reset styling instantly
            stackElement.style.borderLeft = '';
            stackElement.style.paddingLeft = '';
            stackElement.style.marginLeft = '';
            
            const nameEl = stackElement.querySelector('.entry-name');
            if (nameEl) {
              nameEl.style.color = '';
            }
          }
        }
      });
    });
  });
});
