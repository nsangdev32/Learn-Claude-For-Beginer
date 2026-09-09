# Cheatsheet

Bản tra nhanh. Chi tiết nằm ở các bài học tương ứng.

## Shell

```bash
claude                          # phiên tương tác
claude "task"                   # phiên tương tác kèm prompt đầu
claude -p "query"               # headless, chạy xong thoát
claude -c                       # tiếp tục hội thoại gần nhất
claude -r "<phiên>" "query"     # khôi phục phiên
claude --bg "task"              # chạy nền
claude doctor                   # chẩn đoán cấu hình
claude --safe-mode              # tắt mọi tuỳ biến
claude --debug                  # log chi tiết
```

## Cờ hay dùng

```bash
--model <alias|id>              # sonnet | opus | haiku | fable | ID đầy đủ
--effort low|medium|high|xhigh|max
--permission-mode default|acceptEdits|plan|auto|dontAsk|bypassPermissions
--allowedTools "Read" "Bash(npm run *)"
--disallowedTools "Bash(git push *)"
--max-turns 5
--max-budget-usd 2.00
--output-format text|json|stream-json
--add-dir ../shared-lib
--plugin-dir ./my-plugin
--agent <ten-agent>
--append-system-prompt "..."
```

## Lệnh trong phiên

| Lệnh | Việc |
| --- | --- |
| `/help` | Danh sách lệnh |
| `/context` | Xem context đang dùng |
| `/compact [ghi chú]` | Tóm tắt hội thoại |
| `/clear` | Bắt đầu lại |
| `/diff` | Xem thay đổi |
| `/code-review [mức] [--fix]` | Rà lỗi trong diff |
| `/plan` | Vào plan mode |
| `/model`, `/effort` | Đổi model, mức suy luận |
| `/memory` | Sửa file bộ nhớ |
| `/init` | Sinh CLAUDE.md |
| `/permissions` | Quản lý quyền |
| `/mcp` | Quản lý MCP server |
| `/doctor` | Chẩn đoán |
| `/branch`, `/fork` | Rẽ nhánh hội thoại |
| `/btw` | Hỏi ngoài lề |

## Phím tắt

| Phím | Việc |
| --- | --- |
| `Shift+Tab` | Đổi permission mode |
| `Esc` | Ngắt Claude |
| `↑` | Lịch sử |
| `Tab` | Tự hoàn thành |
| `Ctrl+D` ×2 | Thoát |

## Vị trí file

```
~/.claude/CLAUDE.md              # hướng dẫn cá nhân, mọi dự án
~/.claude/settings.json          # settings cá nhân
~/.claude/skills/<ten>/SKILL.md  # skill cá nhân
~/.claude/agents/<ten>.md        # subagent cá nhân
~/.claude/rules/*.md             # rule cá nhân

./CLAUDE.md                      # hướng dẫn dự án (commit)
./CLAUDE.local.md                # hướng dẫn riêng bạn (gitignore)
./.claude/settings.json          # settings nhóm (commit)
./.claude/settings.local.json    # settings riêng bạn (gitignore)
./.claude/rules/*.md             # rule dự án
./.claude/skills/<ten>/SKILL.md  # skill dự án
./.claude/agents/<ten>.md        # subagent dự án
./.mcp.json                      # MCP server dự án (commit, không kèm token)
```

## Permission rules

```json
{
  "permissions": {
    "allow": ["Bash(npm run *)", "Read"],
    "ask":   ["Bash(docker *)"],
    "deny":  ["Bash(git push *)", "Read(./.env)"],
    "defaultMode": "acceptEdits",
    "additionalDirectories": ["../shared"]
  }
}
```

Wildcard: `Bash(git log *)` khớp `git log --oneline`, không khớp `git push`.
`Bash(git *)` khớp **mọi** lệnh git. `Bash(ls *)` khớp cả `ls` trần, không khớp
`lsof`. `Bash(ls*)` khớp cả `lsof`.

MCP: `mcp__<server>__<tool>`. Subagent: `Agent(<Ten>)`.

## Skill

```markdown
---
name: ten-skill
description: Khi nào dùng. Luôn nằm trong context, viết ngắn.
disable-model-invocation: true
allowed-tools: Bash(git add *) Bash(git commit *)
argument-hint: [issue-number]
---

Nội dung, chỉ nạp khi được gọi.

!`git diff HEAD`

Tham số: $ARGUMENTS, hoặc $0 $1 $2 theo vị trí.
```

## Subagent

```markdown
---
name: ten-agent
description: Khi nào giao việc cho agent này.
tools: Read, Grep, Glob
model: sonnet
memory: project
---

System prompt, chỉ nạp khi agent chạy.
```

## Hook

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{ "type": "command", "command": "./format.sh", "timeout": 30 }]
      }
    ]
  }
}
```

Mã thoát: `0` ok, `2` **chặn** (stderr là lý do), khác = lỗi không chặn.

Output JSON, exit 0:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "..."
  }
}
```

## MCP

```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
claude mcp add --transport stdio db --scope project -- npx -y some-server
claude mcp list
claude mcp remove notion
```

## Cây quyết định

```
Sự thật đúng ở mọi phiên            → CLAUDE.md
Luật chỉ cho một số file            → .claude/rules/ có paths
Quy trình nhiều bước, lặp lại       → Skill
Việc ngốn context, chỉ cần kết luận → Subagent
Bắt buộc phải chạy, không được lách → Hook
Cấm tuyệt đối                       → permissions.deny
Chia sẻ cho nhóm/cộng đồng          → Plugin
Chạy trong pipeline                 → claude -p
Nhúng vào ứng dụng                  → Agent SDK
```
