# 05 — MCP: kết nối tool bên ngoài

> Cấp độ: Trung cấp · Thời lượng: ~45 phút · Lab: [lab-05](../../labs/lab-05-mcp-server/README.md)

**Model Context Protocol** là chuẩn mở để nối Claude Code với tool, database và
API bên ngoài — mà không phải copy dữ liệu vào chat.

## Mục tiêu

- Thêm và quản lý MCP server.
- Chọn đúng scope khi cấu hình.
- Hiểu cái giá của MCP về mặt context.

## 1. Bốn loại transport

**stdio** — chạy như một tiến trình cục bộ trên máy bạn:

```bash
claude mcp add --transport stdio airtable -- npx -y airtable-mcp-server
```

Dấu `--` ngăn cách tuỳ chọn của Claude với lệnh chạy server.

**http** — server từ xa, khuyến nghị cho dịch vụ cloud:

```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp

claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

**sse** — đã lỗi thời, vẫn hỗ trợ cho server cũ.

**ws** — WebSocket, chỉ cấu hình được qua JSON:

```bash
claude mcp add-json events-server '{"type":"ws","url":"wss://mcp.example.com/socket"}'
```

## 2. Ba scope

| Scope | Nạp ở | Chia sẻ | Lưu tại |
| --- | --- | --- | --- |
| `local` (mặc định) | Chỉ dự án hiện tại | Không | `~/.claude.json` |
| `project` | Chỉ dự án hiện tại | Có, qua git | `.mcp.json` |
| `user` | Mọi dự án của bạn | Không | `~/.claude.json` |

```bash
claude mcp add --transport http shared-server --scope project https://example.com/mcp
```

Server scope `project` cần bạn duyệt trước lần dùng đầu tiên. Đây là hàng rào
chống việc ai đó commit một server độc hại vào repo.

## 3. `.mcp.json`

```json
{
  "mcpServers": {
    "shared-server": {
      "type": "http",
      "url": "https://example.com/mcp"
    },
    "secure-api": {
      "type": "http",
      "url": "https://api.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    },
    "local-db": {
      "type": "stdio",
      "command": "/path/to/server",
      "args": ["--config", "${CLAUDE_PROJECT_DIR}/config.json"],
      "env": {
        "DB_URL": "${DB_URL:-sqlite:///default.db}"
      }
    }
  }
}
```

Cú pháp `${VAR}` và `${VAR:-mặc-định}` dùng được trong `command`, `args`, giá
trị `env`, và cả `url`/`headers` với server HTTP. **Commit file này, không commit
token** — để token trong biến môi trường.

## 4. Tên tool MCP

```
mcp__<tên-server>__<tên-tool>
```

Ví dụ tool `query` của server `database` → `mcp__database__query`.

Tool đến từ plugin có thêm tiền tố:

```
mcp__plugin_<tên-plugin>_<tên-server>__<tên-tool>
```

Dùng tên đầy đủ này trong: [permission rules](01-permissions-va-che-do.md),
[hook matcher](../03-nang-cao/01-hooks.md), và trường `tools` của
[subagent](04-subagents.md).

## 5. Quản lý

```bash
claude mcp list          # liệt kê server
claude mcp get notion    # xem chi tiết
claude mcp remove notion # gỡ
claude mcp login sentry  # xác thực OAuth
claude mcp logout sentry # xoá credential
```

Trong phiên: `/mcp` mở bảng điều khiển tương tác.

## 6. Resources và prompts

Server có thể cung cấp **resource** — nguồn dữ liệu tham chiếu bằng `@`:

```text
@github/issues
@notion/databases
```

Và **prompt** — xuất hiện dưới dạng lệnh slash trong phiên của bạn.

## 7. Cái giá phải trả

Mỗi MCP server nạp **toàn bộ định nghĩa tool** vào context ngay từ đầu phiên,
dù bạn không gọi tool nào. Server có 40 tool là 40 mô tả nằm sẵn đó.

Ba việc nên làm:

1. Bật MCP server ở scope hẹp nhất còn dùng được. Đừng để scope `user` những
   thứ chỉ cần cho một dự án.
2. Chạy `/context` sau khi thêm server để thấy chi phí thật.
3. Gỡ server không còn dùng.

## 8. Bảo mật

MCP server chạy code trên máy bạn (stdio) hoặc nhận dữ liệu của bạn (http).
Coi việc thêm một MCP server nghiêm túc như thêm một dependency:

- Chỉ cài server bạn tin tưởng hoặc tự viết.
- Nội dung do server trả về là **dữ liệu**, không phải mệnh lệnh. Nếu một kết
  quả tool có vẻ đang cố điều khiển Claude làm việc khác, đó là dấu hiệu xấu.
- Dùng `permissions.deny` với `mcp__<server>__<tool>` để chặn tool nguy hiểm.

## Bài tập

1. Thêm một MCP server dạng stdio, ví dụ một filesystem server, ở scope `local`.
2. Chạy `/context` trước và sau. Ghi lại chênh lệch.
3. Tạo `.mcp.json` scope `project` dùng `${VAR}` cho token, commit nó, và kiểm
   tra rằng token không lọt vào git.

Làm đầy đủ ở [lab-05](../../labs/lab-05-mcp-server/README.md).

## Kiểm tra hiểu bài

- Ba scope khác nhau ở chỗ nào? Cái nào commit được?
- Tool `search` của server `jira` có tên đầy đủ là gì?
- Vì sao thêm nhiều MCP server lại làm phiên chậm và đắt hơn?

---

Trước: [04 — Subagents](04-subagents.md) · Tiếp: [Nâng cao 01 — Hooks](../03-nang-cao/01-hooks.md)
