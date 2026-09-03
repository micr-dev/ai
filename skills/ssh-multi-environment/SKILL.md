# SSH Multi-Environment Management Skill

## Triggers

Use this skill when the user asks to:
- "SSH into my NAS/EC2/server"
- "Run this command on the remote server"
- "Copy files to/from the server"
- "Set up SSH config for..."
- "Manage multiple SSH environments"
- "Forward port from remote server"
- "Check what's running on my server"
- "Deploy to production/staging"
- "Sync files between local and remote"
- "Execute remote commands"
- "Manage SSH keys"
- "Set up persistent remote session"

## Overview

This skill provides systematic workflows for managing multiple SSH environments (NAS, EC2, local-dev, production servers, etc.) with:
- Environment-aware SSH configuration
- Secure key management
- Efficient file transfer patterns
- Remote command execution
- Port forwarding for development
- Persistent session management with tmux
- Environment-specific workflows

**Key Philosophy**: Use SSH config for environment abstraction; use tmux for persistent remote sessions; use rsync for efficient file sync.

## Workflow

### Phase 1: Environment Setup

**Step 1: Configure SSH config**

Create/update `~/.ssh/config` with environment definitions:

```ssh-config
# NAS Environment
Host nas
    HostName 192.168.1.100
    User admin
    Port 22
    IdentityFile ~/.ssh/nas_key
    ServerAliveInterval 60
    ServerAliveCountMax 3

# EC2 Production
Host ec2-prod
    HostName ec2-xx-xxx-xxx-xx.compute.amazonaws.com
    User ubuntu
    Port 22
    IdentityFile ~/.ssh/ec2_prod.pem
    ServerAliveInterval 60
    StrictHostKeyChecking no
    UserKnownHostsFile=/dev/null

# Local Dev Server
Host local-dev
    HostName 192.168.1.50
    User developer
    Port 22
    IdentityFile ~/.ssh/id_rsa
    ForwardAgent yes

# Staging Server
Host staging
    HostName staging.example.com
    User deploy
    Port 2222
    IdentityFile ~/.ssh/staging_key
    ProxyJump bastion

# Bastion/Jump Host
Host bastion
    HostName bastion.example.com
    User admin
    Port 22
    IdentityFile ~/.ssh/bastion_key
```

**Step 2: Verify SSH key permissions**

```bash
# Keys must be readable only by owner
chmod 600 ~/.ssh/nas_key
chmod 600 ~/.ssh/ec2_prod.pem
chmod 600 ~/.ssh/staging_key

# SSH config should be secure
chmod 600 ~/.ssh/config

# Known hosts should be writable
chmod 644 ~/.ssh/known_hosts
```

**Step 3: Test connections**

```bash
# Test each environment
ssh nas "echo 'NAS connection OK'"
ssh ec2-prod "echo 'EC2 connection OK'"
ssh local-dev "echo 'Local-dev connection OK'"

# Test with verbose output if issues
ssh -v nas
```

### Phase 2: Remote Command Execution

**Pattern 1: Single command**

```bash
# Execute single command
ssh nas "df -h"
ssh ec2-prod "systemctl status nginx"
ssh local-dev "docker ps"

# With sudo (if configured)
ssh nas "sudo systemctl restart service"

# Capture output
DISK_USAGE=$(ssh nas "df -h /data | tail -1 | awk '{print \$5}'")
echo "NAS disk usage: $DISK_USAGE"
```

**Pattern 2: Multiple commands**

```bash
# Sequential commands
ssh nas "cd /data && ls -la && du -sh *"

# With heredoc for complex scripts
ssh nas 'bash -s' << 'EOF'
cd /data
for dir in */; do
    echo "Size of $dir:"
    du -sh "$dir"
done
EOF
```

**Pattern 3: Interactive session**

```bash
# Start interactive shell
ssh nas

# Or with specific command
ssh nas -t "cd /data && bash"
```

### Phase 3: File Transfer

**Pattern 1: SCP for simple transfers**

```bash
# Copy file to remote
scp local-file.txt nas:/data/

# Copy file from remote
scp nas:/data/remote-file.txt ./

# Copy directory recursively
scp -r local-dir/ nas:/data/

# Copy with specific port
scp -P 2222 file.txt staging:/app/
```

**Pattern 2: Rsync for efficient sync**

```bash
# Sync directory to remote (dry-run first)
rsync -avz --dry-run ./local-dir/ nas:/data/backup/
rsync -avz ./local-dir/ nas:/data/backup/

# Sync from remote to local
rsync -avz nas:/data/backup/ ./local-backup/

# Sync with delete (mirror)
rsync -avz --delete ./local-dir/ nas:/data/backup/

# Sync with exclusions
rsync -avz --exclude 'node_modules' --exclude '.git' \
    ./project/ ec2-prod:/var/www/app/

# Sync with progress
rsync -avz --progress ./large-file.zip nas:/data/

# Sync over SSH with specific config
rsync -avz -e "ssh -p 2222" ./dir/ staging:/app/
```

**Pattern 3: Tar + SSH for compression**

```bash
# Compress and transfer
tar czf - ./directory | ssh nas "cat > /data/backup.tar.gz"

# Transfer and extract
tar czf - ./directory | ssh nas "cd /data && tar xzf -"

# Transfer from remote
ssh nas "tar czf - /data/directory" | tar xzf -
```

### Phase 4: Port Forwarding

**Pattern 1: Local port forwarding**

```bash
# Forward remote port to local
# Access remote service at localhost:8080
ssh -L 8080:localhost:80 nas

# Forward remote database
ssh -L 5432:localhost:5432 ec2-prod
# Now connect to localhost:5432 to reach remote PostgreSQL

# Forward with background process
ssh -f -N -L 8080:localhost:80 nas
# -f: background, -N: no command execution
```

**Pattern 2: Remote port forwarding**

```bash
# Forward local port to remote
# Remote can access local service
ssh -R 8080:localhost:3000 nas

# Useful for webhooks during development
ssh -R 9000:localhost:9000 ec2-prod
```

**Pattern 3: Dynamic port forwarding (SOCKS proxy)**

```bash
# Create SOCKS proxy
ssh -D 1080 nas

# Configure browser to use localhost:1080 as SOCKS proxy
# All traffic routes through NAS
```

### Phase 5: Persistent Sessions with Tmux

**Pattern 1: Start remote tmux session**

```bash
# SSH and start tmux
ssh nas -t "tmux new -s work"

# Or attach to existing
ssh nas -t "tmux attach -t work"

# List remote sessions
ssh nas "tmux ls"
```

**Pattern 2: Long-running tasks**

```bash
# Start task in tmux on remote
ssh nas -t "tmux new -s backup 'cd /data && ./backup-script.sh'"

# Detach and let it run (Ctrl+B, D)
# Later, reattach to check progress
ssh nas -t "tmux attach -t backup"
```

**Pattern 3: Multiple windows**

```bash
# Create session with multiple windows
ssh nas -t 'tmux new -s dev \; \
    new-window -n logs "tail -f /var/log/app.log" \; \
    new-window -n monitor "htop" \; \
    select-window -t 0'
```

### Phase 6: Environment-Specific Workflows

**Workflow 1: Deploy to production**

```bash
# 1. Build locally
npm run build

# 2. Sync to remote
rsync -avz --delete \
    --exclude 'node_modules' \
    --exclude '.env.local' \
    ./dist/ ec2-prod:/var/www/app/

# 3. Restart service
ssh ec2-prod "sudo systemctl restart app"

# 4. Verify
ssh ec2-prod "curl -s http://localhost:3000/health"
```

**Workflow 2: Backup from NAS**

```bash
# 1. Create remote backup
ssh nas "cd /data && tar czf backup-$(date +%Y%m%d).tar.gz important-files/"

# 2. Transfer to local
scp nas:/data/backup-$(date +%Y%m%d).tar.gz ./backups/

# 3. Verify integrity
tar tzf ./backups/backup-$(date +%Y%m%d).tar.gz > /dev/null && echo "Backup OK"

# 4. Clean up old remote backups
ssh nas "find /data -name 'backup-*.tar.gz' -mtime +30 -delete"
```

**Workflow 3: Monitor remote services**

```bash
# Check service status across environments
for host in nas ec2-prod local-dev; do
    echo "=== $host ==="
    ssh $host "systemctl status nginx | head -3"
done

# Check disk usage
for host in nas ec2-prod; do
    echo "=== $host disk usage ==="
    ssh $host "df -h | grep -E '^/dev/'"
done

# Check running containers
ssh ec2-prod "docker ps --format 'table {{.Names}}\t{{.Status}}'"
```

**Workflow 4: Database operations**

```bash
# Forward database port
ssh -f -N -L 5432:localhost:5432 ec2-prod

# Dump remote database
ssh ec2-prod "pg_dump -U postgres mydb" > backup.sql

# Restore to local
psql -U postgres -d mydb < backup.sql

# Or dump and restore in one command
ssh ec2-prod "pg_dump -U postgres mydb" | psql -U postgres -d mydb_local
```

## Best Practices

### SSH Config Management

1. **Use descriptive host aliases**: `nas`, `ec2-prod`, `staging` instead of IPs
2. **Set ServerAliveInterval**: Prevents connection timeouts
3. **Use IdentityFile per host**: Separate keys for different environments
4. **Enable ForwardAgent carefully**: Only for trusted hosts
5. **Use ProxyJump for bastion hosts**: Cleaner than manual tunneling

### Key Management

1. **One key per environment**: Don't reuse keys across environments
2. **Secure permissions**: `chmod 600` for private keys
3. **Use ssh-agent**: Avoid typing passphrases repeatedly
4. **Rotate keys regularly**: Especially for production
5. **Use ed25519 keys**: More secure than RSA

```bash
# Generate new key
ssh-keygen -t ed25519 -C "nas-key" -f ~/.ssh/nas_key

# Add to ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/nas_key

# Copy public key to remote
ssh-copy-id -i ~/.ssh/nas_key.pub admin@192.168.1.100
```

### File Transfer Optimization

1. **Use rsync over scp**: More efficient, resumable
2. **Dry-run first**: `--dry-run` to preview changes
3. **Exclude unnecessary files**: `--exclude 'node_modules'`
4. **Use compression**: `-z` flag for slow connections
5. **Show progress**: `--progress` for large transfers

### Security Practices

1. **Disable password auth**: Use keys only
2. **Change default SSH port**: Reduces automated attacks
3. **Use fail2ban**: Block brute-force attempts
4. **Limit SSH access**: Firewall rules, IP whitelisting
5. **Audit SSH logs**: Monitor `/var/log/auth.log`

### Session Management

1. **Use tmux for long tasks**: Survives disconnections
2. **Name sessions descriptively**: `tmux new -s backup`
3. **Use tmux windows**: Organize related tasks
4. **Detach, don't kill**: Preserve running processes
5. **Clean up old sessions**: `tmux kill-session -t old`

## Tools to Use

### Core SSH Tools
- **ssh**: Remote shell access
- **scp**: Simple file copy
- **rsync**: Efficient file synchronization
- **ssh-keygen**: Generate SSH keys
- **ssh-copy-id**: Install public keys on remote
- **ssh-agent**: Manage key passphrases

### Session Management
- **tmux**: Terminal multiplexer (preferred)
- **screen**: Alternative to tmux
- **mosh**: Mobile shell (survives network changes)

### Monitoring and Debugging
- **ssh -v**: Verbose connection debugging
- **ssh -vvv**: Very verbose debugging
- **netstat**: Check port forwarding
- **lsof**: Check open SSH connections

### File Transfer Alternatives
- **tar + ssh**: Compressed streaming
- **nc (netcat)**: Raw data transfer
- **sftp**: Interactive file transfer

## Example Sessions

### Example 1: Deploy Application

**User request**: "Deploy the app to production"

```bash
# Step 1: Build locally
npm run build

# Step 2: Backup current production
ssh ec2-prod "cd /var/www/app && tar czf ../app-backup-$(date +%Y%m%d-%H%M).tar.gz ."

# Step 3: Sync new build
rsync -avz --delete \
    --exclude '.env' \
    --exclude 'node_modules' \
    ./dist/ ec2-prod:/var/www/app/

# Step 4: Install dependencies (if needed)
ssh ec2-prod "cd /var/www/app && npm ci --production"

# Step 5: Restart service
ssh ec2-prod "sudo systemctl restart app"

# Step 6: Verify deployment
sleep 5
ssh ec2-prod "curl -s http://localhost:3000/health | jq '.status'"

# Step 7: Check logs
ssh ec2-prod "journalctl -u app -n 20 --no-pager"
```

### Example 2: Database Maintenance

**User request**: "Backup production database and restore to staging"

```bash
# Step 1: Dump production database
ssh ec2-prod "pg_dump -U postgres -Fc production_db" > prod_backup.dump

# Step 2: Copy to staging
scp prod_backup.dump staging:/tmp/

# Step 3: Restore on staging
ssh staging "pg_restore -U postgres -d staging_db -c /tmp/prod_backup.dump"

# Step 4: Verify
ssh staging "psql -U postgres -d staging_db -c 'SELECT COUNT(*) FROM users;'"

# Step 5: Clean up
rm prod_backup.dump
ssh staging "rm /tmp/prod_backup.dump"
```

### Example 3: Monitor Multiple Servers

**User request**: "Check status of all servers"

```bash
# Create monitoring script
cat > check_servers.sh << 'EOF'
#!/bin/bash

HOSTS="nas ec2-prod local-dev staging"

echo "=== Server Status Report ==="
echo "Generated: $(date)"
echo

for host in $HOSTS; do
    echo "--- $host ---"
    
    # Check connectivity
    if ssh -o ConnectTimeout=5 $host "echo 'OK'" &>/dev/null; then
        echo "✓ Connection: OK"
        
        # Uptime
        uptime=$(ssh $host "uptime -p")
        echo "  Uptime: $uptime"
        
        # Disk usage
        disk=$(ssh $host "df -h / | tail -1 | awk '{print \$5}'")
        echo "  Disk: $disk used"
        
        # Memory
        mem=$(ssh $host "free -h | grep Mem | awk '{print \$3\"/\"\$2}'")
        echo "  Memory: $mem"
        
        # Load average
        load=$(ssh $host "uptime | awk -F'load average:' '{print \$2}'")
        echo "  Load:$load"
    else
        echo "✗ Connection: FAILED"
    fi
    echo
done
EOF

chmod +x check_servers.sh
./check_servers.sh
```

### Example 4: Development Workflow

**User request**: "Set up remote development environment"

```bash
# Step 1: Forward ports for development
ssh -f -N -L 3000:localhost:3000 local-dev  # App
ssh -f -N -L 5432:localhost:5432 local-dev  # Database
ssh -f -N -L 6379:localhost:6379 local-dev  # Redis

# Step 2: Start remote tmux session
ssh local-dev -t "tmux new -s dev"

# Step 3: In tmux, start services
# Window 0: App
cd /app && npm run dev

# Window 1: Logs (Ctrl+B, C to create new window)
tail -f /var/log/app.log

# Window 2: Database console
psql -U postgres -d mydb

# Step 4: Detach (Ctrl+B, D) and work locally
# App accessible at localhost:3000
# Database at localhost:5432

# Step 5: Sync code changes
# In local terminal, watch for changes and sync
fswatch -o ./src | xargs -n1 -I{} rsync -avz ./src/ local-dev:/app/src/

# Step 6: Reattach to check logs
ssh local-dev -t "tmux attach -t dev"
```

## Notes

### Common SSH Config Options

```ssh-config
# Connection keepalive
ServerAliveInterval 60
ServerAliveCountMax 3

# Disable strict host checking (dev only)
StrictHostKeyChecking no
UserKnownHostsFile=/dev/null

# Enable agent forwarding
ForwardAgent yes

# Compression for slow connections
Compression yes

# Reuse connections (faster)
ControlMaster auto
ControlPath ~/.ssh/control-%r@%h:%p
ControlPersist 10m

# Jump through bastion
ProxyJump bastion

# Custom identity file
IdentityFile ~/.ssh/custom_key

# Specific port
Port 2222
```

### Troubleshooting

**Connection refused:**
```bash
# Check if SSH service running
ssh -v host  # Look for connection errors

# Check firewall
ssh host "sudo ufw status"

# Check SSH service
ssh host "sudo systemctl status sshd"
```

**Permission denied:**
```bash
# Check key permissions
ls -la ~/.ssh/

# Check remote authorized_keys
ssh host "ls -la ~/.ssh/authorized_keys"

# Try with password (if enabled)
ssh -o PreferredAuthentications=password host
```

**Timeout issues:**
```bash
# Increase timeout
ssh -o ConnectTimeout=30 host

# Check network
ping host

# Try different port
ssh -p 2222 host
```

**Port forwarding not working:**
```bash
# Check if port already in use
lsof -i :8080

# Check remote service
ssh host "netstat -tlnp | grep :80"

# Try with verbose
ssh -v -L 8080:localhost:80 host
```

### Performance Tips

1. **Use ControlMaster**: Reuse SSH connections
2. **Enable compression**: For slow networks
3. **Use rsync**: More efficient than scp
4. **Batch commands**: Reduce connection overhead
5. **Use tmux**: Avoid reconnecting for each task

### Security Checklist

- [ ] SSH keys have correct permissions (600)
- [ ] Password authentication disabled on servers
- [ ] SSH running on non-standard port
- [ ] Firewall rules limit SSH access
- [ ] fail2ban installed and configured
- [ ] SSH logs monitored regularly
- [ ] Keys rotated periodically
- [ ] ForwardAgent only on trusted hosts
- [ ] Bastion host for production access
- [ ] Two-factor authentication enabled (if supported)

### Environment-Specific Notes

**NAS:**
- Often behind firewall, may need VPN
- Usually has limited resources
- Good for backups and file storage
- May have custom SSH port

**EC2:**
- Use .pem keys from AWS
- Security groups control access
- May need bastion/jump host
- Consider AWS Systems Manager Session Manager as alternative

**Local Dev:**
- Usually on same network
- Can use simpler authentication
- Good for testing before production
- May have Docker/containers running

**Staging:**
- Should mirror production setup
- Use separate keys from production
- Good for testing deployments
- May share bastion with production
