# Lab 05 — Kết nối MCP server

> Sau bài [Trung cấp 05](../../docs/02-trung-cap/05-mcp.md) · ~45 phút

## Mục tiêu

Thêm một MCP server, đo cái giá của nó về context, và cấu hình an toàn ở scope
dự án.

## Các bước

### 1. Đo trước

Phiên mới, chưa thêm gì:

```text
/context
```

Ghi lại tổng và phần MCP.

### 2. Thêm một server stdio

Chọn một server đơn giản, ví dụ một filesystem server hoặc một server bạn tự
viết. Scope `local` để thử:

```bash
claude mcp add --transport stdio my-server -- npx -y <ten-goi-mcp>
claude mcp list
```

Trong phiên:

```text
/mcp
```

Xem trạng thái kết nối và danh sách tool.

### 3. Đo sau

```text
/context
```

Chênh lệch chính là cái giá bạn trả cho server này ở **mọi phiên**, kể cả phiên
không dùng tới nó.

### 4. Dùng thử một tool

Giao một việc buộc phải dùng tool của server. Chạy `--verbose` nếu muốn thấy
tên tool đầy đủ dạng `mcp__my-server__<tool>`.

### 5. Chuyển sang scope dự án

```bash
claude mcp remove my-server
claude mcp add --transport stdio my-server --scope project -- npx -y <ten-goi-mcp>
```

Mở `.mcp.json` vừa sinh ra. Nếu server cần token, sửa để dùng biến môi trường:

```json
{
  "mcpServers": {
    "my-server": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "<ten-goi-mcp>"],
      "env": {
        "API_TOKEN": "${MY_SERVER_TOKEN}"
      }
    }
  }
}
```

Kiểm chứng không có bí mật nào lọt vào git:

```bash
git diff .mcp.json
grep -riE '(token|secret|api[_-]?key)\s*[:=]\s*["'\'']?[A-Za-z0-9_-]{16,}' .mcp.json || echo "sạch"
```

### 6. Hạn chế quyền của server

Thêm vào `.claude/settings.json`:

```json
{
  "permissions": {
    "deny": ["mcp__my-server__<tool-nguy-hiem>"],
    "ask":  ["mcp__my-server__<tool-ghi-du-lieu>"]
  }
}
```

Xác nhận rule có tác dụng bằng cách yêu cầu Claude dùng đúng tool đó.

## Tiêu chí hoàn thành

- [ ] Server kết nối được, `/mcp` báo trạng thái tốt.
- [ ] Có số liệu `/context` trước và sau, biết chính xác chi phí.
- [ ] `.mcp.json` ở scope `project`, dùng `${VAR}` cho mọi bí mật.
- [ ] Đã kiểm tra không có token trong file được commit.
- [ ] Có ít nhất một permission rule nhắm vào tool của server.

## Câu hỏi suy ngẫm

- Server này có đáng chi phí context mà nó chiếm ở **mọi** phiên không? Nếu
  chỉ dùng một tuần một lần, có nên để scope `user` không?
- Kết quả trả về từ MCP server nên được coi là dữ liệu hay mệnh lệnh? Vì sao
  điều này quan trọng về mặt bảo mật?
