# 04 — Subagents

> Cấp độ: Trung cấp · Thời lượng: ~45 phút · Lab: [lab-03](../../labs/lab-03-subagent-review/README.md)

Subagent là một Claude phụ chạy trong **context window riêng**, với system
prompt riêng, bộ tool riêng và model riêng.

## Mục tiêu

- Biết khi nào giao việc cho subagent thay vì làm thẳng.
- Viết được file định nghĩa subagent.
- Dùng giới hạn tool và chọn model để kiểm soát rủi ro và chi phí.

## 1. Vì sao dùng subagent

| Lý do | Giải thích |
| --- | --- |
| Giữ sạch context | Kết quả khảo sát không đổ hết vào phiên chính |
| Ràng buộc năng lực | Agent chỉ-đọc thì không thể sửa nhầm file |
| Tái sử dụng | Một định nghĩa dùng cho mọi dự án |
| Chuyên môn hoá | Prompt riêng cho một loại việc |
| Kiểm soát chi phí | Việc đơn giản định tuyến sang model rẻ hơn |

Trường hợp điển hình: "tìm xem logic tính thuế nằm ở đâu trong repo 5000 file".
Subagent đọc 40 file, phiên chính chỉ nhận về 3 dòng kết luận.

## 2. Đặt file ở đâu

| Vị trí | Phạm vi | Ưu tiên |
| --- | --- | --- |
| Managed settings | Toàn tổ chức | 1 (cao nhất) |
| Cờ `--agents` | Một phiên | 2 |
| `.claude/agents/` | Dự án, chia sẻ qua git | 3 |
| `~/.claude/agents/` | Mọi dự án của bạn | 4 |
| `agents/` trong plugin | Nơi plugin được bật | 5 |

## 3. File định nghĩa

```markdown
---
name: code-improver
description: Rà file và đề xuất cải thiện về khả năng đọc, hiệu năng và best practice. Dùng sau khi viết hoặc sửa code.
tools: Read, Grep, Glob
model: sonnet
memory: project
---

Bạn là chuyên gia cải thiện chất lượng code.

Với mỗi vấn đề tìm được:
1. Nêu rõ vấn đề
2. Trích đoạn code hiện tại
3. Đưa bản cải thiện kèm giải thích

Tập trung vào: khả năng đọc, hiệu năng, best practice, và bảo mật.
```

Chỉ `name` và `description` là bắt buộc.

## 4. Các trường frontmatter

| Trường | Tác dụng |
| --- | --- |
| `tools` | Danh sách trắng. Bỏ trống = kế thừa mọi tool |
| `disallowedTools` | Danh sách đen |
| `model` | `sonnet`, `opus`, `haiku`, `fable`, ID đầy đủ, hoặc `inherit` |
| `permissionMode` | `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan` |
| `maxTurns` | Giới hạn số lượt trước khi dừng |
| `skills` | Skill nạp sẵn khi khởi động |
| `mcpServers` | MCP server dành cho subagent này |
| `hooks` | Hook chỉ áp cho subagent này |
| `memory` | `user`, `project`, hoặc `local` — bộ nhớ riêng |
| `background` | `true` = chạy nền |
| `effort` | `low` → `max` |
| `isolation` | `worktree` = chạy trong git worktree riêng |
| `color` | Màu hiển thị |

## 5. Gọi subagent

```text
# Để Claude tự quyết
dùng agent code-improver để rà module authentication

# Ép dùng đúng agent
@"code-improver (agent)" review module này

# Đặt làm mặc định cho cả phiên
claude --agent code-improver
```

Hoặc trong `.claude/settings.json`:

```json
{ "agent": "code-improver" }
```

## 6. Giới hạn tool

Danh sách trắng — chỉ những tool được nêu:

```yaml
tools: Read, Grep, Glob, Bash
```

Danh sách đen — kế thừa mọi thứ trừ những tool bị gỡ:

```yaml
disallowedTools: Write, Edit
```

Một agent review code **nên** chỉ-đọc. Đây là ràng buộc kỹ thuật, không phải
lời nhắc trong prompt, nên nó không thể bị bỏ qua.

## 7. Bốn cạm bẫy

**Mô tả dài tốn context.** Tổng mọi `description` của subagent luôn nằm trong
context. Viết ngắn, đẩy chi tiết xuống phần thân — phần thân chỉ nạp khi agent chạy.

**Subagent không thấy auto memory của phiên chính.** Ngoại lệ là `fork`, vốn kế
thừa toàn bộ hội thoại cha.

**Model rẻ cho việc rẻ.** Tìm kiếm, đếm, liệt kê → model nhanh. Thiết kế kiến
trúc → model mạnh.

**Tạo agent trong thư mục mới thì cần khởi động lại** Claude Code để nó nhận.

## 8. Subagent hay skill?

| | Skill | Subagent |
| --- | --- | --- |
| Context | Dùng chung với phiên chính | Riêng biệt |
| Dùng cho | Quy trình bạn muốn Claude làm theo | Việc bạn muốn giao hẳn đi |
| Kết quả | Toàn bộ quá trình nằm trong phiên | Chỉ kết luận quay về |

Có thể kết hợp: một skill với `context: fork` chính là chạy skill đó trong
subagent.

## Bài tập

1. Tạo `.claude/agents/doc-checker.md` chỉ-đọc, nhiệm vụ kiểm tra tài liệu trong
   `docs/` có link gãy không.
2. Chạy nó, rồi chạy `/context` để xác nhận phiên chính không phình lên.
3. Đổi `model` sang một model nhanh hơn và so sánh thời gian với chất lượng.

Làm đầy đủ ở [lab-03](../../labs/lab-03-subagent-review/README.md).

## Kiểm tra hiểu bài

- Vì sao subagent giữ context phiên chính sạch hơn?
- `tools:` và `disallowedTools:` khác nhau thế nào?
- Phần nào của định nghĩa subagent luôn tốn context, phần nào không?

---

Trước: [03 — Skills](03-skills.md) · Tiếp: [05 — MCP](05-mcp.md)
