# Reddit Research Skill

## Triggers

Use this skill when the user asks to:
- "Search Reddit for..."
- "Find Reddit discussions about..."
- "What does Reddit say about..."
- "Look up Reddit threads on..."
- "Find Reddit opinions on..."
- "Research on Reddit..."
- "Check Reddit for..."
- "Analyze Reddit sentiment about..."
- "Find Reddit communities discussing..."

## Overview

This skill provides a systematic workflow for researching topics on Reddit using a two-phase approach:
1. **Discovery Phase**: Use Kagi Search with Reddit site filters to find relevant threads
2. **Analysis Phase**: Use reddit-mcp-buddy MCP to fetch structured data and analyze content

This approach combines the speed of search with the depth of structured Reddit API access.

## Workflow

### Phase 1: Discovery with Kagi Search

**Step 1: Construct the search query**
- Start with the user's topic/keywords
- Add `site:reddit.com` filter
- For broader coverage, use: `(site:reddit.com OR site:old.reddit.com OR site:redd.it)`
- Add time filters if needed: `after:2024-01-01`
- Add subreddit filters: `site:reddit.com/r/programming`

**Step 2: Execute Kagi search**
```bash
# Use kagi-search MCP tool
kagi-search with query: "topic site:reddit.com"
```

**Step 3: Extract Reddit URLs**
- Collect post URLs from search results
- Prioritize by relevance score and recency
- Typical batch size: 3-5 most relevant posts

### Phase 2: Deep Analysis with reddit-mcp-buddy

**Step 4: Fetch post details**
For each URL from Phase 1:
```bash
# Use reddit-mcp-buddy_get_post_details
- url: <reddit-url>
- comment_limit: 20-50 (default 20)
- comment_depth: 2-3 (default 3)
- comment_sort: "best" | "top" | "new" | "controversial"
- max_top_comments: 5 (default 5)
```

**Step 5: Analyze structured data**
Extract from each post:
- Post title, score, author, timestamp
- Post content/selftext
- Top comments with scores
- Comment threads (nested discussions)
- Subreddit context

**Step 6: Synthesize findings**
- Identify common themes across posts
- Note sentiment patterns (positive/negative/mixed)
- Highlight expert opinions (high-karma users, detailed responses)
- Flag controversies (high comment count, low score)
- Extract actionable insights

### Alternative Workflows

**For subreddit exploration:**
```bash
# Browse a specific subreddit
reddit-mcp-buddy_browse_subreddit
- subreddit: "programming"
- sort: "hot" | "new" | "top" | "rising"
- limit: 25 (default)
- time: "day" | "week" | "month" | "year" | "all"
```

**For Reddit-wide search:**
```bash
# Search across all of Reddit
reddit-mcp-buddy_search_reddit
- query: "search terms"
- subreddits: [] (empty for all)
- sort: "relevance" | "hot" | "top" | "new" | "comments"
- limit: 25 (default)
- time: "all" (default)
```

**For user analysis:**
```bash
# Analyze a Reddit user's activity
reddit-mcp-buddy_user_analysis
- username: "username"
- posts_limit: 10 (default)
- comments_limit: 10 (default)
- time_range: "month" (default)
```

## Best Practices

### Search Strategy
1. **Start broad, then narrow**: Begin with general Kagi search, then drill into specific subreddits
2. **Use time filters**: Recent discussions often more relevant than old threads
3. **Check multiple subreddits**: Different communities have different perspectives
4. **Look for megathreads**: Often contain concentrated expert discussion

### Comment Analysis
1. **Prioritize high-karma comments**: Usually indicate quality/accuracy
2. **Read controversial comments**: Often reveal important caveats or alternatives
3. **Check user history**: Frequent posters in a subreddit often have domain expertise
4. **Follow comment chains**: Deep threads often contain nuanced discussion

### Rate Limiting
1. **Batch requests**: Fetch 3-5 posts at once, then analyze
2. **Use appropriate limits**: Start with `comment_limit: 20`, increase only if needed
3. **Respect depth**: `comment_depth: 2-3` usually sufficient for most research
4. **Monitor for errors**: If rate-limited, add delays between requests

### Data Quality
1. **Verify claims**: Reddit opinions are not facts; cross-reference with official sources
2. **Note biases**: Each subreddit has its own culture and biases
3. **Check dates**: Old threads may contain outdated information
4. **Consider sample size**: Single thread ≠ consensus

## Tools to Use

### Primary Tools
- **kagi-search**: Discovery phase, finding relevant Reddit threads
- **reddit-mcp-buddy_get_post_details**: Deep analysis of specific posts
- **reddit-mcp-buddy_search_reddit**: Reddit-native search when Kagi insufficient
- **reddit-mcp-buddy_browse_subreddit**: Exploring specific communities

### Supporting Tools
- **reddit-mcp-buddy_user_analysis**: Vetting expert opinions
- **reddit-mcp-buddy_reddit_explain**: Understanding Reddit terminology/culture

### When NOT to Use Reddit Research
- Official documentation exists (prefer primary sources)
- Legal/medical advice needed (Reddit is not authoritative)
- Real-time information required (Reddit has delays)
- Quantitative data needed (Reddit is qualitative/anecdotal)

## Example Session

**User request**: "What do developers think about Bun vs Node.js?"

**Step 1: Kagi Discovery**
```
Query: "bun vs node.js site:reddit.com/r/programming OR site:reddit.com/r/node OR site:reddit.com/r/javascript"
Results: 5 relevant threads from past 6 months
```

**Step 2: Fetch Top 3 Posts**
```
Post 1: "Switched from Node to Bun - My Experience" (r/programming, 450 upvotes)
Post 2: "Bun 1.0 Discussion Thread" (r/node, 320 upvotes)
Post 3: "Is Bun production-ready?" (r/javascript, 180 upvotes)
```

**Step 3: Analyze Each Post**
```
reddit-mcp-buddy_get_post_details for each URL
- comment_limit: 30
- comment_depth: 3
- comment_sort: "best"
```

**Step 4: Synthesize Findings**
```
Common themes:
- Performance: Bun significantly faster for cold starts
- Compatibility: Some npm packages have issues
- Ecosystem: Node.js has more mature tooling
- Production use: Mixed opinions, many waiting for 1.x stability

Expert opinions (high-karma users):
- "Use Bun for new projects, stick with Node for production"
- "Performance gains real but ecosystem gaps exist"
- "Wait 6 months for ecosystem to catch up"

Controversies:
- Debate over benchmark validity
- Concerns about long-term maintenance
- Questions about corporate backing
```

**Step 5: Deliver Summary**
Present findings with:
- Key themes and sentiment
- Notable expert quotes
- Links to most valuable threads
- Caveats and limitations
- Recommendation based on use case

## Notes

### Reddit API Limitations
- reddit-mcp-buddy uses Reddit's public API (no authentication required)
- Rate limits apply (typically 60 requests/minute)
- Some content may be unavailable (deleted posts, private subreddits)
- Real-time data may have slight delays

### Subreddit Selection Guide
**Technology:**
- r/programming, r/webdev, r/javascript, r/python, r/golang
- r/ExperiencedDevs (senior perspectives)
- r/cscareerquestions (career advice)

**Products/Services:**
- r/SaaS, r/startups, r/Entrepreneur
- r/selfhosted (self-hosting discussions)
- r/homelab (infrastructure)

**Specific Tools:**
- r/node, r/reactjs, r/nextjs, r/svelte
- r/docker, r/kubernetes, r/aws

**General Discussion:**
- r/AskReddit (broad questions)
- r/explainlikeimfive (simple explanations)
- r/OutOfTheLoop (context on trends)

### Quality Signals
**High-quality threads:**
- Detailed original post with specific questions
- Multiple high-karma responses
- Active discussion (not just upvotes)
- Recent activity (within 6 months)
- Subreddit has active moderation

**Low-quality threads:**
- Vague or clickbait titles
- Few or low-quality comments
- Very old (>2 years unless historical research)
- Heavily downvoted
- Locked/removed by moderators

### Integration with Other Research
Reddit research works best when combined with:
1. **Official documentation** (ground truth)
2. **Kagi/Perplexity** (broader web research)
3. **GitHub issues** (technical details)
4. **Blog posts** (in-depth analysis)
5. **Stack Overflow** (specific technical problems)

Use Reddit for:
- Real-world experiences and opinions
- Community sentiment and trends
- Practical advice and gotchas
- Alternative perspectives
- Discovering edge cases

Don't use Reddit for:
- Official specifications
- Legal/compliance information
- Medical/safety-critical advice
- Authoritative facts
- Real-time breaking news
