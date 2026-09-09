# 02 — Plugins

> Cấp độ: Nâng cao · Thời lượng: ~40 phút

Plugin đóng gói skills, agents, hooks và MCP server thành một đơn vị có phiên
bản, cài đặt được, chia sẻ được.

## Mục tiêu

- Biết khi nào nên chuyển từ `.claude/` sang plugin.
- Tạo và chạy thử plugin cục bộ.
- Hiểu cấu trúc thư mục và lỗi bố cục thường gặp.

## 1. `.claude/` hay plugin?

| | Standalone `.claude/` | Plugin |
| --- | --- | --- |
| Tên skill | `/hello` | `/ten-plugin:hello` |
| Hợp cho | Việc cá nhân, tuỳ biến riêng dự án, thử nghiệm nhanh | Chia sẻ cho nhóm, phát hành có phiên bản, dùng lại nhiều dự án |

Cách làm khuyến nghị: bắt đầu ở `.claude/` cho nhanh, chuyển thành plugin khi
đã ổn định và cần chia sẻ.

## 2. Plugin tối thiểu

```
my-first-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── hello/
        └── SKILL.md
```

`.claude-plugin/plugin.json`:

```json
{
  "name": "my-first-plugin",
  "description": "Plugin chào hỏi để học cơ bản",
  "version": "1.0.0",
  "author": { "name": "Tên bạn" }
}
```

| Trường | Ý nghĩa |
| --- | --- |
| `name` | Định danh và **namespace** cho skill: `/my-first-plugin:hello` |
| `description` | Hiển thị trong trình quản lý plugin |
| `version` | Tuỳ chọn. Người dùng chỉ nhận cập nhật khi bạn tăng số này |
| `author` | Tuỳ chọn |

`skills/hello/SKILL.md`:

```markdown
---
description: Chào người dùng một cách thân thiện
disable-model-invocation: true
---

Chào người dùng và hỏi hôm nay bạn cần giúp gì.
```

## 3. Chạy thử

```bash
claude --plugin-dir ./my-first-plugin
```

Trong phiên: `/my-first-plugin:hello`. Sau khi sửa file, chạy `/reload-plugins`
để nạp lại mà không cần khởi động lại.

Nạp nhiều plugin cùng lúc bằng cách lặp cờ:

```bash
claude --plugin-dir ./plugin-one --plugin-dir ./plugin-two
```

Cờ này cũng nhận file `.zip`. Với archive đặt trên URL thì dùng `--plugin-url`.

## 4. Cấu trúc đầy đủ

| Thư mục | Chứa gì |
| --- | --- |
| `.claude-plugin/` | Chỉ `plugin.json` |
| `skills/` | Skill dạng `<tên>/SKILL.md` |
| `agents/` | Định nghĩa subagent |
| `hooks/hooks.json` | Hook |
| `.mcp.json` | Cấu hình MCP server |
| `.lsp.json` | Cấu hình LSP server |
| `monitors/monitors.json` | Monitor chạy nền |
| `bin/` | File thực thi, được thêm vào `PATH` khi plugin bật |
| `settings.json` | Settings mặc định khi plugin bật |

> **Lỗi bố cục phổ biến nhất:** đặt `skills/`, `agents/`, `hooks/` *bên trong*
> `.claude-plugin/`. Chỉ `plugin.json` nằm trong đó. Mọi thư mục khác nằm ở
> gốc plugin.

## 5. Chuyển cấu hình sẵn có thành plugin

```bash
mkdir -p my-plugin/.claude-plugin
cp -r .claude/skills my-plugin/
cp -r .claude/agents my-plugin/
mkdir my-plugin/hooks
```

Copy đối tượng `hooks` từ `.claude/settings.json` sang `my-plugin/hooks/hooks.json`
— định dạng giống hệt.

Sau khi chuyển, xoá bản gốc trong `.claude/` để tránh trùng lặp. Định nghĩa
agent ở `.claude/agents/` ghi đè agent cùng tên của plugin; còn skill của plugin
có namespace riêng nên cả hai cùng tồn tại.

## 6. Phân phối

```bash
claude plugin validate ./my-plugin           # kiểm tra trước khi phát hành
claude plugin validate ./my-plugin --strict  # coi cảnh báo là lỗi
```

Phát hành qua **marketplace**: một repo chứa `.claude-plugin/marketplace.json`.
Repo riêng tư dùng được cho plugin nội bộ.

Hai marketplace công khai của Anthropic:

- `claude-plugins-official` — do Anthropic tuyển chọn, tự đăng ký sẵn.
- `claude-community` — cộng đồng, thêm bằng
  `/plugin marketplace add anthropics/claude-plugins-community`.

## 7. Plugin trong thư mục skills

Không muốn gõ `--plugin-dir` mỗi lần:

```bash
claude plugin init my-tool
```

Tạo `~/.claude/skills/my-tool/` kèm `plugin.json` và `SKILL.md` mẫu. Phiên sau
nó tự nạp dưới tên `my-tool@skills-dir`.

## Bài tập

1. Tạo plugin có một skill và một subagent chỉ-đọc. Chạy thử bằng `--plugin-dir`.
2. Thêm một hook `PostToolUse` vào `hooks/hooks.json` của plugin và xác nhận nó chạy.
3. Chạy `claude plugin validate` và sửa hết cảnh báo.

## Kiểm tra hiểu bài

- Skill của plugin `deploy-tools` tên `staging` được gọi bằng lệnh gì?
- File nào được phép nằm trong `.claude-plugin/`?
- Lệnh nào nạp lại plugin sau khi sửa mà không cần khởi động lại?

---

Trước: [01 — Hooks](01-hooks.md) · Tiếp: [03 — Headless và CI](03-headless-va-ci.md)
