document.addEventListener('DOMContentLoaded', () => {
  const rawCodeElements = [
    document.getElementById('raw-agents-code'),
    document.getElementById('dialog-raw-agents-code'),
  ].filter(Boolean);
  const rawAgentsViews = [
    document.getElementById('raw-agents-view'),
    document.getElementById('dialog-raw-agents-view'),
  ].filter(Boolean);
  const renderedAgentsViews = [
    document.getElementById('rendered-agents-view'),
    document.getElementById('dialog-rendered-agents-view'),
  ].filter(Boolean);
  const lineNumbersContainers = [
    document.getElementById('editor-line-numbers'),
    document.getElementById('dialog-editor-line-numbers'),
  ].filter(Boolean);
  const agentsViewButtons = document.querySelectorAll('.editor-view-toggle [data-view]');
  const copyAgentsInlineBtn = document.getElementById('copy-agents-inline-btn');
  const copyAgentsDialogBtn = document.getElementById('copy-agents-dialog-btn');
  const agentsInlineOpenTarget = document.getElementById('agents-inline-open-target');
  const closeAgentsDialogBtn = document.getElementById('close-agents-dialog-btn');
  const agentsDialog = document.getElementById('agents-dialog');
  const agentsDialogPanel = agentsDialog?.querySelector('.morph-dialog-panel');
  const agentsDialogBackdrop = agentsDialog?.querySelector('[data-close-agents-dialog]');
  const agentsMorphSource = document.querySelector('#agents-md .editor-pane');
  const skillDialog = document.getElementById('skill-dialog');
  const skillDialogBackdrop = skillDialog?.querySelector('[data-close-skill-dialog]');
  const closeSkillDialogBtn = document.getElementById('close-skill-dialog-btn');
  const skillDialogLabel = document.getElementById('skill-dialog-label');
  const skillDialogTitle = document.getElementById('skill-dialog-title');
  const skillViewButtons = document.querySelectorAll('[data-skill-view]');
  const skillRawView = document.getElementById('skill-raw-view');
  const skillRawCode = document.getElementById('skill-raw-code');
  const skillRenderedView = document.getElementById('skill-rendered-view');
  const copySkillBtn = document.getElementById('copy-skill-btn');
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const skillContentPaths = {
    'grill-with-docs': 'skills/grill-with-docs.md',
    'grill-me': 'skills/grill-me.md',
    'compact-handoff': 'skills/compact-handoff.md',
    'repository-test-design': 'skills/repository-test-design.md',
    'optimo': 'skills/optimo.md',
    'naming': 'skills/naming.md',
    'thermo-nuclear-code-quality-review': 'skills/thermo-nuclear-code-quality-review.md',
    'mermaid-diagrams': 'skills/mermaid-diagrams.md',
    'language-selection': 'skills/language-selection.md',
    'create-cli': 'skills/create-cli.md',
  };
  const skillContentCache = new Map();
  
  let agentsMarkdownContent = '';
  let activeAgentsView = 'raw';
  let activeSkillView = 'raw';
  let activeSkillContent = '';
  let isAgentsDialogOpen = false;
  let isSkillDialogOpen = false;
  let lastSkillTrigger = null;

  const faviconLink = document.getElementById('dynamic-favicon');
  if (faviconLink) {
    const faviconFrames = ['/favicon-a.png', '/favicon-i.png'];
    const setFaviconFrame = () => {
      const faviconFrameIndex = Math.floor(Date.now() / 700) % faviconFrames.length;
      faviconLink.setAttribute('href', `${faviconFrames[faviconFrameIndex]}?v=${faviconFrameIndex}`);
      faviconLink.setAttribute('type', 'image/png');
    };

    setFaviconFrame();
    window.setInterval(setFaviconFrame, 250);
  }

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
      
      rawCodeElements.forEach(element => {
        element.innerHTML = escapedText;
      });
      renderedAgentsViews.forEach(element => {
        element.innerHTML = renderMarkdown(text);
      });
      
      // Generate IDE line numbers
      const lines = text.endsWith('\n') ? text.split('\n').slice(0, -1) : text.split('\n');
      let lineNumsHtml = '';
      for (let i = 1; i <= lines.length; i++) {
        lineNumsHtml += `<div>${i}</div>`;
      }
      lineNumbersContainers.forEach(container => {
        container.innerHTML = lineNumsHtml;
      });
      setAgentsView(activeAgentsView);
      syncAgentsLineNumbers();
    })
    .catch(error => {
      console.error(error);
      rawCodeElements.forEach(element => {
        element.textContent = 'Failed to load AGENTS.md. Ensure the file is present in the workspace root.';
      });
      renderedAgentsViews.forEach(element => {
        element.innerHTML = '<p>Failed to load AGENTS.md. Ensure the file is present in the workspace root.</p>';
      });
    });

  // 2. LIGHTWEIGHT MARKDOWN TO HTML RENDERER
  function renderMarkdown(md) {
    if (!md) return '<p>No content available.</p>';

    const escapeHtml = value => value
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');

    const renderInline = value => escapeHtml(value)
      .replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>')
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      .replace(/\*([^*]+)\*/g, '<em>$1</em>')
      .replace(/\[REDACTED\]/g, '<span class="redacted-text">[REDACTED]</span>')
      .replace(/█{3,}/g, match => `<span class="redacted-block">${match}</span>`)
      .replace(/\n/g, '<br>');

    const lines = md.replace(/\r\n/g, '\n').split('\n');
    const blocks = [];
    let index = 0;

    const collectParagraph = () => {
      const paragraph = [];
      while (index < lines.length && lines[index].trim() !== '') {
        if (/^(#{1,6})\s+/.test(lines[index]) || /^```/.test(lines[index]) || /^---\s*$/.test(lines[index]) || /^\s*([-*]|\d+\.)\s+/.test(lines[index]) || /^\s*>/.test(lines[index])) {
          break;
        }
        paragraph.push(lines[index]);
        index += 1;
      }
      return paragraph.join('\n');
    };

    while (index < lines.length) {
      const line = lines[index];
      const trimmed = line.trim();

      if (!trimmed) {
        index += 1;
        continue;
      }

      const fenceMatch = trimmed.match(/^```(\w+)?/);
      if (fenceMatch) {
        const language = fenceMatch[1] || 'text';
        index += 1;
        const codeLines = [];
        while (index < lines.length && !/^```/.test(lines[index].trim())) {
          codeLines.push(lines[index]);
          index += 1;
        }
        index += 1;
        blocks.push(`<pre><code class="language-${language}">${escapeHtml(codeLines.join('\n'))}</code></pre>`);
        continue;
      }

      const headingMatch = trimmed.match(/^(#{1,6})\s+(.+)$/);
      if (headingMatch) {
        const level = Math.min(3, headingMatch[1].length);
        blocks.push(`<h${level}>${renderInline(headingMatch[2])}</h${level}>`);
        index += 1;
        continue;
      }

      if (/^---\s*$/.test(trimmed)) {
        blocks.push('<hr>');
        index += 1;
        continue;
      }

      if (/^\s*>/.test(line)) {
        const quoteLines = [];
        while (index < lines.length && /^\s*>/.test(lines[index])) {
          quoteLines.push(lines[index].replace(/^\s*>\s?/, ''));
          index += 1;
        }
        const alertMatch = quoteLines[0]?.match(/^\[!(IMPORTANT|NOTE|WARNING|TIP|CAUTION)\]/);
        if (alertMatch) {
          const content = quoteLines.slice(1).join('\n');
          blocks.push(`<div class="gh-alert alert-${alertMatch[1].toLowerCase()}"><strong>[${alertMatch[1]}]</strong><br>${renderInline(content)}</div>`);
        } else {
          blocks.push(`<blockquote>${renderInline(quoteLines.join('\n'))}</blockquote>`);
        }
        continue;
      }

      if (/^\s*[-*]\s+/.test(line) || /^\s*\d+\.\s+/.test(line)) {
        const ordered = /^\s*\d+\.\s+/.test(line);
        const items = [];
        const itemPattern = ordered ? /^\s*\d+\.\s+(.+)$/ : /^\s*[-*]\s+(.+)$/;
        while (index < lines.length && itemPattern.test(lines[index])) {
          items.push(lines[index].replace(itemPattern, '$1'));
          index += 1;
        }
        const tag = ordered ? 'ol' : 'ul';
        blocks.push(`<${tag}>${items.map(item => `<li>${renderInline(item)}</li>`).join('')}</${tag}>`);
        continue;
      }

      if (/^\|.+\|$/.test(trimmed) && index + 1 < lines.length && /^\|?[\s:-]+\|[\s|:-]+$/.test(lines[index + 1].trim())) {
        const headerCells = trimmed.slice(1, -1).split('|').map(cell => cell.trim());
        index += 2;
        const rows = [];
        while (index < lines.length && /^\|.+\|$/.test(lines[index].trim())) {
          rows.push(lines[index].trim().slice(1, -1).split('|').map(cell => cell.trim()));
          index += 1;
        }
        blocks.push(`<table><thead><tr>${headerCells.map(cell => `<th>${renderInline(cell)}</th>`).join('')}</tr></thead><tbody>${rows.map(row => `<tr>${row.map(cell => `<td>${renderInline(cell)}</td>`).join('')}</tr>`).join('')}</tbody></table>`);
        continue;
      }

      const paragraph = collectParagraph();
      if (paragraph) {
        blocks.push(`<p>${renderInline(paragraph)}</p>`);
      }
    }

    return blocks.join('\n');
  }

  function setAgentsView(view) {
    if (activeAgentsView === view && rawAgentsViews.length > 0) {
      updateAgentsViewButtons(view);
      return;
    }

    const previousView = activeAgentsView;
    activeAgentsView = view;
    const isRendered = view === 'rendered';

    updateAgentsViewButtons(view);

    const previousPanels = previousView === 'rendered' ? renderedAgentsViews : rawAgentsViews;
    const nextPanels = isRendered ? renderedAgentsViews : rawAgentsViews;

    lineNumbersContainers.forEach(container => {
      container.hidden = isRendered;
    });

    if (prefersReducedMotion || previousView === view) {
      renderedAgentsViews.forEach(panel => {
        panel.hidden = !isRendered;
      });
      rawAgentsViews.forEach(panel => {
        panel.hidden = isRendered;
      });
      return;
    }

    previousPanels.forEach(panel => {
      panel.classList.remove('is-entering');
      panel.classList.add('view-panel', 'is-exiting');
      window.setTimeout(() => {
        panel.hidden = true;
        panel.classList.remove('is-exiting');
      }, 170);
    });

    nextPanels.forEach(panel => {
      panel.hidden = false;
      panel.classList.remove('is-exiting');
      panel.classList.add('view-panel', 'is-entering');
      window.setTimeout(() => {
        panel.classList.remove('is-entering');
      }, 230);
    });

    syncAgentsLineNumbers();
  }

  function syncAgentsLineNumbers() {
    [
      ['raw-agents-view', 'editor-line-numbers'],
      ['dialog-raw-agents-view', 'dialog-editor-line-numbers'],
    ].forEach(([codeId, lineNumbersId]) => {
      const code = document.getElementById(codeId);
      const lineNumbers = document.getElementById(lineNumbersId);
      if (!code || !lineNumbers) return;
      lineNumbers.scrollTop = code.scrollTop;
    });
  }

  [
    ['raw-agents-view', 'editor-line-numbers'],
    ['dialog-raw-agents-view', 'dialog-editor-line-numbers'],
  ].forEach(([codeId, lineNumbersId]) => {
    const code = document.getElementById(codeId);
    const lineNumbers = document.getElementById(lineNumbersId);
    if (!code || !lineNumbers) return;

    code.addEventListener('scroll', () => {
      lineNumbers.scrollTop = code.scrollTop;
    }, { passive: true });
  });

  function updateAgentsViewButtons(view) {
    agentsViewButtons.forEach(button => {
      const isActive = button.getAttribute('data-view') === view;
      button.classList.toggle('is-active', isActive);
      button.setAttribute('aria-selected', String(isActive));
    });
  }

  async function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return;
    }

    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.setAttribute('readonly', '');
    textarea.style.position = 'fixed';
    textarea.style.top = '-9999px';
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    textarea.remove();
  }

  // 3. INLINE AGENTS.MD VIEW TOGGLE
  agentsViewButtons.forEach(button => {
    button.addEventListener('click', () => {
      setAgentsView(button.getAttribute('data-view'));
    });
  });

  function setCopiedState(button, copiedLabel = 'Copied AGENTS.md', defaultLabel = 'Copy AGENTS.md') {
    button.setAttribute('aria-label', copiedLabel);
    button.classList.add('is-copied');

    window.setTimeout(() => {
      button.setAttribute('aria-label', defaultLabel);
      button.classList.remove('is-copied');
    }, 1600);
  }

  async function handleCopyAgents(button) {
    try {
      await copyText(agentsMarkdownContent);
    } catch (error) {
      console.warn('Clipboard copy failed', error);
    }
    setCopiedState(button);
  }

  copyAgentsInlineBtn?.addEventListener('click', () => handleCopyAgents(copyAgentsInlineBtn));
  copyAgentsDialogBtn?.addEventListener('click', () => handleCopyAgents(copyAgentsDialogBtn));

  skillViewButtons.forEach(button => {
    button.addEventListener('click', () => {
      setSkillView(button.getAttribute('data-skill-view'));
    });
  });

  copySkillBtn?.addEventListener('click', async () => {
    try {
      await copyText(activeSkillContent);
    } catch (error) {
      console.warn('Clipboard copy failed', error);
    }
    setCopiedState(copySkillBtn, 'Copied SKILL.md', 'Copy SKILL.md');
  });

  function getDialogTargetRect() {
    const margin = window.innerWidth <= 768 ? 12 : 32;
    const width = Math.min(920, window.innerWidth - margin * 2);
    const height = Math.min(720, window.innerHeight - margin * 2);
    return {
      left: (window.innerWidth - width) / 2,
      top: (window.innerHeight - height) / 2,
      width,
      height,
    };
  }

  function getSourceToTargetTransform(sourceRect, targetRect) {
    return {
      x: sourceRect.left - targetRect.left,
      y: sourceRect.top - targetRect.top,
      scaleX: sourceRect.width / targetRect.width,
      scaleY: sourceRect.height / targetRect.height,
    };
  }

  function setDialogPanelRect(rect) {
    agentsDialogPanel.style.width = `${rect.width}px`;
    agentsDialogPanel.style.height = `${rect.height}px`;
    agentsDialogPanel.style.left = `${rect.left}px`;
    agentsDialogPanel.style.top = `${rect.top}px`;
    agentsDialogPanel.style.position = 'fixed';
  }

  function animateDialogMorph(sourceRect, direction) {
    if (!agentsDialogPanel || prefersReducedMotion) return Promise.resolve();

    const targetRect = getDialogTargetRect();
    setDialogPanelRect(targetRect);

    if (direction === 'close') {
      const animation = agentsDialogPanel.animate(
        [
          { transform: 'translate(0, 0) scale(1)', opacity: 1, filter: 'blur(0)' },
          { transform: 'translateY(-0.5rem) scale(0.992)', opacity: 0, filter: 'blur(4px)' },
        ],
        {
          duration: 180,
          easing: 'cubic-bezier(0.4, 0, 1, 1)',
          fill: 'both',
        },
      );

      return animation.finished.catch(() => {});
    }

    const transform = getSourceToTargetTransform(sourceRect, targetRect);
    const from = `translate(${transform.x}px, ${transform.y}px) scale(${transform.scaleX}, ${transform.scaleY})`;
    const to = 'translate(0, 0) scale(1)';

    const animation = agentsDialogPanel.animate(
      [
        { transform: from, opacity: 0.82 },
        { transform: to, opacity: 1 },
      ],
      {
        duration: 420,
        easing: 'cubic-bezier(0.22, 1, 0.36, 1)',
        fill: 'both',
      },
    );

    return animation.finished.catch(() => {});
  }

  async function openAgentsDialog() {
    if (!agentsDialog || !agentsDialogPanel || !agentsMorphSource || isAgentsDialogOpen) return;

    isAgentsDialogOpen = true;
    const sourceRect = agentsMorphSource.getBoundingClientRect();
    agentsDialog.hidden = false;
    agentsDialog.setAttribute('aria-hidden', 'false');
    document.body.classList.add('is-dialog-open');
    agentsDialog.classList.add('is-open');
    setAgentsView(activeAgentsView);
    await animateDialogMorph(sourceRect, 'open');
    closeAgentsDialogBtn?.focus({ preventScroll: true });
  }

  async function closeAgentsDialog() {
    if (!agentsDialog || !agentsDialogPanel || !agentsMorphSource || !isAgentsDialogOpen) return;

    isAgentsDialogOpen = false;
    const sourceRect = agentsMorphSource.getBoundingClientRect();
    agentsDialog.classList.remove('is-open');
    await animateDialogMorph(sourceRect, 'close');
    agentsDialog.hidden = true;
    agentsDialog.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('is-dialog-open');
    agentsDialogPanel.getAnimations().forEach(animation => animation.cancel());
    agentsInlineOpenTarget?.focus({ preventScroll: true });
  }

  agentsInlineOpenTarget?.addEventListener('click', openAgentsDialog);
  agentsInlineOpenTarget?.addEventListener('keydown', event => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      openAgentsDialog();
    }
  });
  closeAgentsDialogBtn?.addEventListener('click', closeAgentsDialog);
  agentsDialogBackdrop?.addEventListener('click', closeAgentsDialog);

  window.addEventListener('keydown', event => {
    if (event.key === 'Escape' && isAgentsDialogOpen) {
      closeAgentsDialog();
    }
    if (event.key === 'Escape' && isSkillDialogOpen) {
      closeSkillDialog();
    }
  });

  window.addEventListener('resize', () => {
    if (!isAgentsDialogOpen || !agentsDialogPanel) return;
    setDialogPanelRect(getDialogTargetRect());
  });

  document.querySelectorAll('.entry-title-link').forEach(link => {
    if (link.querySelector('.link-icon')) return;

    const icon = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    icon.classList.add('link-icon');
    icon.setAttribute('aria-hidden', 'true');
    link.append(icon);
  });

  document.querySelectorAll('.link-icon').forEach(icon => {
    icon.setAttribute('fill', 'none');
    icon.setAttribute('viewBox', '0 0 10 10');
    icon.innerHTML = `
      <path
        d="M1.004 9.166 9.337.833m0 0v8.333m0-8.333H1.004"
        stroke="currentColor"
        stroke-width="1.25"
        stroke-linecap="round"
        stroke-linejoin="round"
      ></path>
    `;
  });

  function setupRoleFlips() {
    document.querySelectorAll('.role-column').forEach(column => {
      const role = column.querySelector('.role-label')?.textContent?.trim();
      const entryName = column.querySelector('.entry-name');
      if (!role || !entryName || entryName.dataset.flipReady === 'true') return;

      const original = entryName.textContent.trim();
      entryName.dataset.flipReady = 'true';
      entryName.setAttribute('aria-label', original);

      const parentLink = entryName.closest('a');
      if (parentLink && !parentLink.getAttribute('aria-label')) {
        parentLink.setAttribute('aria-label', `${original}, ${role}`);
      }

      entryName.textContent = '';
      entryName.classList.add('text-3d-flip');
      entryName.style.setProperty('--flip-width', `${Math.max(original.length, role.length) * 0.62}em`);

      const front = document.createElement('span');
      front.className = 'text-3d-flip-inner text-3d-flip-front';
      front.setAttribute('aria-hidden', 'true');
      front.textContent = original;

      const back = document.createElement('span');
      back.className = 'text-3d-flip-inner text-3d-flip-back';
      back.setAttribute('aria-hidden', 'true');
      back.textContent = role;

      entryName.append(front, back);
    });
  }

  function setupSkillDialog() {
    document.querySelectorAll('.skill-item').forEach(item => {
      item.setAttribute('role', 'button');
      item.setAttribute('tabindex', '0');

      const open = async () => {
        if (!skillDialog || !skillDialogLabel || !skillDialogTitle || !skillRawView || !skillRawCode || !skillRenderedView) return;

        lastSkillTrigger = item;
        const title = item.querySelector('.skill-name')?.textContent?.trim() || 'Skill';
        const label = item.querySelector('.skill-label')?.textContent?.trim() || 'Skill';
        const fallback = item.querySelector('.skill-detail')?.textContent?.replace(/^[\s-]+/, '').trim() || '';

        skillDialogLabel.textContent = label;
        skillDialogTitle.textContent = title;
        activeSkillContent = '';
        skillRawCode.textContent = 'Loading SKILL.md...';
        skillRenderedView.innerHTML = '<p>Loading SKILL.md...</p>';
        setSkillView('raw');
        isSkillDialogOpen = true;
        skillDialog.hidden = false;
        skillDialog.setAttribute('aria-hidden', 'false');
        skillDialog.classList.add('is-open');
        document.body.classList.add('is-dialog-open');
        closeSkillDialogBtn?.focus({ preventScroll: true });

        try {
          const detail = await loadSkillContent(item.id);
          if (lastSkillTrigger === item && isSkillDialogOpen) {
            activeSkillContent = detail;
            skillRawCode.textContent = detail;
            skillRenderedView.innerHTML = renderMarkdown(getRenderableSkillMarkdown(detail));
            skillRawView.scrollTop = 0;
            skillRawView.scrollLeft = 0;
            skillRenderedView.scrollTop = 0;
          }
        } catch (error) {
          console.warn('Failed to load skill content', error);
          activeSkillContent = fallback || 'Failed to load SKILL.md.';
          skillRawCode.textContent = activeSkillContent;
          skillRenderedView.innerHTML = renderMarkdown(activeSkillContent);
        }
      };

      item.addEventListener('click', open);
      item.addEventListener('keydown', event => {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          open();
        }
      });
    });
  }

  function setSkillView(view) {
    activeSkillView = view === 'rendered' ? 'rendered' : 'raw';
    const isRendered = activeSkillView === 'rendered';

    skillViewButtons.forEach(button => {
      const isActive = button.getAttribute('data-skill-view') === activeSkillView;
      button.classList.toggle('is-active', isActive);
      button.setAttribute('aria-selected', String(isActive));
    });

    if (skillRawView) {
      skillRawView.hidden = isRendered;
    }
    if (skillRenderedView) {
      skillRenderedView.hidden = !isRendered;
    }
  }

  async function loadSkillContent(skillId) {
    if (skillContentCache.has(skillId)) {
      return skillContentCache.get(skillId);
    }

    const path = skillContentPaths[skillId];
    if (!path) {
      throw new Error(`No skill content path for ${skillId}`);
    }

    const response = await fetch(path);
    if (!response.ok) {
      throw new Error(`Failed to fetch ${path}`);
    }

    const text = await response.text();
    skillContentCache.set(skillId, text);
    return text;
  }

  function getRenderableSkillMarkdown(markdown) {
    return markdown.replace(/^---\n[\s\S]*?\n---\n?/, '').trim();
  }

  function closeSkillDialog() {
    if (!skillDialog || !isSkillDialogOpen) return;

    isSkillDialogOpen = false;
    skillDialog.classList.remove('is-open');
    skillDialog.hidden = true;
    skillDialog.setAttribute('aria-hidden', 'true');
    if (!isAgentsDialogOpen) {
      document.body.classList.remove('is-dialog-open');
    }
    lastSkillTrigger?.focus({ preventScroll: true });
  }

  closeSkillDialogBtn?.addEventListener('click', closeSkillDialog);
  skillDialogBackdrop?.addEventListener('click', closeSkillDialog);

  function revealElement(element, delay = 0) {
    if (!element || element.dataset.revealReady === 'true') return;
    element.dataset.revealReady = 'true';
    element.classList.add('component-reveal');
    element.style.setProperty('--component-delay', `${delay}ms`);
  }

  function preserveAccessibleLabel(element) {
    const text = element.textContent;
    if (!text) return;
    const parentLink = element.closest('a');
    if (parentLink && !parentLink.getAttribute('aria-label')) {
      parentLink.setAttribute('aria-label', text);
    }
  }

  function splitTextEffect(element, mode, delay = 0) {
    const text = element.textContent;
    if (!text || element.dataset.textEffectReady === 'true') return;

    element.dataset.textEffectReady = 'true';
    preserveAccessibleLabel(element);
    element.setAttribute('aria-label', text);
    element.classList.add('text-effect-root', `text-effect-${mode}`);
    element.style.setProperty('--effect-delay', `${delay}ms`);

    const parts = mode === 'char'
      ? Array.from(text)
      : text.match(/\S+|\s+/g) || [];

    element.textContent = '';
    let effectIndex = 0;

    parts.forEach(part => {
      if (!part) return;

      if (/^\s+$/.test(part)) {
        element.appendChild(document.createTextNode(part));
        return;
      }

      const span = document.createElement('span');
      span.textContent = part;
      span.setAttribute('aria-hidden', 'true');
      span.className = `text-effect-unit ${mode === 'char' ? 'text-effect-letter' : 'text-effect-word'}`;
      span.style.setProperty('--effect-index', String(effectIndex));
      effectIndex += 1;
      element.appendChild(span);
    });
  }

  function setupTextEffects() {
    if (prefersReducedMotion) return;

    const getPositionedElements = selector => {
      return Array.from(document.querySelectorAll(selector))
        .filter(element => element instanceof HTMLElement)
        .map(element => {
          const rect = element.getBoundingClientRect();
          return {
            element,
            top: Math.round(rect.top / 28) * 28,
            left: rect.left,
          };
        })
        .sort((a, b) => a.top - b.top || a.left - b.left)
        .map(item => item.element);
    };

    const getPhaseDelay = (index, total, baseDelay, maxDuration) => {
      if (total <= 1) return baseDelay;

      return Math.round(baseDelay + (index / (total - 1)) * maxDuration);
    };

    const applyPageWideBodySweep = (elements, baseDelay) => {
      const viewportWidth = Math.max(window.innerWidth, 1);
      const sweepDuration = 130;

      elements.forEach(element => {
        element.querySelectorAll('.text-effect-unit').forEach(unit => {
          const rect = unit.getBoundingClientRect();
          const pageX = Math.max(0, Math.min(1, rect.left / viewportWidth));
          const delay = Math.round(baseDelay + pageX * sweepDuration);
          unit.style.setProperty('--effect-delay', `${delay}ms`);
          unit.style.setProperty('--effect-index', '0');
        });
      });
    };

    const componentElements = getPositionedElements('.change-group, .stack-section, .agents-box-container');
    componentElements.forEach((element, index) => {
      revealElement(element, Math.min(index * 4, 64));
    });

    const bigTitleElements = getPositionedElements('.column-title, .section-heading');
    bigTitleElements.forEach((element, index) => {
      const mode = element.classList.contains('column-title') ? 'char' : 'word-mode';
      splitTextEffect(element, mode, getPhaseDelay(index, bigTitleElements.length, 70, 160));
    });

    const smallTitleBaseDelay = 260;
    const smallTitleElements = getPositionedElements('.skill-label, .skill-name, .change-date, .change-title');

    smallTitleElements.forEach((element, index) => {
      const mode = element.matches('.skill-label') ? 'preset' : 'custom';
      splitTextEffect(element, mode, getPhaseDelay(index, smallTitleElements.length, smallTitleBaseDelay, 210));
    });

    const bodyBaseDelay = 500;

    const bodyElements = getPositionedElements('.entry-description, .change-description, .skill-detail, .entry-metadata');
    bodyElements.forEach(element => {
      splitTextEffect(element, 'body', bodyBaseDelay);
    });
    applyPageWideBodySweep(bodyElements, bodyBaseDelay);
  }

  function startFontDependentUi() {
    document.body.classList.remove('fonts-loading');
    document.body.classList.add('fonts-ready');
    setupRoleFlips();
    setupSkillDialog();
    setupTextEffects();
  }

  function waitForCriticalFonts() {
    if (!document.fonts?.load) {
      return Promise.resolve();
    }

    const criticalFontLoads = [
      '400 1rem helveticaNeue',
      '600 1rem helveticaNeue',
      '700 1rem helveticaNeue',
      '400 1rem "Commit Mono"',
    ];

    return Promise.all(criticalFontLoads.map(font => document.fonts.load(font)))
      .then(() => document.fonts.ready);
  }

  if (document.fonts?.ready) {
    waitForCriticalFonts().then(startFontDependentUi).catch(startFontDependentUi);
  } else {
    startFontDependentUi();
  }

  document.addEventListener('animationend', event => {
    const target = event.target;
    if (!(target instanceof HTMLElement)) return;

    if (target.classList.contains('text-effect-unit') || target.classList.contains('component-reveal')) {
      target.classList.add('is-revealed');
    }
  });

  // 4. CROSS-HIGHLIGHTING: CHANGELOG HOVER DYNAMIC LINKING
  const changeEntries = document.querySelectorAll('.change-entry');
  
  changeEntries.forEach(entry => {
    entry.addEventListener('mouseenter', () => {
      const targetsString = entry.getAttribute('data-targets');
      if (!targetsString) return;
      
      const targets = targetsString.split(',').map(target => target.trim()).filter(Boolean);
      targets.forEach(targetId => {
        const stackElement = document.getElementById(targetId);
        if (stackElement) {
          stackElement.classList.add('is-linked-target');
        }
      });
    });
    
    entry.addEventListener('mouseleave', () => {
      const targetsString = entry.getAttribute('data-targets');
      if (!targetsString) return;
      
      const targets = targetsString.split(',').map(target => target.trim()).filter(Boolean);
      targets.forEach(targetId => {
        const stackElement = document.getElementById(targetId);
        if (stackElement) {
          stackElement.classList.remove('is-linked-target');
        }
      });
    });
  });
});
