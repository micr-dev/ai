# MCP Server Development

Comprehensive guide for developing Model Context Protocol (MCP) servers for OpenCode integration.

## Triggers

Use this skill when the user mentions:
- "create MCP server"
- "build MCP"
- "develop MCP"
- "MCP server development"
- "new MCP tool"
- "MCP integration"
- "scaffold MCP"
- "MCP protocol"

## Overview

This skill provides patterns, templates, and workflows for creating production-ready MCP servers that integrate seamlessly with OpenCode.

## MCP Architecture

### Core Concepts

**MCP Server:** Exposes tools/resources via stdio/HTTP
**MCP Client:** OpenCode connects and invokes tools
**Tools:** Functions the AI can call
**Resources:** Static/dynamic content the AI can read
**Prompts:** Reusable prompt templates

### Communication Patterns

1. **stdio (Standard I/O)** - Most common, process-based
2. **HTTP/SSE** - For remote servers or web services
3. **WebSocket** - For bidirectional streaming

## Workflow

### 1. Planning Phase

**Define your MCP server:**
- What tools will it expose?
- What data sources does it access?
- What authentication is needed?
- Will it be local or remote?

**Example planning questions:**
```
- Tool: "search_reddit" - searches Reddit posts
- Data: Reddit API via PRAW
- Auth: Reddit API credentials
- Type: Local stdio server
```

### 2. Project Scaffolding

**TypeScript/Node.js (Recommended):**
```bash
mkdir mcp-[name]
cd mcp-[name]
npm init -y
npm install @modelcontextprotocol/sdk
npm install -D typescript @types/node tsx
```

**Python:**
```bash
mkdir mcp-[name]
cd mcp-[name]
uv init
uv add mcp
```

**Project structure:**
```
mcp-[name]/
├── src/
│   ├── index.ts          # Main server entry
│   ├── tools/            # Tool implementations
│   │   ├── tool1.ts
│   │   └── tool2.ts
│   └── types.ts          # Type definitions
├── package.json
├── tsconfig.json
└── README.md
```

### 3. Server Implementation (TypeScript)

**Basic server template:**
```typescript
#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

// Create server instance
const server = new Server(
  {
    name: "mcp-[name]",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "tool_name",
        description: "Clear description of what this tool does",
        inputSchema: {
          type: "object",
          properties: {
            param1: {
              type: "string",
              description: "Parameter description",
            },
            param2: {
              type: "number",
              description: "Another parameter",
            },
          },
          required: ["param1"],
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "tool_name": {
      // Validate arguments
      if (!args.param1) {
        throw new Error("param1 is required");
      }

      // Execute tool logic
      const result = await executeToolLogic(args);

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(result, null, 2),
          },
        ],
      };
    }

    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("MCP server running on stdio");
}

main().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});
```

### 4. Tool Schema Design

**Best practices for input schemas:**

```typescript
// Good: Specific, well-documented
{
  name: "search_posts",
  description: "Search Reddit posts by query with filters",
  inputSchema: {
    type: "object",
    properties: {
      query: {
        type: "string",
        description: "Search query string",
      },
      subreddit: {
        type: "string",
        description: "Optional subreddit to search in (without r/ prefix)",
      },
      limit: {
        type: "number",
        description: "Maximum results to return (1-100, default: 25)",
        minimum: 1,
        maximum: 100,
        default: 25,
      },
      sort: {
        type: "string",
        enum: ["relevance", "hot", "top", "new"],
        description: "Sort order for results",
        default: "relevance",
      },
    },
    required: ["query"],
  },
}

// Bad: Vague, no validation
{
  name: "search",
  description: "Search stuff",
  inputSchema: {
    type: "object",
    properties: {
      q: { type: "string" },
      opts: { type: "object" },
    },
  },
}
```

### 5. Error Handling

**Robust error handling pattern:**
```typescript
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  try {
    const { name, arguments: args } = request.params;

    // Validate tool exists
    if (!VALID_TOOLS.includes(name)) {
      return {
        content: [
          {
            type: "text",
            text: `Error: Unknown tool '${name}'`,
          },
        ],
        isError: true,
      };
    }

    // Validate arguments
    const validation = validateArgs(name, args);
    if (!validation.valid) {
      return {
        content: [
          {
            type: "text",
            text: `Error: Invalid arguments - ${validation.error}`,
          },
        ],
        isError: true,
      };
    }

    // Execute with timeout
    const result = await Promise.race([
      executeTool(name, args),
      timeout(30000), // 30s timeout
    ]);

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(result, null, 2),
        },
      ],
    };
  } catch (error) {
    console.error("Tool execution error:", error);
    return {
      content: [
        {
          type: "text",
          text: `Error: ${error.message}`,
        },
      ],
      isError: true,
    };
  }
});
```

### 6. Configuration Management

**Environment variables pattern:**
```typescript
// config.ts
import { z } from "zod";

const configSchema = z.object({
  API_KEY: z.string().min(1, "API_KEY is required"),
  API_URL: z.string().url().default("https://api.example.com"),
  TIMEOUT_MS: z.coerce.number().default(30000),
  DEBUG: z.coerce.boolean().default(false),
});

export const config = configSchema.parse(process.env);
```

**Usage:**
```typescript
import { config } from "./config.js";

const response = await fetch(config.API_URL, {
  headers: {
    Authorization: `Bearer ${config.API_KEY}`,
  },
  signal: AbortSignal.timeout(config.TIMEOUT_MS),
});
```

### 7. Testing

**Test tool invocations:**
```typescript
// test/tools.test.ts
import { describe, it, expect } from "vitest";
import { executeTool } from "../src/tools/index.js";

describe("search_posts tool", () => {
  it("should search with valid query", async () => {
    const result = await executeTool("search_posts", {
      query: "typescript",
      limit: 5,
    });

    expect(result).toHaveProperty("posts");
    expect(result.posts).toHaveLength(5);
  });

  it("should reject invalid limit", async () => {
    await expect(
      executeTool("search_posts", {
        query: "test",
        limit: 200, // exceeds max
      })
    ).rejects.toThrow("limit must be between 1 and 100");
  });
});
```

**Manual testing with MCP Inspector:**
```bash
npx @modelcontextprotocol/inspector node dist/index.js
```

### 8. OpenCode Integration

**Add to OpenCode config:**
```json
{
  "mcpServers": {
    "mcp-[name]": {
      "command": "node",
      "args": ["/path/to/mcp-[name]/dist/index.js"],
      "env": {
        "API_KEY": "your-api-key"
      }
    }
  }
}
```

**Or use npx for published packages:**
```json
{
  "mcpServers": {
    "mcp-[name]": {
      "command": "npx",
      "args": ["-y", "mcp-[name]@latest"],
      "env": {
        "API_KEY": "your-api-key"
      }
    }
  }
}
```

### 9. Documentation

**README.md template:**
```markdown
# mcp-[name]

[Brief description of what this MCP server does]

## Installation

\`\`\`bash
npm install -g mcp-[name]
\`\`\`

## Configuration

Add to your OpenCode config:

\`\`\`json
{
  "mcpServers": {
    "mcp-[name]": {
      "command": "mcp-[name]",
      "env": {
        "API_KEY": "your-api-key"
      }
    }
  }
}
\`\`\`

## Tools

### tool_name

Description of what this tool does.

**Parameters:**
- `param1` (string, required): Description
- `param2` (number, optional): Description

**Example:**
\`\`\`
User: "Use tool_name with param1=value"
Agent: [calls tool and returns result]
\`\`\`

## Development

\`\`\`bash
npm install
npm run build
npm test
\`\`\`

## License

MIT
```

### 10. Publishing

**Prepare for npm:**
```json
// package.json
{
  "name": "mcp-[name]",
  "version": "1.0.0",
  "type": "module",
  "bin": {
    "mcp-[name]": "./dist/index.js"
  },
  "files": [
    "dist"
  ],
  "scripts": {
    "build": "tsc",
    "prepublishOnly": "npm run build"
  }
}
```

**Publish:**
```bash
npm run build
npm publish
```

## Common Patterns

### Pattern 1: API Wrapper MCP

Wrap external APIs (Reddit, GitHub, etc.):
- One tool per API endpoint
- Handle rate limiting
- Cache responses when appropriate
- Provide clear error messages

### Pattern 2: Local Tool MCP

Execute local operations (file search, git, etc.):
- Validate paths/permissions
- Use safe execution patterns
- Return structured output
- Handle timeouts

### Pattern 3: Database MCP

Query databases:
- Use connection pooling
- Parameterized queries only
- Read-only by default
- Clear schema documentation

### Pattern 4: Browser Automation MCP

Control browsers (Playwright, Puppeteer):
- Manage browser lifecycle
- Handle navigation timeouts
- Capture screenshots
- Clean up resources

## Best Practices

1. **Clear tool names** - Use verb_noun pattern (search_posts, create_issue)
2. **Detailed descriptions** - Help AI understand when to use each tool
3. **Strong typing** - Use JSON Schema validation
4. **Error messages** - Be specific about what went wrong
5. **Timeouts** - Always set reasonable timeouts
6. **Logging** - Use stderr for logs (stdout is for MCP protocol)
7. **Security** - Validate all inputs, use environment variables for secrets
8. **Testing** - Test each tool independently
9. **Documentation** - Clear examples for each tool
10. **Versioning** - Use semantic versioning

## Tools to Use

- `write` - Create server files
- `bash` - Run build/test commands
- `read` - Read existing MCP servers for reference
- `edit` - Update configuration files

## Example Session

```
User: "Create an MCP server for Hacker News API"

Agent:
1. Creates project structure
2. Implements tools:
   - search_stories
   - get_story
   - get_comments
3. Adds error handling and validation
4. Creates tests
5. Generates documentation
6. Provides OpenCode config snippet

User: "Add it to my OpenCode config"

Agent:
1. Reads ~/.config/opencode/config.json
2. Adds mcp-hackernews entry
3. Verifies configuration
4. Suggests testing with a simple query
```

## References

- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [MCP SDK Documentation](https://github.com/modelcontextprotocol/sdk)
- [OpenCode MCP Integration](https://opencode.ai/docs/mcp)

## Notes

- Prefer TypeScript for type safety
- Use stdio transport for local servers
- Test with MCP Inspector before OpenCode integration
- Keep tools focused and single-purpose
- Version your MCP servers properly