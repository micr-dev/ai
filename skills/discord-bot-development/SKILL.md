# Discord Bot Development

Comprehensive guide for building Discord bots using discord-py-self MCP and best practices.

## Triggers

Use this skill when the user mentions:
- "discord bot"
- "discord selfbot"
- "discord automation"
- "discord admin commands"
- "discord channel management"
- "discord message handling"
- "build discord bot"
- "discord integration"

## Overview

This skill provides patterns and workflows for developing Discord bots, with focus on the discord-py-self MCP for user account automation and standard bot patterns.

## Discord Bot Types

### 1. User Account Bots (Selfbots)
- Uses discord-py-self MCP
- Runs under your user account
- Good for personal automation
- **Warning:** Against Discord ToS for public use

### 2. Official Bot Accounts
- Uses Discord Bot API
- Requires bot token from Discord Developer Portal
- Proper way for public bots
- Supports slash commands, interactions

## Workflow

### 1. Setup Phase

**For discord-py-self MCP (already installed):**
```bash
# Check if MCP is configured
cat ~/.config/opencode/config.json | grep discord-py-self
```

**For official Discord bot:**
```bash
# Install discord.py
pip install discord.py
# or
uv add discord.py
```

### 2. Common Patterns

#### Pattern A: Message Monitoring

**Use discord-py-self MCP:**
```typescript
// Read recent messages
discord-py-self_read_messages({
  channel_id: "123456789",
  limit: 50
})

// Search for specific content
discord-py-self_search_messages({
  channel_id: "123456789",
  query: "keyword",
  limit: 25
})
```

#### Pattern B: Automated Responses

**Monitor and respond:**
```typescript
// 1. Read messages periodically
const messages = await discord-py-self_read_messages({
  channel_id: "123456789",
  limit: 10
});

// 2. Check for triggers
const needsResponse = messages.find(m => 
  m.content.includes("@me") && !m.author.is_bot
);

// 3. Send response
if (needsResponse) {
  await discord-py-self_send_message({
    channel_id: "123456789",
    content: "Response message"
  });
}
```

#### Pattern C: Channel Management

**Create and organize channels:**
```typescript
// Create channel
discord-py-self_create_channel({
  guild_id: "123456789",
  name: "new-channel",
  type: "text",
  category_id: "987654321" // optional
})

// List all channels
discord-py-self_list_channels({
  guild_id: "123456789"
})

// Delete channel
discord-py-self_delete_channel({
  channel_id: "123456789"
})
```

#### Pattern D: User Management

**Manage server members:**
```typescript
// Kick member
discord-py-self_kick_member({
  guild_id: "123456789",
  user_id: "987654321",
  reason: "Violation of rules"
})

// Ban member
discord-py-self_ban_member({
  guild_id: "123456789",
  user_id: "987654321",
  delete_message_days: 7,
  reason: "Spam"
})

// Add role
discord-py-self_add_role({
  guild_id: "123456789",
  user_id: "987654321",
  role_id: "555555555"
})
```

#### Pattern E: Slash Commands & Interactions

**Handle slash commands:**
```typescript
// Send slash command
discord-py-self_send_slash_command({
  channel_id: "123456789",
  command_name: "poll",
  application_id: "bot_app_id",
  options: {
    question: "What's your favorite color?",
    choices: ["Red", "Blue", "Green"]
  }
})

// Click button
discord-py-self_click_button({
  channel_id: "123456789",
  message_id: "987654321",
  custom_id: "accept_button"
})

// Select menu option
discord-py-self_select_menu({
  channel_id: "123456789",
  message_id: "987654321",
  values: ["option1", "option2"]
})
```

### 3. Bot Architecture

**Modular bot structure:**
```
discord-bot/
├── src/
│   ├── bot.ts              # Main bot entry
│   ├── commands/           # Command handlers
│   │   ├── admin.ts
│   │   ├── moderation.ts
│   │   └── utility.ts
│   ├── events/             # Event handlers
│   │   ├── message.ts
│   │   ├── member.ts
│   │   └── ready.ts
│   ├── utils/              # Helper functions
│   │   ├── permissions.ts
│   │   └── formatting.ts
│   └── config.ts           # Configuration
├── package.json
└── README.md
```

### 4. Command Handler Pattern

**TypeScript command system:**
```typescript
// commands/base.ts
export interface Command {
  name: string;
  description: string;
  aliases?: string[];
  permissions?: string[];
  execute: (args: string[], context: CommandContext) => Promise<void>;
}

export interface CommandContext {
  channelId: string;
  guildId: string;
  authorId: string;
  message: Message;
}

// commands/ping.ts
export const pingCommand: Command = {
  name: "ping",
  description: "Check bot latency",
  aliases: ["p"],
  execute: async (args, context) => {
    const start = Date.now();
    await discord-py-self_send_message({
      channel_id: context.channelId,
      content: "Pinging..."
    });
    const latency = Date.now() - start;
    
    await discord-py-self_edit_message({
      channel_id: context.channelId,
      message_id: sentMessage.id,
      content: `Pong! Latency: ${latency}ms`
    });
  }
};

// bot.ts - Command dispatcher
const commands = new Map<string, Command>();
commands.set("ping", pingCommand);
commands.set("help", helpCommand);

async function handleMessage(message: Message) {
  if (!message.content.startsWith("!")) return;
  
  const [commandName, ...args] = message.content.slice(1).split(" ");
  const command = commands.get(commandName.toLowerCase());
  
  if (!command) return;
  
  const context: CommandContext = {
    channelId: message.channel_id,
    guildId: message.guild_id,
    authorId: message.author.id,
    message
  };
  
  try {
    await command.execute(args, context);
  } catch (error) {
    console.error(`Command error: ${commandName}`, error);
    await discord-py-self_send_message({
      channel_id: context.channelId,
      content: `Error executing command: ${error.message}`
    });
  }
}
```

### 5. Event-Driven Architecture

**Event handler pattern:**
```typescript
// events/message.ts
export async function onMessage(message: Message) {
  // Ignore bot messages
  if (message.author.bot) return;
  
  // Handle commands
  if (message.content.startsWith("!")) {
    await handleCommand(message);
    return;
  }
  
  // Auto-moderation
  if (containsBadWords(message.content)) {
    await discord-py-self_delete_message({
      channel_id: message.channel_id,
      message_id: message.id
    });
    await warnUser(message.author.id);
  }
  
  // Auto-responses
  if (message.content.toLowerCase().includes("hello")) {
    await discord-py-self_send_message({
      channel_id: message.channel_id,
      content: `Hello ${message.author.username}!`
    });
  }
}

// events/member.ts
export async function onMemberJoin(member: Member) {
  // Send welcome message
  const welcomeChannel = await getWelcomeChannel(member.guild_id);
  await discord-py-self_send_message({
    channel_id: welcomeChannel.id,
    content: `Welcome ${member.mention} to the server!`
  });
  
  // Auto-assign role
  await discord-py-self_add_role({
    guild_id: member.guild_id,
    user_id: member.id,
    role_id: "new_member_role_id"
  });
}
```

### 6. Permission System

**Check permissions before actions:**
```typescript
// utils/permissions.ts
export async function hasPermission(
  userId: string,
  guildId: string,
  permission: string
): Promise<boolean> {
  const member = await getMember(guildId, userId);
  const roles = member.roles;
  
  // Check if user has admin role
  const adminRoles = ["admin_role_id", "moderator_role_id"];
  return roles.some(roleId => adminRoles.includes(roleId));
}

// Usage in command
export const kickCommand: Command = {
  name: "kick",
  description: "Kick a member",
  permissions: ["KICK_MEMBERS"],
  execute: async (args, context) => {
    // Check permissions
    if (!await hasPermission(context.authorId, context.guildId, "KICK_MEMBERS")) {
      await discord-py-self_send_message({
        channel_id: context.channelId,
        content: "You don't have permission to use this command."
      });
      return;
    }
    
    const userId = args[0];
    const reason = args.slice(1).join(" ") || "No reason provided";
    
    await discord-py-self_kick_member({
      guild_id: context.guildId,
      user_id: userId,
      reason
    });
  }
};
```

### 7. Rate Limiting

**Avoid Discord rate limits:**
```typescript
// utils/ratelimit.ts
class RateLimiter {
  private buckets = new Map<string, number[]>();
  
  async checkLimit(key: string, maxRequests: number, windowMs: number): Promise<boolean> {
    const now = Date.now();
    const requests = this.buckets.get(key) || [];
    
    // Remove old requests outside window
    const validRequests = requests.filter(time => now - time < windowMs);
    
    if (validRequests.length >= maxRequests) {
      return false; // Rate limited
    }
    
    validRequests.push(now);
    this.buckets.set(key, validRequests);
    return true;
  }
}

const rateLimiter = new RateLimiter();

// Usage
async function sendMessage(channelId: string, content: string) {
  const canSend = await rateLimiter.checkLimit(
    `channel:${channelId}`,
    5, // 5 messages
    10000 // per 10 seconds
  );
  
  if (!canSend) {
    console.warn("Rate limited, waiting...");
    await sleep(2000);
  }
  
  await discord-py-self_send_message({ channel_id: channelId, content });
}
```

### 8. Error Handling

**Robust error handling:**
```typescript
async function safeExecute<T>(
  operation: () => Promise<T>,
  fallback?: T
): Promise<T | null> {
  try {
    return await operation();
  } catch (error) {
    console.error("Operation failed:", error);
    
    if (error.message.includes("Missing Permissions")) {
      console.error("Bot lacks required permissions");
    } else if (error.message.includes("Unknown Channel")) {
      console.error("Channel not found or deleted");
    } else if (error.message.includes("Rate limited")) {
      console.error("Hit rate limit, backing off");
      await sleep(5000);
    }
    
    return fallback ?? null;
  }
}

// Usage
const messages = await safeExecute(
  () => discord-py-self_read_messages({ channel_id: "123", limit: 10 }),
  [] // fallback to empty array
);
```

### 9. Configuration Management

**Environment-based config:**
```typescript
// config.ts
import { z } from "zod";

const configSchema = z.object({
  DISCORD_TOKEN: z.string().optional(), // For official bots
  COMMAND_PREFIX: z.string().default("!"),
  ADMIN_ROLE_IDS: z.string().transform(s => s.split(",")),
  WELCOME_CHANNEL_ID: z.string().optional(),
  LOG_CHANNEL_ID: z.string().optional(),
  AUTO_MOD_ENABLED: z.coerce.boolean().default(false),
});

export const config = configSchema.parse(process.env);
```

### 10. Logging & Monitoring

**Structured logging:**
```typescript
// utils/logger.ts
export async function logAction(
  action: string,
  details: Record<string, any>,
  guildId: string
) {
  const logChannel = config.LOG_CHANNEL_ID;
  if (!logChannel) return;
  
  const embed = {
    title: action,
    fields: Object.entries(details).map(([key, value]) => ({
      name: key,
      value: String(value),
      inline: true
    })),
    timestamp: new Date().toISOString(),
    color: 0x00ff00
  };
  
  await discord-py-self_send_message({
    channel_id: logChannel,
    content: JSON.stringify({ embeds: [embed] })
  });
}

// Usage
await logAction("Member Kicked", {
  "User": member.username,
  "Moderator": moderator.username,
  "Reason": reason
}, guildId);
```

## Best Practices

1. **Respect Rate Limits** - Implement rate limiting to avoid bans
2. **Permission Checks** - Always verify permissions before actions
3. **Error Handling** - Gracefully handle all Discord API errors
4. **Logging** - Log important actions for audit trails
5. **Modular Design** - Separate commands, events, and utilities
6. **Configuration** - Use environment variables for secrets
7. **Testing** - Test in private servers before production
8. **Documentation** - Document all commands and features
9. **User Feedback** - Provide clear feedback for all actions
10. **ToS Compliance** - Follow Discord Terms of Service

## Common Use Cases

### Use Case 1: Moderation Bot
- Auto-delete spam/bad words
- Warn/kick/ban commands
- Raid protection
- Message logging

### Use Case 2: Utility Bot
- Server info commands
- User lookup
- Role management
- Channel organization

### Use Case 3: Notification Bot
- Monitor external APIs
- Post updates to channels
- Alert on specific events
- Scheduled announcements

### Use Case 4: Game/Fun Bot
- Mini-games
- Polls and voting
- Trivia
- Economy system

## Tools to Use

- `discord-py-self_*` - All discord-py-self MCP tools
- `bash` - Run bot processes
- `write` - Create bot files
- `read` - Read Discord bot code
- `edit` - Update bot configuration

## Example Session

```
User: "Create a Discord moderation bot"

Agent:
1. Creates bot structure with commands/events
2. Implements core commands:
   - !kick <user> <reason>
   - !ban <user> <reason>
   - !warn <user> <reason>
   - !mute <user> <duration>
3. Adds auto-moderation for bad words
4. Implements permission checks
5. Adds logging to mod-log channel
6. Provides setup instructions

User: "Add a welcome message feature"

Agent:
1. Creates onMemberJoin event handler
2. Sends welcome message to welcome channel
3. Auto-assigns "Member" role
4. Logs join to mod-log
5. Updates configuration for welcome channel ID
```

## Security Considerations

1. **Never commit tokens** - Use environment variables
2. **Validate all inputs** - Prevent injection attacks
3. **Limit command access** - Use permission system
4. **Rate limit user commands** - Prevent abuse
5. **Sanitize user content** - Before displaying/logging
6. **Use least privilege** - Only request needed permissions
7. **Monitor for abuse** - Log suspicious activity
8. **Regular updates** - Keep dependencies updated

## References

- [discord-py-self MCP Documentation](https://github.com/your-repo/discord-py-self-mcp)
- [Discord API Documentation](https://discord.com/developers/docs)
- [Discord.py Documentation](https://discordpy.readthedocs.io/)

## Notes

- discord-py-self is for personal automation only
- For public bots, use official Discord Bot API
- Test thoroughly in private servers
- Monitor rate limits carefully
- Keep bot code modular and maintainable