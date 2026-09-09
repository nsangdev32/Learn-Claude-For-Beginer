# Lab 04 — Hook định dạng và hook chặn

> Sau bài [Nâng cao 01](../../docs/03-nang-cao/01-hooks.md) · ~60 phút

## Mục tiêu

Viết hai hook: một cái dọn dẹp sau khi Claude sửa file, một cái chặn hành động
nguy hiểm trước khi nó xảy ra.

## Chuẩn bị

Cần `jq`. Kiểm tra: `jq --version`.

## Phần A — Hook định dạng

### 1. Script

`.claude/hooks/format.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

file=$(jq -r '.tool_input.file_path // empty')
[ -z "$file" ] && exit 0
[ -f "$file" ] || exit 0

case "$file" in
  *.ts|*.tsx|*.js|*.jsx|*.json|*.md)
    npx --no-install prettier --write "$file" >/dev/null 2>&1 || true
    ;;
  *.py)
    ruff format "$file" >/dev/null 2>&1 || true
    ;;
esac

exit 0
```

```bash
chmod +x .claude/hooks/format.sh
```

Đổi công cụ format cho khớp dự án của bạn.

### 2. Đăng ký

`.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/format.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### 3. Thử

Nhờ Claude sửa một file với định dạng cố tình xấu. Kiểm tra file sau khi sửa —
nó phải đã được format.

Không chạy? `claude --debug` và tìm dòng log về hook.

## Phần B — Hook chặn

### 1. Script

`.claude/hooks/guard.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

cmd=$(jq -r '.tool_input.command // ""')

deny() {
  jq -n --arg reason "$1" '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: $reason
    }
  }'
  exit 0
}

case "$cmd" in
  *"git push --force"*|*"git push -f"*)
    deny "Force push bị chặn bởi hook của dự án." ;;
  *"rm -rf /"*)
    deny "Lệnh xoá nguy hiểm bị chặn." ;;
esac

exit 0
```

```bash
chmod +x .claude/hooks/guard.sh
```

### 2. Đăng ký

Thêm vào `hooks` trong `.claude/settings.json`:

```json
"PreToolUse": [
  {
    "matcher": "Bash",
    "hooks": [
      {
        "type": "command",
        "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/guard.sh",
        "timeout": 10
      }
    ]
  }
]
```

### 3. Thử

```text
chạy lệnh: git push --force origin main
```

Claude phải bị chặn và nhận đúng lý do bạn viết.

### 4. So sánh hai cách chặn

Thay script bằng cách dùng mã thoát:

```bash
echo "Force push bị chặn bởi hook của dự án." >&2
exit 2
```

Cả hai đều chặn. Ghi nhận khác biệt về output bạn nhìn thấy.

## Phần C — Hook `SessionStart`

Viết hook in ra nhánh git hiện tại và số file đang thay đổi, để mỗi phiên bắt
đầu bạn đều biết mình đang đứng ở đâu.

## Tiêu chí hoàn thành

- [ ] Hook format chạy tự động sau mỗi `Write`/`Edit`.
- [ ] Hook chặn ngăn được `git push --force` kèm lý do rõ ràng.
- [ ] Đã thử cả hai cách: JSON output và `exit 2`.
- [ ] Có hook `SessionStart` in trạng thái git.
- [ ] Đọc được log hook trong `claude --debug`.

## Câu hỏi suy ngẫm

- Hook này khác gì `permissions.deny` với `Bash(git push --force *)`?
  Trường hợp nào hook làm được mà permission rule không?
- Điều gì xảy ra nếu hook của bạn chậm 5 giây và khớp `*`?
- Vì sao không nên `eval` nội dung do model sinh ra trong hook?
