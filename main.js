document.addEventListener('DOMContentLoaded', () => {
  const agentsMarkdownPath = '/agents/AGENTS.md';
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
  const skillDialog = document.getElementById('skill-dialog');
  const skillDialogPanel = skillDialog?.querySelector('.skill-dialog-panel');
  const skillDialogBackdrop = skillDialog?.querySelector('[data-close-skill-dialog]');
  const closeSkillDialogBtn = document.getElementById('close-skill-dialog-btn');
  const skillDialogLabel = document.getElementById('skill-dialog-label');
  const skillDialogTitle = document.getElementById('skill-dialog-title');
  const skillViewButtons = document.querySelectorAll('[data-skill-view]');
  const skillRawView = document.getElementById('skill-raw-view');
  const skillRawCode = document.getElementById('skill-raw-code');
  const skillRenderedView = document.getElementById('skill-rendered-view');
  const skillGithubLink = document.getElementById('skill-github-link');
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const skillContentPaths = {    'crabbox': 'skills/crabbox/SKILL.md',
    'grill-with-docs': 'skills/grill-with-docs/SKILL.md',
    'grill-me': 'skills/grill-me/SKILL.md',
    'compact-handoff': 'skills/compact-handoff/SKILL.md',
    'repository-test-design': 'skills/repository-test-design/SKILL.md',
    'optimo': 'skills/optimo/SKILL.md',
    'naming': 'skills/naming.md',
    'thermo-nuclear-code-quality-review': 'skills/thermo-nuclear-code-quality-review/SKILL.md',
    'mermaid-diagrams': 'skills/mermaid-diagrams/SKILL.md',
    'language-selection': 'skills/language-selection/SKILL.md',
    'create-cli': 'skills/create-cli/SKILL.md',
    'animated-favicons': 'skills/animated-favicons/SKILL.md',
    'grill-with-facts': 'skills/grill-with-facts/SKILL.md',
    'make-interfaces-feel-better': 'skills/make-interfaces-feel-better/SKILL.md',
    'oracle': 'skills/oracle/SKILL.md',
    'quality-code': 'skills/quality-code/SKILL.md',
    'review-animations': 'skills/review-animations/SKILL.md',
    'write-better-error-messages': 'skills/write-better-error-messages/SKILL.md',
    'codebase-memory-mcp-skill': 'skills/codebase-memory-mcp/SKILL.md',
    'domain-modeling': 'skills/domain-modeling/SKILL.md',
    'codebase-design': 'skills/codebase-design/SKILL.md',
    'grilling': 'skills/grilling/SKILL.md',
    'idea-generator': 'skills/idea-generator/SKILL.md',
    'teach': 'skills/teach/SKILL.md',
    'transitions-dev': 'skills/transitions-dev/SKILL.md',
    'writing-great-skills': 'skills/writing-great-skills/SKILL.md',
    'dft-writing': 'skills/dft-writing/SKILL.md',
    'effect-program-design': 'skills/effect-program-design/SKILL.md',
    'animation-vocabulary': 'skills/animation-vocabulary/SKILL.md',
    'timeboxed-iterating': 'skills/timeboxed-iterating/SKILL.md',
    'find-fonts': 'skills/find-fonts/SKILL.md',
    'tmux-codex-orchestrator': 'skills/tmux-codex-orchestrator/SKILL.md',
    'transitions-polish': 'skills/transitions-polish/SKILL.md',
  };
  const skillContentCache = new Map();
  const floatingTooltip = document.createElement('div');
  floatingTooltip.className = 'floating-tooltip font-karla';
  floatingTooltip.setAttribute('role', 'tooltip');
  document.body.appendChild(floatingTooltip);
  
  let agentsMarkdownContent = '';
  let activeAgentsView = 'raw';
  let activeSkillView = 'raw';
  let isAgentsDialogOpen = false;
  let isSkillDialogOpen = false;
  let lastSkillTrigger = null;
  let activeTooltipTarget = null;
  const suppressedTooltipFocusTargets = new WeakSet();
  const snapshotStatus = document.getElementById('snapshot-status');
  const snapshotStatusLabel = document.getElementById('snapshot-status-label');
  const snapshotCurrentLink = document.getElementById('snapshot-current-link');
  const stackScrollRegion = document.querySelector('.stack-scroll-region');

  const monthNames = [
    'january',
    'february',
    'march',
    'april',
    'may',
    'june',
    'july',
    'august',
    'september',
    'october',
    'november',
    'december',
  ];

  const stackItemSelector = '.stack-entry, .skill-item, .agents-box-container';
  const snapshotCategorySections = {
    model: 'models',
    harness: 'harnesses',
    hook: 'hooks',
    mcp: 'mcps',
    cli: 'cli-tools',
    skill: 'skills',
    workspace: 'workspace',
  };
  let snapshotRecords = null;

  function parseDisplayDate(displayDate) {
    const [day, month, year] = displayDate.split('/').map(part => Number(part));
    return { day, month, year };
  }

  function getDateValue(displayDate) {
    const { day, month, year } = parseDisplayDate(displayDate);
    return year * 10000 + month * 100 + day;
  }

  function getSnapshotSlug(displayDate) {
    const { day, month, year } = parseDisplayDate(displayDate);
    return `${monthNames[month - 1]}-${day}-${year}`;
  }

  function getSnapshotTitle(displayDate) {
    const { day, month, year } = parseDisplayDate(displayDate);
    const monthLabel = monthNames[month - 1];
    return `${monthLabel.charAt(0).toUpperCase()}${monthLabel.slice(1)} ${day}, ${year}`;
  }

  function getSnapshotDateFromPath() {
    const pathParts = window.location.pathname.split('/').filter(Boolean);
    const slug = pathParts[0] === 'ai' ? pathParts[1] : pathParts[0];
    if (!slug) return null;

    const match = slug.match(/^([a-z]+)-(\d{1,2})-(\d{4})$/i);
    if (!match) return null;

    const month = monthNames.indexOf(match[1].toLowerCase()) + 1;
    const day = Number(match[2]);
    const year = Number(match[3]);
    if (!month || !day || !year) return null;

    return `${String(day).padStart(2, '0')}/${String(month).padStart(2, '0')}/${year}`;
  }

  function getSnapshotCategory(title) {
    if (/\bModels?\b/i.test(title)) return 'model';
    if (/\bHarness(?:es)?\b/i.test(title)) return 'harness';
    if (/\bHooks?\b/i.test(title)) return 'hook';
    if (/\bMCPs?\b/i.test(title)) return 'mcp';
    if (/\bCLI\b/i.test(title)) return 'cli';
    if (/\bSkills?\b/i.test(title)) return 'skill';
    if (/\bWorkspace\b/i.test(title)) return 'workspace';
    return null;
  }

  function normalizeSnapshotName(value) {
    return value
      .toLowerCase()
      .replace(/\b(model|harness|hook|mcp|cli|skill|workspace)s?\b/g, '')
      .replace(/[^a-z0-9]+/g, '');
  }

  function getSnapshotEntryName(element) {
    return element.querySelector('.entry-name, .skill-name')?.textContent?.trim()
      || (element.id === 'agents-md' ? 'AGENTS.md' : element.id);
  }

  function getSnapshotEvents() {
    const events = [];

    document.querySelectorAll('.change-group').forEach(group => {
      const date = group.getAttribute('data-group');
      if (!date) return;

      group.querySelectorAll('.change-entry').forEach(entry => {
        const title = entry.querySelector('.change-title')?.textContent?.trim() || '';
        const targets = (entry.getAttribute('data-targets') || '')
          .split(',')
          .map(target => target.trim())
          .filter(Boolean);

        targets.forEach(target => {
          events.push({
            action: title.split(' ')[0],
            category: getSnapshotCategory(title),
            date,
            dateValue: getDateValue(date),
            target,
            title,
          });
        });
      });
    });

    return events.sort((a, b) => a.dateValue - b.dateValue);
  }

  function getHistoricalEntryName(event) {
    const actionPattern = /^(Added|Removed|Modified|Updated)\s+/;
    const categoryPattern = /\s+(Model|Harness|Hook|MCP|CLI|Skill|Workspace)s?(?:\s+.*)?$/i;
    const fromTitle = event.title.replace(actionPattern, '').replace(categoryPattern, '').trim();

    if (fromTitle && !fromTitle.includes(',')) return fromTitle;

    return event.target
      .replace(/-(model|harness|hook|mcp|cli|skill|workspace)$/i, '')
      .split('-')
      .map(part => part.toUpperCase() === 'mcp' || part.toUpperCase() === 'cli'
        ? part.toUpperCase()
        : `${part.charAt(0).toUpperCase()}${part.slice(1)}`)
      .join(' ');
  }

  function getSnapshotContainer(category, name) {
    const sectionId = snapshotCategorySections[category];
    const section = sectionId ? document.getElementById(sectionId) : null;
    if (!section) return null;

    if (category === 'model' || category === 'harness') {
      const roleColumns = section.querySelectorAll('.role-column');
      const isPrimaryModel = category === 'model' && /GPT 5\.5/i.test(name);
      return roleColumns[isPrimaryModel ? 0 : Math.min(1, roleColumns.length - 1)] || null;
    }

    return section.querySelector('.skills-inline-list, .two-column-list, .simple-list');
  }

  function createHistoricalSnapshotRecord(event, recordsByTarget) {
    if (!event.category) return null;
    if (event.target === snapshotCategorySections[event.category]) return null;

    const name = getHistoricalEntryName(event);
    const container = getSnapshotContainer(event.category, name);
    if (!container) return null;

    const element = document.createElement('div');
    element.id = `snapshot-history-${event.target}`;
    element.className = event.category === 'skill'
      ? 'skill-item snapshot-historical-entry snapshot-hidden'
      : 'stack-entry snapshot-historical-entry snapshot-hidden';
    element.dataset.snapshotGenerated = 'true';

    const nameClass = event.category === 'skill' ? 'skill-name' : 'entry-name';
    element.innerHTML = `<div class="entry-header"><span class="${nameClass}">${name}</span></div>`;
    container.append(element);

    const record = {
      category: event.category,
      element,
      end: null,
      generated: true,
      name,
      start: null,
      target: event.target,
    };
    recordsByTarget.set(event.target, record);
    return record;
  }

  function buildSnapshotRecords() {
    const recordsByTarget = new Map();
    const currentRecords = [];

    document.querySelectorAll(stackItemSelector).forEach(element => {
      if (element.dataset.snapshotGenerated === 'true') return;

      const section = element.closest('.stack-section');
      const category = Object.entries(snapshotCategorySections)
        .find(([, sectionId]) => section?.id === sectionId)?.[0] || null;
      const record = {
        category,
        element,
        end: null,
        generated: false,
        name: getSnapshotEntryName(element),
        start: null,
        target: element.id,
      };
      recordsByTarget.set(element.id, record);
      currentRecords.push(record);
    });

    const findRecord = event => {
      const exact = recordsByTarget.get(event.target);
      if (exact) return exact;

      const normalizedTarget = normalizeSnapshotName(event.target);
      return currentRecords.find(record => (
        record.category === event.category
        && normalizeSnapshotName(record.name) === normalizedTarget
      )) || null;
    };

    const events = getSnapshotEvents();
    const eventDates = Array.from(new Set(events.map(event => event.dateValue)));
    events.forEach(event => {
      if (event.action !== 'Added' && event.action !== 'Removed') return;

      const existingRecord = findRecord(event) || recordsByTarget.get(event.target);
      const record = existingRecord || createHistoricalSnapshotRecord(event, recordsByTarget);
      if (!record) return;

      if (event.action === 'Added') {
        record.start = record.start === null ? event.dateValue : Math.min(record.start, event.dateValue);
      } else {
        // A removal proves the item existed immediately before this change,
        // but not that it existed for the entire timeline. When the changelog
        // has no earlier addition, expose it only from the preceding snapshot.
        if (!existingRecord && record.start === null) {
          record.start = eventDates.filter(dateValue => dateValue < event.dateValue).at(-1) ?? null;
        }
        record.end = record.end === null ? event.dateValue : Math.min(record.end, event.dateValue);
      }
    });

    events.forEach(event => {
      if (event.action === 'Replaced') {
        const replacement = findRecord(event);
        if (replacement && replacement.start === null) replacement.start = event.dateValue;

        const predecessorName = event.title.match(/^Replaced (.+?) with /)?.[1];
        if (!predecessorName) return;

        let predecessor = Array.from(recordsByTarget.values()).find(record => (
          record.category === event.category
          && normalizeSnapshotName(record.name) === normalizeSnapshotName(predecessorName)
        ));
        if (!predecessor) {
          predecessor = createHistoricalSnapshotRecord({ ...event, target: normalizeSnapshotName(predecessorName) }, recordsByTarget);
          if (predecessor) {
            predecessor.name = predecessorName;
            predecessor.element.querySelector('.entry-name').textContent = predecessorName;
          }
        }
        if (predecessor) predecessor.end = event.dateValue;
      }

      const versionUpdate = event.title.match(/^Updated (.+?) to ([\d.]+)$/i);
      if (!versionUpdate) return;

      const updatedRecord = findRecord(event);
      if (updatedRecord && updatedRecord.start === null) updatedRecord.start = event.dateValue;

      const baseName = normalizeSnapshotName(versionUpdate[1]);
      const updatedCategory = event.category || updatedRecord?.category;
      Array.from(recordsByTarget.values()).forEach(record => {
        if (record === updatedRecord || record.category !== updatedCategory) return;
        const versionSuffix = normalizeSnapshotName(record.name).slice(baseName.length);
        if (normalizeSnapshotName(record.name).startsWith(baseName) && /^\d+$/.test(versionSuffix)) {
          record.end = record.end === null ? event.dateValue : Math.min(record.end, event.dateValue);
        }
      });
    });

    return Array.from(recordsByTarget.values());
  }

  function updateEmptySnapshotContainers() {
    document.querySelectorAll('.role-column, .two-column-list, .simple-list, .skills-inline-list').forEach(container => {
      const visibleItems = Array.from(container.querySelectorAll(stackItemSelector))
        .filter(item => !item.classList.contains('snapshot-hidden'));
      container.classList.toggle('snapshot-hidden', visibleItems.length === 0);
    });

    document.querySelectorAll('.stack-section').forEach(section => {
      const visibleItems = Array.from(section.querySelectorAll(stackItemSelector))
        .filter(item => !item.classList.contains('snapshot-hidden'));
      section.classList.toggle('snapshot-hidden', visibleItems.length === 0);
    });
  }

  function applySnapshot(displayDate, { pushState = false, transition = false } = {}) {
    const commitSnapshot = () => {
      snapshotRecords ||= buildSnapshotRecords();
      const snapshotValue = displayDate ? getDateValue(displayDate) : null;

      snapshotRecords.forEach(record => {
        const isCurrentView = snapshotValue === null;
        const existedAtSnapshot = (
          (record.start === null || record.start <= snapshotValue)
          && (record.end === null || snapshotValue < record.end)
        );
        const isVisible = isCurrentView ? !record.generated : existedAtSnapshot;
        record.element.classList.toggle('snapshot-hidden', !isVisible);
      });

      updateEmptySnapshotContainers();

      document.querySelectorAll('.change-group').forEach(group => {
        group.classList.toggle('is-active-snapshot', Boolean(displayDate && group.getAttribute('data-group') === displayDate));
      });

      if (snapshotStatus && snapshotStatusLabel) {
        snapshotStatus.hidden = !displayDate;
        if (displayDate) {
          snapshotStatusLabel.textContent = `Snapshot as of ${getSnapshotTitle(displayDate)}`;
        }
      }

      const title = displayDate ? `AI Stack - ${getSnapshotTitle(displayDate)}` : 'AI Stack';
      document.title = title;

      if (pushState) {
        const path = displayDate ? `/${getSnapshotSlug(displayDate)}` : '/';
        window.history.pushState({ snapshotDate: displayDate }, '', path);
      }

      if (transition && stackScrollRegion) {
        stackScrollRegion.scrollTop = 0;
      }
    };

    if (transition && !prefersReducedMotion && document.startViewTransition) {
      return document.startViewTransition(commitSnapshot).finished;
    }

    commitSnapshot();
    return Promise.resolve();
  }

  function setupSnapshotLinks() {
    document.querySelectorAll('.change-group').forEach(group => {
      const displayDate = group.getAttribute('data-group');
      const dateElement = group.querySelector('.change-date');
      if (!displayDate || !dateElement || dateElement.querySelector('a')) return;

      const link = document.createElement('a');
      link.className = 'change-date-link';
      link.href = `/${getSnapshotSlug(displayDate)}`;
      link.textContent = dateElement.textContent.trim();
      link.setAttribute('aria-label', `View AI stack snapshot for ${getSnapshotTitle(displayDate)}`);
      link.addEventListener('click', event => {
        event.preventDefault();
        applySnapshot(displayDate, { pushState: true, transition: true });
      });

      dateElement.textContent = '';
      dateElement.append(link);
    });

    window.addEventListener('popstate', () => {
      applySnapshot(getSnapshotDateFromPath(), { pushState: false, transition: true });
    });

    snapshotCurrentLink?.addEventListener('click', event => {
      event.preventDefault();
      applySnapshot(null, { pushState: true, transition: true });
    });

    applySnapshot(getSnapshotDateFromPath(), { pushState: false });
  }

  const faviconLink = document.getElementById('dynamic-favicon');
  if (faviconLink) {
    const faviconFrames = ['/favicon-a.png', '/favicon-i.png'];
    let faviconFrameIndex = -1;
    let faviconRevision = 0;

    const setFaviconFrame = () => {
      const previousIcon = document.getElementById('dynamic-favicon');
      const nextIcon = document.createElement('link');

      faviconRevision += 1;
      faviconFrameIndex = (faviconFrameIndex + 1) % faviconFrames.length;
      nextIcon.id = 'dynamic-favicon';
      nextIcon.rel = 'icon';
      nextIcon.type = 'image/png';
      nextIcon.href = `${faviconFrames[faviconFrameIndex]}?frame=${faviconFrameIndex}&rev=${faviconRevision}`;

      previousIcon?.remove();
      document.head.append(nextIcon);
    };

    setFaviconFrame();
    window.setInterval(setFaviconFrame, 700);
  }

  // 1. FETCH & PROCESS AGENTS.MD FOR THE CODE BOX
  fetch(agentsMarkdownPath)
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
        element.textContent = `Failed to load AGENTS.md from ${agentsMarkdownPath}.`;
      });
      renderedAgentsViews.forEach(element => {
        element.innerHTML = `<p>Failed to load AGENTS.md from <code>${agentsMarkdownPath}</code>.</p>`;
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
    activeAgentsView = view;
    const isRendered = view === 'rendered';

    updateAgentsViewButtons(view);

    lineNumbersContainers.forEach(container => {
      container.hidden = isRendered;
    });

    renderedAgentsViews.forEach(panel => {
      panel.hidden = !isRendered;
    });
    rawAgentsViews.forEach(panel => {
      panel.hidden = isRendered;
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

  const copiedStateTimers = new WeakMap();

  function positionFloatingTooltip(target) {
    const label = target.getAttribute('data-tooltip');
    if (!label) return;

    floatingTooltip.textContent = label;
    floatingTooltip.classList.add('is-visible');

    const targetRect = target.getBoundingClientRect();
    const tooltipRect = floatingTooltip.getBoundingClientRect();
    const viewportPadding = 12;
    const centeredLeft = targetRect.left + targetRect.width / 2;
    const left = Math.min(
      Math.max(centeredLeft, tooltipRect.width / 2 + viewportPadding),
      window.innerWidth - tooltipRect.width / 2 - viewportPadding,
    );
    const top = targetRect.bottom + tooltipRect.height + 12 > window.innerHeight
      ? targetRect.top - tooltipRect.height - 8
      : targetRect.bottom + 8;

    floatingTooltip.style.left = `${left}px`;
    floatingTooltip.style.top = `${Math.max(viewportPadding, top)}px`;
  }

  function showFloatingTooltip(target) {
    activeTooltipTarget = target;
    positionFloatingTooltip(target);
  }

  function hideFloatingTooltip(target) {
    if (target && activeTooltipTarget !== target) return;
    activeTooltipTarget = null;
    floatingTooltip.classList.remove('is-visible');
  }

  function focusWithoutTooltip(target) {
    if (!target) return;
    suppressedTooltipFocusTargets.add(target);
    target.focus({ preventScroll: true });
  }

  document.querySelectorAll('.editor-actions [data-tooltip]').forEach(target => {
    target.addEventListener('pointerenter', () => showFloatingTooltip(target));
    target.addEventListener('pointerleave', () => hideFloatingTooltip(target));
    target.addEventListener('focus', () => {
      if (suppressedTooltipFocusTargets.delete(target)) return;
      showFloatingTooltip(target);
    });
    target.addEventListener('blur', () => hideFloatingTooltip(target));
  });

  window.addEventListener('scroll', () => {
    if (activeTooltipTarget) positionFloatingTooltip(activeTooltipTarget);
  }, true);

  window.addEventListener('resize', () => {
    if (activeTooltipTarget) positionFloatingTooltip(activeTooltipTarget);
  });

  function setCopiedState(button, copiedLabel = 'Copied AGENTS.md', defaultLabel = 'Copy AGENTS.md') {
    const existingTimer = copiedStateTimers.get(button);
    if (existingTimer) {
      window.clearTimeout(existingTimer);
    }

    button.setAttribute('aria-label', copiedLabel);
    button.setAttribute('data-tooltip', copiedLabel);
    button.classList.add('is-copied');
    button.querySelector('.t-icon-swap')?.setAttribute('data-state', 'b');
    button.blur();
    showFloatingTooltip(button);

    const timer = window.setTimeout(() => {
      button.setAttribute('aria-label', defaultLabel);
      button.setAttribute('data-tooltip', defaultLabel);
      button.classList.remove('is-copied');
      button.querySelector('.t-icon-swap')?.setAttribute('data-state', 'a');
      copiedStateTimers.delete(button);
      hideFloatingTooltip(button);
    }, 650);

    copiedStateTimers.set(button, timer);
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

  function getModalCloseDuration() {
    if (prefersReducedMotion) return 0;

    const value = getComputedStyle(document.documentElement).getPropertyValue('--modal-close-dur');
    return Number.parseFloat(value) || 150;
  }

  function openModal(dialog, panel) {
    dialog.hidden = false;
    dialog.setAttribute('aria-hidden', 'false');
    dialog.classList.remove('is-closing');
    panel.classList.remove('is-closing');

    // Commit the resting closed state before transitioning to open.
    void panel.offsetWidth;
    dialog.classList.add('is-open');
    panel.classList.add('is-open');
    document.body.classList.add('is-dialog-open');
  }

  async function closeModal(dialog, panel) {
    dialog.classList.remove('is-open');
    panel.classList.remove('is-open');
    dialog.classList.add('is-closing');
    panel.classList.add('is-closing');

    await new Promise(resolve => window.setTimeout(resolve, getModalCloseDuration()));

    // A reopened modal has already removed is-closing; its older close timer
    // must not hide the new presentation state.
    if (!panel.classList.contains('is-closing')) return false;

    dialog.classList.remove('is-closing');
    panel.classList.remove('is-closing');
    dialog.hidden = true;
    dialog.setAttribute('aria-hidden', 'true');
    return true;
  }

  function openAgentsDialog() {
    if (!agentsDialog || !agentsDialogPanel || isAgentsDialogOpen) return;

    isAgentsDialogOpen = true;
    setAgentsView(activeAgentsView);
    openModal(agentsDialog, agentsDialogPanel);
    focusWithoutTooltip(closeAgentsDialogBtn);
  }

  async function closeAgentsDialog() {
    if (!agentsDialog || !agentsDialogPanel || !isAgentsDialogOpen) return;

    isAgentsDialogOpen = false;
    const didClose = await closeModal(agentsDialog, agentsDialogPanel);
    if (!didClose) return;
    if (!isSkillDialogOpen) document.body.classList.remove('is-dialog-open');
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
      const title = item.querySelector('.skill-name')?.textContent?.trim() || 'Skill';
      const contentPath = skillContentPaths[item.id];

      if (!contentPath) {
        const externalUrl = getSkillGithubUrl(item.id);
        item.setAttribute('data-skill-action', 'external');
        item.setAttribute('role', 'link');
        item.setAttribute('tabindex', '0');
        item.setAttribute('aria-label', `Open ${title} on GitHub`);

        const openExternal = () => {
          window.open(externalUrl, '_blank', 'noopener,noreferrer');
        };

        item.addEventListener('click', openExternal);
        item.addEventListener('keydown', event => {
          if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault();
            openExternal();
          }
        });
        return;
      }

      item.setAttribute('data-skill-action', 'dialog');
      item.setAttribute('role', 'button');
      item.setAttribute('tabindex', '0');

      const open = async () => {
        if (!skillDialog || !skillDialogPanel || !skillDialogLabel || !skillDialogTitle || !skillRawView || !skillRawCode || !skillRenderedView) return;

        lastSkillTrigger = item;
        const label = item.querySelector('.skill-label')?.textContent?.trim() || 'Skill';
        const fallback = item.querySelector('.skill-detail')?.textContent?.replace(/^[\s-]+/, '').trim() || '';

        skillDialogLabel.textContent = label;
        skillDialogTitle.textContent = title;
        if (skillGithubLink) {
          skillGithubLink.href = getSkillGithubUrl(item.id);
        }
        skillRawCode.textContent = 'Loading SKILL.md...';
        skillRenderedView.innerHTML = '<p>Loading SKILL.md...</p>';
        setSkillView('raw');
        isSkillDialogOpen = true;
        openModal(skillDialog, skillDialogPanel);
        focusWithoutTooltip(closeSkillDialogBtn);

        try {
          const detail = await loadSkillContent(item.id);
          if (lastSkillTrigger === item && isSkillDialogOpen) {
            skillRawCode.textContent = detail;
            skillRenderedView.innerHTML = renderMarkdown(getRenderableSkillMarkdown(detail));
            skillRawView.scrollTop = 0;
            skillRawView.scrollLeft = 0;
            skillRenderedView.scrollTop = 0;
          }
        } catch (error) {
          console.warn('Failed to load skill content', error);
          const fallbackContent = fallback || 'Failed to load SKILL.md.';
          skillRawCode.textContent = fallbackContent;
          skillRenderedView.innerHTML = renderMarkdown(fallbackContent);
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

  function getSkillGithubUrl(skillId) {
    const externalSkillUrls = {
      'dynamic-workflows': 'https://github.com/DannyMac180/skills/blob/main/codex-dynamic-workflows',
      'grill-with-docs': 'https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs',
      'grill-me': 'https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me',
      'compact-handoff': 'https://github.com/mattpocock/skills/blob/main/skills/productivity/handoff',
      'thermo-nuclear-code-quality-review': 'https://github.com/cursor/plugins/blob/main/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md',
      'create-cli': 'https://github.com/steipete/create-cli',
      'make-interfaces-feel-better': 'https://github.com/jakubkrehel/make-interfaces-feel-better',
      'emil-design-eng': 'https://github.com/BiniamD/emil-design-eng',
      'changelog': 'https://github.com/pavelsimo/changelog',
      'bugbash': 'https://github.com/av/skills/tree/master/bugbash',
      'bughunt': 'https://github.com/av/skills/tree/master/bughunt',
      'commit-helper': 'https://github.com/butttons/pi-kit/tree/main/skills/commit-helper',
      'ideate': 'https://github.com/av/skills/tree/master/ideate',
      'timeboxed-iterating': 'https://github.com/av/skills/tree/master/timeboxed-iterating',
      'release-helper': 'https://github.com/butttons/pi-kit/tree/main/skills/release-helper',
      'oracle': 'https://github.com/openclaw/openclaw/blob/main/skills/oracle/SKILL.md',
      'quality-code': 'https://github.com/RhysSullivan/skills/blob/main/skills/quality-code',
      'review-animations': 'https://github.com/emilkowalski/skills/blob/main/skills/review-animations',
      'animation-vocabulary': 'https://github.com/emilkowalski/skills/blob/main/skills/animation-vocabulary',
      'write-better-error-messages': 'https://github.com/gillkyle/skills/blob/main/skills/write-better-error-messages',
      'domain-modeling': 'https://github.com/mattpocock/skills/blob/main/skills/engineering/domain-modeling',
      'codebase-design': 'https://github.com/mattpocock/skills/blob/main/skills/engineering/codebase-design/SKILL.md',
      'grilling': 'https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling',
      'teach': 'https://github.com/mattpocock/skills/blob/main/skills/productivity/teach',
      'writing-great-skills': 'https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-great-skills',
      'apple-design': 'https://github.com/emilkowalski/skills/blob/main/skills/apple-design',
      'transitions-dev': 'https://github.com/Jakubantalik/transitions.dev/tree/main/skills/transitions-dev',
      'cli-review': 'https://github.com/greptileai/skills/blob/main/skills/cli-review',
      'greploop': 'https://github.com/greptileai/skills/blob/main/skills/greploop',
      'better-colors': 'https://github.com/jakubkrehel/skills/blob/main/skills/better-colors',
      'improve-codebase-architecture': 'https://github.com/mattpocock/skills/blob/main/skills/engineering/improve-codebase-architecture',
      'better-typography': 'https://github.com/jakubkrehel/skills/blob/main/skills/better-typography',
      'better-ui': 'https://github.com/jakubkrehel/skills/blob/main/skills/better-ui',
      'improve-animations': 'https://github.com/emilkowalski/skills/blob/main/skills/improve-animations',
      'resolving-merge-conflicts': 'https://github.com/mattpocock/skills/blob/main/skills/engineering/resolving-merge-conflicts',
      'wayfinder': 'https://github.com/mattpocock/skills/blob/main/skills/engineering/wayfinder',
      'tmux-codex-orchestrator': 'https://github.com/ValXp/ai_tools/tree/main/skills/tmux-codex-orchestrator',
      'transitions-polish': 'https://github.com/Jakubantalik/transitions.dev/tree/main/skills/transitions-polish',
      'declankify': 'https://github.com/DeweyMarco/declankify',
    };

    if (externalSkillUrls[skillId]) {
      return externalSkillUrls[skillId];
    }

    const path = skillContentPaths[skillId];
    if (!path) {
      throw new Error(`No canonical source URL for ${skillId}`);
    }

    const repoBaseUrl = 'https://github.com/micr-dev/ai';
    const sourcePath = path.endsWith('/SKILL.md') ? path.slice(0, -'/SKILL.md'.length) : path;
    const view = path.endsWith('/SKILL.md') ? 'tree' : 'blob';
    return `${repoBaseUrl}/${view}/main/${sourcePath}`;
  }

  function getRenderableSkillMarkdown(markdown) {
    return markdown.replace(/^---\n[\s\S]*?\n---\n?/, '').trim();
  }

  async function closeSkillDialog() {
    if (!skillDialog || !skillDialogPanel || !isSkillDialogOpen) return;

    isSkillDialogOpen = false;
    const didClose = await closeModal(skillDialog, skillDialogPanel);
    if (!didClose) return;
    if (!isAgentsDialogOpen) {
      document.body.classList.remove('is-dialog-open');
    }
    lastSkillTrigger?.focus({ preventScroll: true });
  }

  closeSkillDialogBtn?.addEventListener('click', closeSkillDialog);
  skillDialogBackdrop?.addEventListener('click', closeSkillDialog);

  setupRoleFlips();
  setupSkillDialog();

  setupSnapshotLinks();

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
