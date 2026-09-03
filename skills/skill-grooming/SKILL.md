# Skill Grooming & Audit

Comprehensive skill quality assessment and maintenance workflow for OpenCode agent skills.

## Triggers

Use this skill when the user mentions:
- "groom skills"
- "audit skills"
- "review skills"
- "check skill quality"
- "validate skills"
- "skill maintenance"
- "skill quality check"

## Overview

This skill provides a systematic approach to auditing and maintaining OpenCode agent skills, ensuring they meet quality standards and remain effective.

## Workflow

### 1. Discovery Phase

**Locate all skills:**
```bash
find ~/.config/opencode/skills -name "SKILL.md" -type f
```

**List skill directories:**
```bash
ls -la ~/.config/opencode/skills/
```

### 2. Quality Checklist

For each skill, verify:

#### A. File Structure
- [ ] SKILL.md exists and is readable
- [ ] Proper markdown formatting
- [ ] Clear section headers (Triggers, Overview, Workflow, etc.)

#### B. Trigger Phrases
- [ ] Triggers section exists
- [ ] At least 3-5 trigger phrases defined
- [ ] Triggers are specific and actionable
- [ ] Triggers cover common user phrasings
- [ ] No overly generic triggers (e.g., "help me")

#### C. Content Quality
- [ ] Clear overview/purpose statement
- [ ] Step-by-step workflow defined
- [ ] Code examples where applicable
- [ ] Tool usage patterns documented
- [ ] Error handling guidance included

#### D. Metadata (if present)
- [ ] metadata.json is valid JSON
- [ ] Contains name, description, version
- [ ] Tags are relevant and specific

#### E. Skill Pointer Validation (for category pointers)
- [ ] Points to valid skill library
- [ ] References are up-to-date
- [ ] No broken links

### 3. Audit Report Template

```markdown
# Skill Audit Report

**Date:** YYYY-MM-DD
**Total Skills:** N

## Summary

- ✅ Passing: N skills
- ⚠️  Warnings: N skills
- ❌ Failing: N skills

## Detailed Results

### Skill: [name]
**Status:** ✅ Pass / ⚠️ Warning / ❌ Fail

**Issues:**
- Issue 1
- Issue 2

**Recommendations:**
- Recommendation 1
- Recommendation 2

---

## Overall Recommendations

1. Priority fixes
2. Quality improvements
3. Documentation gaps
```

### 4. Common Issues & Fixes

#### Issue: Missing Triggers
**Fix:** Add comprehensive trigger phrases
```markdown
## Triggers

Use this skill when the user mentions:
- "primary trigger phrase"
- "alternative phrasing"
- "common variation"
- "related action"
```

#### Issue: Vague Workflow
**Fix:** Add specific, actionable steps
```markdown
## Workflow

### Step 1: [Action]
**What:** Clear description
**How:** Specific commands/tools
**Example:**
\`\`\`bash
command example
\`\`\`
```

#### Issue: No Code Examples
**Fix:** Add practical examples
```markdown
## Examples

### Example 1: [Scenario]
\`\`\`bash
# Command
tool --flag value
\`\`\`

**Expected output:**
\`\`\`
output example
\`\`\`
```

### 5. Batch Audit Script

Create a quick audit script:

```bash
#!/bin/bash
# skill-audit.sh

SKILLS_DIR="$HOME/.config/opencode/skills"
REPORT_FILE="skill-audit-$(date +%Y%m%d-%H%M%S).md"

echo "# Skill Audit Report" > "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "**Date:** $(date +%Y-%m-%d)" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

TOTAL=0
PASS=0
WARN=0
FAIL=0

for skill_dir in "$SKILLS_DIR"/*; do
  if [ -d "$skill_dir" ]; then
    TOTAL=$((TOTAL + 1))
    skill_name=$(basename "$skill_dir")
    skill_file="$skill_dir/SKILL.md"
    
    echo "## Skill: $skill_name" >> "$REPORT_FILE"
    
    if [ ! -f "$skill_file" ]; then
      echo "**Status:** ❌ FAIL - Missing SKILL.md" >> "$REPORT_FILE"
      FAIL=$((FAIL + 1))
    else
      # Check for triggers section
      if grep -q "## Triggers" "$skill_file"; then
        echo "**Status:** ✅ PASS" >> "$REPORT_FILE"
        PASS=$((PASS + 1))
      else
        echo "**Status:** ⚠️  WARNING - Missing Triggers section" >> "$REPORT_FILE"
        WARN=$((WARN + 1))
      fi
    fi
    
    echo "" >> "$REPORT_FILE"
  fi
done

# Summary at top
sed -i "4i\\
## Summary\\n\\
- ✅ Passing: $PASS skills\\n\\
- ⚠️  Warnings: $WARN skills\\n\\
- ❌ Failing: $FAIL skills\\n\\
- **Total:** $TOTAL skills\\n" "$REPORT_FILE"

echo "Audit complete: $REPORT_FILE"
```

### 6. Interactive Grooming

For each skill with issues:

1. **Read the skill:**
   ```bash
   cat ~/.config/opencode/skills/[skill-name]/SKILL.md
   ```

2. **Identify gaps** using the quality checklist

3. **Propose fixes** in chat before editing

4. **Apply fixes** with user approval

5. **Verify** the updated skill loads correctly

### 7. Skill Quality Scoring

Score each skill (0-100):

- **Triggers (25 points)**
  - 5+ specific triggers: 25 pts
  - 3-4 triggers: 15 pts
  - 1-2 triggers: 5 pts
  - No triggers: 0 pts

- **Workflow (30 points)**
  - Detailed step-by-step: 30 pts
  - Basic steps: 15 pts
  - Vague description: 5 pts
  - Missing: 0 pts

- **Examples (20 points)**
  - Multiple code examples: 20 pts
  - One example: 10 pts
  - No examples: 0 pts

- **Documentation (15 points)**
  - Comprehensive: 15 pts
  - Basic: 8 pts
  - Minimal: 3 pts
  - Missing: 0 pts

- **Metadata (10 points)**
  - Complete metadata: 10 pts
  - Partial: 5 pts
  - Missing: 0 pts

**Grade Scale:**
- 90-100: Excellent
- 75-89: Good
- 60-74: Acceptable
- Below 60: Needs improvement

## Tools to Use

- `read` - Read skill files
- `grep` - Search for patterns
- `glob` - Find skill files
- `edit` - Fix skill issues
- `bash` - Run audit scripts

## Output Format

Always provide:
1. Summary statistics (total, pass, warn, fail)
2. Detailed findings per skill
3. Prioritized recommendations
4. Offer to fix issues interactively

## Best Practices

1. **Batch audit first** - Get overview before diving deep
2. **Prioritize by usage** - Fix frequently-used skills first
3. **Test after changes** - Verify skill loads correctly
4. **Document patterns** - Note common issues for future reference
5. **Version control** - Suggest backing up before major changes

## Example Session

```
User: "Audit my skills"

Agent:
1. Runs batch audit script
2. Generates report showing:
   - 18 total skills
   - 12 passing
   - 4 warnings (missing examples)
   - 2 failing (no triggers)
3. Presents prioritized fix list
4. Offers to fix issues interactively

User: "Fix the failing ones"

Agent:
1. Reads failing skill files
2. Proposes trigger phrases based on skill content
3. Adds triggers with user approval
4. Verifies skills load correctly
5. Updates audit report
```

## Notes

- Run audits periodically (monthly recommended)
- Keep audit reports for tracking improvements
- Share common patterns in AGENTS.md
- Consider creating skill templates for consistency