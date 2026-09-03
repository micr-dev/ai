# Browser Automation Testing Skill

## Triggers

Use this skill when the user asks to:
- "Test this page in a browser"
- "Automate browser interactions"
- "Fill out this form automatically"
- "Click through this workflow"
- "Test the UI flow"
- "Verify the page loads correctly"
- "Capture screenshots of..."
- "Extract data from this website"
- "Test login flow"
- "Verify navigation works"
- "Check if elements are visible"
- "Scrape this website"
- "Monitor this page for changes"

## Overview

This skill provides systematic workflows for browser automation using the camofox-browser-mcp server. Camofox provides:
- Real browser rendering (Firefox-based)
- Anti-detection features (evades bot detection)
- Stable element references (snapshot-based interaction)
- Session persistence (cookies, localStorage)
- Multi-tab support

**Key Philosophy**: Use accessibility snapshots with stable `ref` identifiers instead of fragile CSS selectors.

## Workflow

### Phase 1: Setup and Navigation

**Step 1: Ensure backend is running**
```bash
# Start the camofox browser engine
camofox-browser-mcp_camofox_start_browser
```

If this fails with connectivity errors, start the backend manually:
```bash
# In a tmux session
tmux new -s camofox
camofox-browser
# Detach with Ctrl+B, D
```

**Step 2: Create a tab**
```bash
camofox-browser-mcp_camofox_create_tab
- userId: (optional, defaults to CAMOFOX_DEFAULT_USER_ID)
- sessionKey: (optional, for grouping tabs)
- url: (optional, initial URL to load)
```

Returns: `tabId` (use for all subsequent operations)

**Step 3: Navigate to target**
```bash
# Option A: Direct navigation
camofox-browser-mcp_camofox_navigate_tab
- tabId: <tab-id>
- url: "https://example.com"

# Option B: Navigate + snapshot in one call
camofox-browser-mcp_navigate_and_snapshot
- tabId: <tab-id>
- url: "https://example.com"
- waitForNetwork: true (default)
- waitTimeoutMs: 10000 (default)
- includeScreenshot: false (optional)
```

**Step 4: Wait for page ready**
```bash
camofox-browser-mcp_camofox_wait
- tabId: <tab-id>
- timeoutMs: 10000 (default)
- waitForNetwork: true (default)
```

### Phase 2: Snapshot-Based Interaction

**Step 5: Capture accessibility snapshot**
```bash
camofox-browser-mcp_camofox_get_snapshot
- tabId: <tab-id>
- offset: 0 (for pagination on long pages)
- includeScreenshot: false (set true for visual debugging)
```

Returns:
- Accessibility tree with stable `ref` identifiers (e1, e2, e3...)
- Element roles, names, values
- Interactive elements (buttons, links, inputs)
- Current URL and page title

**Step 6: Identify target elements**
From the snapshot, find elements by:
- Role (button, link, textbox, etc.)
- Name/label (visible text)
- Value (current input value)
- Position in tree

Example snapshot output:
```
e1: button "Sign In"
e2: textbox "Email" (value: "")
e3: textbox "Password" (value: "")
e4: link "Forgot password?"
```

**Step 7: Interact using refs**
```bash
# Click an element
camofox-browser-mcp_camofox_click
- tabId: <tab-id>
- ref: "e1"

# Type into an input
camofox-browser-mcp_camofox_type
- tabId: <tab-id>
- ref: "e2"
- text: "user@example.com"
- pressEnter: false (optional)

# Fill multiple fields at once
camofox-browser-mcp_fill_form
- tabId: <tab-id>
- fields: [
    {ref: "e2", value: "user@example.com"},
    {ref: "e3", value: "password123"}
  ]
- submitRef: "e1" (optional, click after filling)
```

**Step 8: Re-snapshot after changes**
After navigation, form submission, or dynamic content loading:
```bash
# Wait for changes to settle
camofox-browser-mcp_camofox_wait
- tabId: <tab-id>

# Capture new snapshot
camofox-browser-mcp_camofox_get_snapshot
- tabId: <tab-id>
```

### Phase 3: Verification and Extraction

**Step 9: Verify expected state**
Check snapshot for:
- Expected elements present (success messages, new page elements)
- Error messages absent
- URL changed as expected
- Page title correct

**Step 10: Extract data**
```bash
# Get all links on page
camofox-browser-mcp_camofox_get_links
- tabId: <tab-id>
- limit: 50 (default)
- offset: 0 (for pagination)

# Capture screenshot for visual verification
camofox-browser-mcp_camofox_screenshot
- tabId: <tab-id>
- fullPage: false (set true for full-page screenshot)
```

**Step 11: Clean up**
```bash
# Close tab when done
camofox-browser-mcp_camofox_close_tab
- tabId: <tab-id>

# Or close entire session
camofox-browser-mcp_camofox_close_session
- userId: (optional)
```

## Best Practices

### Snapshot-Driven Development
1. **Always snapshot before interacting**: Get fresh refs after any page change
2. **Use refs, not selectors**: Refs are stable across snapshots; CSS selectors are fragile
3. **Verify element presence**: Check snapshot contains expected elements before clicking
4. **Handle dynamic content**: Wait for network idle before snapshotting

### Waiting Strategies
```bash
# Wait for page load
camofox-browser-mcp_camofox_wait
- waitForNetwork: true

# Wait for specific text to appear
camofox-browser-mcp_camofox_wait_for_text
- tabId: <tab-id>
- text: "Success"

# Scroll to load lazy content
camofox-browser-mcp_camofox_scroll
- tabId: <tab-id>
- direction: "down"
- amount: 700 (pixels)
```

### Form Filling Patterns
```bash
# Pattern 1: Fill and submit separately
fill_form with fields
click submitRef

# Pattern 2: Type and press Enter
camofox-browser-mcp_type_and_submit
- ref: "e2"
- text: "search query"
- submitKey: "Enter"

# Pattern 3: Batch clicks
camofox-browser-mcp_batch_click
- actions: [{ref: "e1"}, {ref: "e2"}, {ref: "e3"}]
- delayMs: 500 (between clicks)
```

### Error Handling
1. **Check for error messages**: After form submission, snapshot and look for error text
2. **Verify navigation**: Check URL changed as expected
3. **Handle timeouts**: Increase `waitTimeoutMs` for slow pages
4. **Retry on failure**: Re-snapshot and retry with fresh refs

### Session Management
```bash
# Group related tabs
create_tab with sessionKey: "test-session-1"
create_tab with sessionKey: "test-session-1"

# Close all tabs in a group
camofox-browser-mcp_camofox_close_tab_group
- sessionKey: "test-session-1"

# List all tabs
camofox-browser-mcp_camofox_list_tabs
- userId: (optional)
```

### Cookie Management
```bash
# Import cookies for authenticated sessions
camofox-browser-mcp_camofox_import_cookies
- cookies: [{name: "session", value: "...", domain: ".example.com"}]
# OR
- cookiesFilePath: "/path/to/cookies.json"
```

## Tools to Use

### Core Navigation
- **camofox-browser-mcp_camofox_start_browser**: Initialize browser engine
- **camofox-browser-mcp_camofox_create_tab**: Create new tab
- **camofox-browser-mcp_camofox_navigate_tab**: Navigate to URL
- **camofox-browser-mcp_navigate_and_snapshot**: Navigate + snapshot in one call
- **camofox-browser-mcp_camofox_wait**: Wait for page ready

### Snapshot and Interaction
- **camofox-browser-mcp_camofox_get_snapshot**: Get accessibility tree with refs
- **camofox-browser-mcp_camofox_click**: Click element by ref
- **camofox-browser-mcp_camofox_type**: Type into input by ref
- **camofox-browser-mcp_fill_form**: Fill multiple fields at once
- **camofox-browser-mcp_type_and_submit**: Type and press Enter

### Advanced Interaction
- **camofox-browser-mcp_camofox_hover**: Hover over element
- **camofox-browser-mcp_camofox_press**: Press keyboard key
- **camofox-browser-mcp_camofox_scroll**: Scroll page
- **camofox-browser-mcp_camofox_scroll_element**: Scroll element into view
- **camofox-browser-mcp_batch_click**: Click multiple elements in sequence

### Data Extraction
- **camofox-browser-mcp_camofox_get_links**: Extract all links
- **camofox-browser-mcp_camofox_screenshot**: Capture screenshot
- **camofox-browser-mcp_camofox_get_stats**: Get tab statistics

### Session Management
- **camofox-browser-mcp_camofox_list_tabs**: List all open tabs
- **camofox-browser-mcp_camofox_close_tab**: Close specific tab
- **camofox-browser-mcp_camofox_close_tab_group**: Close tab group
- **camofox-browser-mcp_camofox_close_session**: Close entire session

### History and Navigation
- **camofox-browser-mcp_camofox_back**: Go back in history
- **camofox-browser-mcp_camofox_forward**: Go forward in history
- **camofox-browser-mcp_camofox_refresh**: Reload page

### Special Features
- **camofox-browser-mcp_web_search**: Navigate to search engine results
- **camofox-browser-mcp_camofox_youtube_transcript**: Extract YouTube captions
- **camofox-browser-mcp_camofox_import_cookies**: Import authentication cookies

## Example Session

### Example 1: Login Flow Test

**User request**: "Test the login flow on example.com"

```bash
# Step 1: Start browser and create tab
camofox_start_browser
camofox_create_tab → tabId: "tab-123"

# Step 2: Navigate and snapshot
navigate_and_snapshot
- tabId: "tab-123"
- url: "https://example.com/login"
- waitForNetwork: true

# Snapshot shows:
# e1: textbox "Email"
# e2: textbox "Password"
# e3: button "Sign In"

# Step 3: Fill login form
fill_form
- tabId: "tab-123"
- fields: [
    {ref: "e1", value: "test@example.com"},
    {ref: "e2", value: "testpass123"}
  ]
- submitRef: "e3"

# Step 4: Wait and verify
camofox_wait
- tabId: "tab-123"
- timeoutMs: 5000

get_snapshot
- tabId: "tab-123"

# Check snapshot for:
# - URL changed to /dashboard
# - Welcome message present
# - No error messages

# Step 5: Clean up
close_tab
- tabId: "tab-123"
```

### Example 2: Multi-Step Form

**User request**: "Fill out the registration form with multiple pages"

```bash
# Page 1: Personal Info
navigate_and_snapshot → url: "/register/step1"
# Snapshot: e1=firstName, e2=lastName, e3=email, e4=nextButton

fill_form
- fields: [{ref: "e1", value: "John"}, {ref: "e2", value: "Doe"}, {ref: "e3", value: "john@example.com"}]
- submitRef: "e4"

wait → timeoutMs: 3000

# Page 2: Address
get_snapshot
# Snapshot: e1=street, e2=city, e3=zip, e4=nextButton

fill_form
- fields: [{ref: "e1", value: "123 Main St"}, {ref: "e2", value: "Boston"}, {ref: "e3", value: "02101"}]
- submitRef: "e4"

wait → timeoutMs: 3000

# Page 3: Confirmation
get_snapshot
# Verify all info displayed correctly
# Click final submit button
```

### Example 3: Data Extraction

**User request**: "Extract all product links from the catalog page"

```bash
# Navigate to catalog
navigate_and_snapshot
- url: "https://shop.example.com/catalog"

# Scroll to load lazy content
scroll_and_snapshot
- direction: "down"
- amount: 1000

scroll_and_snapshot
- direction: "down"
- amount: 1000

# Extract all links
get_links
- limit: 100

# Filter for product links (e.g., /product/*)
# Return list of product URLs
```

### Example 4: Search and Verify

**User request**: "Search for 'laptop' and verify results appear"

```bash
# Navigate to homepage
navigate_and_snapshot
- url: "https://example.com"

# Snapshot shows: e1=textbox "Search"

# Type and submit search
type_and_submit
- ref: "e1"
- text: "laptop"
- submitKey: "Enter"

# Wait for results
wait_for_text
- text: "results"

# Verify results page
get_snapshot
# Check for:
# - Search results present
# - "laptop" in page title
# - Multiple product listings
```

## Notes

### When to Use Camofox vs Other Tools

**Use Camofox when:**
- Page requires JavaScript rendering
- Need to interact with dynamic UI (SPAs)
- Testing user workflows
- Bypassing bot detection
- Need session persistence (cookies)
- Extracting data from complex pages

**Use curl/wget when:**
- Simple static HTML pages
- API endpoints
- Raw file downloads
- No JavaScript required

**Use defuddle skill when:**
- Just need readable text/markdown
- Article extraction
- No interaction required

### Performance Optimization

1. **Reuse tabs**: Don't create new tab for each page in a flow
2. **Batch operations**: Use `fill_form` instead of multiple `type` calls
3. **Minimize screenshots**: Only capture when needed for debugging
4. **Use navigate_and_snapshot**: Combines navigation + wait + snapshot
5. **Set appropriate timeouts**: Don't wait longer than necessary

### Debugging Tips

1. **Enable screenshots**: Set `includeScreenshot: true` to see what browser sees
2. **Check console messages**: Use `camofox_get_stats` to see errors
3. **Verify refs exist**: Always check snapshot before using refs
4. **Test selectors**: If refs fail, try CSS selectors as fallback
5. **Increase timeouts**: Slow pages may need longer waits

### Common Pitfalls

1. **Stale refs**: Always re-snapshot after page changes
2. **Race conditions**: Wait for network idle before snapshotting
3. **Wrong element**: Verify ref matches intended element in snapshot
4. **Timeout too short**: Increase for slow-loading pages
5. **Missing wait**: Always wait after navigation/interaction

### Integration with Testing Frameworks

Camofox automation can be integrated with:
- **Vitest**: Write tests that call Camofox tools
- **Playwright**: Use Camofox for anti-detection, Playwright for assertions
- **CI/CD**: Run Camofox in headless mode in pipelines
- **Monitoring**: Schedule periodic checks with Camofox

### Security Considerations

1. **Credentials**: Never hardcode passwords; use environment variables
2. **Cookie storage**: Store cookies securely; don't commit to git
3. **Rate limiting**: Respect target site's rate limits
4. **Terms of Service**: Ensure automation is allowed
5. **Data privacy**: Handle extracted data according to privacy laws
