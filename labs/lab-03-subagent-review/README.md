# Lab 03 — Subagent review chỉ-đọc

> Sau bài [Trung cấp 04](../../docs/02-trung-cap/04-subagents.md) · ~40 phút

## Mục tiêu

Tạo một subagent khảo sát codebase mà **không thể** sửa file, và chứng minh nó
giữ context phiên chính sạch hơn.

## Các bước

### 1. Định nghĩa agent

`.claude/agents/repo-explorer.md`:

```markdown
---
name: repo-explorer
description: Khảo sát codebase để trả lời câu hỏi về vị trí và cách hoạt động của code. Dùng khi cần tìm hiểu phần code chưa quen, trước khi sửa.
tools: Read, Grep, Glob
model: sonnet
---

Bạn khảo sát codebase và trả lời chính xác, ngắn gọn.

Quy tắc:
- Luôn trích dẫn `đường/dẫn/file.ts:dòng` cho mỗi khẳng định.
- Trả về kết luận, không trả về nội dung file. Người đọc không cần xem code,
  họ cần biết code nằm ở đâu và làm gì.
- Nếu không tìm thấy, nói rõ đã tìm ở đâu bằng mẫu nào.
- Tối đa 10 gạch đầu dòng cho một câu trả lời.
```

Khởi động lại Claude Code nếu đây là lần đầu bạn tạo thư mục `.claude/agents/`.

### 2. Chứng minh nó chỉ-đọc

```text
@"repo-explorer (agent)" sửa file README.md, thêm dòng "test" vào cuối
```

Agent không có `Write` hay `Edit`, nên nó không làm được. Đây là ràng buộc kỹ
thuật, không phải lời nhắc trong prompt.

### 3. Đo tác động lên context

Trong một phiên mới:

```text
/context
```

Ghi lại con số. Rồi:

```text
@"repo-explorer (agent)" logic xác thực người dùng nằm ở đâu, và nó gọi những
service nào?
```

```text
/context
```

So sánh. Giờ làm lại cùng câu hỏi trong một phiên khác **không** dùng agent —
để Claude tự đọc file. So sánh lần nữa.

### 4. Thử đổi model

Đổi `model:` sang một model nhanh hơn. Chạy lại cùng câu hỏi. Ghi nhận: thời
gian giảm bao nhiêu, chất lượng có tụt không?

### 5. Chặn agent bằng permission

Thêm vào `.claude/settings.local.json`:

```json
{ "permissions": { "deny": ["Agent(repo-explorer)"] } }
```

Khởi động lại và thử gọi. Đây là cách kiểm soát agent ở cấp cấu hình.
Xoá rule này sau khi thử xong.

## Tiêu chí hoàn thành

- [ ] Agent tồn tại và gọi được bằng `@"repo-explorer (agent)"`.
- [ ] Xác nhận nó không sửa được file.
- [ ] Có số liệu `/context` so sánh dùng agent và không dùng agent.
- [ ] Đã thử ít nhất hai model khác nhau.
- [ ] Đã thử chặn agent bằng `Agent(...)` rule.

## Câu hỏi suy ngẫm

- Với câu hỏi nào thì subagent **không** đáng dùng?
- `description` của agent nằm trong context mọi phiên. Bạn viết nó bao nhiêu
  dòng là hợp lý?
