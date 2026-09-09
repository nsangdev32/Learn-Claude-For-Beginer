# 01 — Hooks

> Cấp độ: Nâng cao · Thời lượng: ~60 phút · Lab: [lab-04](../../labs/lab-04-hook-dinh-dang/README.md)

Hook là lệnh shell chạy tại các mốc cố định trong vòng đời phiên. Khác với
`CLAUDE.md` vốn chỉ là gợi ý, hook **luôn chạy** bất kể Claude quyết định gì.

## Mục tiêu

- Chọn đúng sự kiện cho việc bạn cần.
- Viết hook chặn được một hành động.
- Đọc được input JSON và trả về output đúng chuẩn.

## 1. Khi nào cần hook

Câu hỏi để tự kiểm tra: *"Việc này có được phép không xảy ra không?"*

- "Nên chạy lint sau khi sửa file" → CLAUDE.md là đủ.
- "**Phải** chạy lint sau mỗi lần sửa file" → hook.
- "Không được đọc file bí mật" → `permissions.deny`.
- "Không được chạy `rm -rf` ngoài thư mục build" → hook `PreToolUse`.

## 2. Các sự kiện

| Nhóm | Sự kiện |
| --- | --- |
| Vòng đời phiên | `SessionStart`, `Setup`, `SessionEnd` |
| Theo lượt | `UserPromptSubmit`, `UserPromptExpansion`, `Stop`, `StopFailure` |
| Thực thi tool | `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PostToolBatch`, `PermissionRequest`, `PermissionDenied` |
| Agent / task | `SubagentStart`, `SubagentStop`, `TaskCreated`, `TaskCompleted`, `TeammateIdle` |
| File / cấu hình | `FileChanged`, `ConfigChange`, `CwdChanged`, `DirectoryAdded`, `InstructionsLoaded`, `WorktreeCreate`, `WorktreeRemove` |
| Context | `PreCompact`, `PostCompact`, `PreModelSwitch`, `PostModelSwitch` |
| Hiển thị | `MessageDisplay`, `Notification`, `Elicitation`, `ElicitationResult` |

Bốn cái dùng nhiều nhất: `PreToolUse` (chặn), `PostToolUse` (dọn dẹp sau),
`UserPromptSubmit` (bổ sung context), `SessionStart` (chuẩn bị môi trường).

## 3. Cấu hình

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs -r npx prettier --write",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

Đặt trong `.claude/settings.json` (chia sẻ) hoặc `~/.claude/settings.json`
(cá nhân). Trong plugin thì đặt ở `hooks/hooks.json` với cùng định dạng.

Ngoài `type: "command"` còn có `http`, `mcp_tool`, `prompt`, `agent`.

## 4. Matcher

| Dạng | Cách hiểu | Ví dụ |
| --- | --- | --- |
| `"*"`, `""`, bỏ trống | Khớp tất cả | |
| Chữ, số, `_`, `-`, dấu cách, `\|`, `,` | So khớp chuỗi hoặc danh sách | `"Bash"`, `"Edit\|Write"` |
| Ký tự khác | Regex không neo | `"^Notebook"`, `"mcp__.*"` |

Matcher khớp với `tool_name` cho sự kiện tool. Với `SessionStart` thì khớp
`startup`/`resume`/`clear`/`compact`/`fork`; với `SubagentStart` thì khớp tên agent.

## 5. Input hook nhận được

Hook `command` nhận JSON qua **stdin**:

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/dir",
  "permission_mode": "acceptEdits",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": { "command": "npm test" },
  "tool_use_id": "toolu_01ABC..."
}
```

Trường thay đổi theo sự kiện: `UserPromptSubmit` có `user_prompt`,
`SessionStart` có `model` và `started_by`, `Stop` có `last_assistant_message`,
`FileChanged` có `file_path`.

## 6. Output: hai cách kiểm soát

**Cách 1 — mã thoát:**

| Mã | Ý nghĩa |
| --- | --- |
| `0` | Thành công. Nếu stdout là JSON hợp lệ thì đọc quyết định từ đó |
| `2` | **Chặn.** stderr được đưa cho Claude làm lý do |
| Khác | Lỗi không chặn, hành động vẫn tiếp tục |

```bash
#!/usr/bin/env bash
echo "Lệnh xoá nguy hiểm bị chặn" >&2
exit 2
```

**Cách 2 — JSON qua stdout, exit 0:**

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Chỉ được xoá trong thư mục build/"
  }
}
```

Các trường hữu ích khác:

| Trường | Tác dụng |
| --- | --- |
| `permissionDecision` | `"allow"` hoặc `"deny"` |
| `additionalContext` | Thêm thông tin vào context cho Claude |
| `updatedInput` | Sửa input của tool trước khi chạy |
| `systemMessage` | Ghi chú nội bộ cho Claude |
| `retry` | Với `PermissionDenied`: cho phép thử lại |

## 7. Ví dụ hoàn chỉnh: chặn `rm -rf` ngoài `build/`

`.claude/hooks/guard-rm.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

input=$(cat)
cmd=$(printf '%s' "$input" | jq -r '.tool_input.command // ""')

if printf '%s' "$cmd" | grep -qE '\brm\s+(-[a-zA-Z]*\s+)*-?[a-zA-Z]*r'; then
  if ! printf '%s' "$cmd" | grep -qE '(^|\s)(\./)?build/'; then
    jq -n '{
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "deny",
        permissionDecisionReason: "Chỉ cho phép xoá đệ quy bên trong build/"
      }
    }'
    exit 0
  fi
fi
exit 0
```

`.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/guard-rm.sh",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

Nhớ `chmod +x`.

## 8. Gỡ lỗi

```bash
claude --debug
```

Log ghi lại hook nào khớp, mã thoát và output của chúng. Vài lỗi hay gặp:

| Triệu chứng | Nguyên nhân thường gặp |
| --- | --- |
| Hook không chạy | Chưa `chmod +x`, hoặc thư mục chưa được tin tưởng |
| Hook chạy nhưng không chặn | Trả mã 1 thay vì 2, hoặc JSON sai schema |
| Chặn nhầm mọi thứ | Matcher regex quá rộng |
| Phiên chậm hẳn | Hook nặng chạy trên `PostToolUse` khớp `*` |

Tắt toàn bộ hook để khoanh vùng: `"disableAllHooks": true`, hoặc `claude --safe-mode`.

## 9. An toàn

Hook chạy **lệnh shell tuỳ ý** với quyền của bạn. Vì thế:

- Hook trong settings của dự án chỉ chạy sau khi bạn tin tưởng thư mục đó.
- Đọc kỹ `.claude/settings.json` và `hooks/` của repo lạ trước khi bấm tin tưởng.
- Đừng nội suy nội dung do model sinh ra thẳng vào lệnh shell. Dùng `jq -r` và
  truyền qua `xargs` thay vì `eval`.

## Bài tập

1. Viết hook `PostToolUse` chạy formatter sau mỗi lần `Write` hoặc `Edit`.
2. Viết hook `PreToolUse` chặn `git push` và trả lý do rõ ràng.
3. Viết hook `SessionStart` in ra nhánh git và trạng thái working tree.

Làm đầy đủ ở [lab-04](../../labs/lab-04-hook-dinh-dang/README.md).

## Kiểm tra hiểu bài

- Mã thoát nào chặn hành động, và Claude nhận lý do từ đâu?
- Hook khác `permissions.deny` ở chỗ nào? Khi nào dùng cái nào?
- Vì sao hook trong settings của dự án cần workspace trust?

---

Tiếp: [02 — Plugins](02-plugins.md)
