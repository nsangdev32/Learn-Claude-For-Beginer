# 05 — Quản lý context

> Cấp độ: Cơ bản · Thời lượng: ~30 phút

Context window là bộ nhớ làm việc của một phiên. Nó hữu hạn. Phần lớn trường hợp
"Claude hôm nay ngu đi" thật ra là context đã đầy hoặc đã bị nhiễu.

## Mục tiêu

- Đọc được `/context` và biết cái gì đang chiếm chỗ.
- Chọn đúng giữa `/compact` và `/clear`.
- Giảm lượng context tiêu thụ cho cùng một công việc.

## 1. Cái gì nằm trong context

Từ lúc phiên bắt đầu, context đã có sẵn:

- System prompt và định nghĩa tool.
- Các file `CLAUDE.md` đã nạp và `.claude/rules/` không có `paths`.
- Dòng đầu của auto memory (`MEMORY.md`).
- Mô tả (description) của mọi skill và subagent bạn đã cài.
- Danh sách tool của các MCP server đang kết nối.

Rồi trong lúc làm việc, nó phình thêm vì: nội dung file Claude đọc, output của
lệnh bash, kết quả tìm kiếm, và toàn bộ lịch sử hội thoại.

Chạy `/context` để thấy phân bổ. `/context all` cho chi tiết hơn.

## 2. Ba công cụ, ba tình huống

| Lệnh | Làm gì | Dùng khi |
| --- | --- | --- |
| `/compact [ghi chú]` | Tóm tắt hội thoại thành bản gọn | Vẫn đang làm cùng một việc, chỉ cần chỗ trống |
| `/clear` | Xoá sạch, bắt đầu lại | Chuyển sang việc khác hẳn |
| `/btw <câu hỏi>` | Hỏi ngoài lề, không lưu vào lịch sử | Cần tra một thứ không liên quan |

`/compact` nhận thêm chỉ dẫn:

```text
/compact giữ lại quyết định về schema database và danh sách file đã sửa
```

## 3. Cái gì sống sót qua compact

`CLAUDE.md` ở gốc dự án được **đọc lại từ đĩa** và nạp lại sau khi compact.
Rule có `paths:` nạp lại khi Claude đọc file khớp mẫu.

Cái **không** sống sót: hướng dẫn bạn chỉ nói trong chat. Nếu sau `/compact`
Claude quên một quy ước, nghĩa là quy ước đó chưa được viết vào `CLAUDE.md`.

## 4. Giảm tiêu thụ context

Xếp theo mức tiết kiệm, nhiều nhất trước:

**Giao việc khảo sát cho subagent.** Subagent có context riêng; phiên chính chỉ
nhận kết luận, không nhận toàn bộ file nó đã đọc. Xem
[bài Subagents](../02-trung-cap/04-subagents.md).

**Cắt bớt MCP server không dùng.** Mỗi server nạp toàn bộ định nghĩa tool vào
context ngay từ đầu phiên, dù bạn không gọi tool nào.

**Giữ CLAUDE.md dưới 200 dòng.** Chuyển hướng dẫn theo phạm vi sang
`.claude/rules/` có `paths`, chuyển quy trình nhiều bước sang
[skill](../02-trung-cap/03-skills.md) (skill chỉ nạp nội dung khi được gọi).

**Đừng dán file vào chat.** Nói tên file, để Claude tự đọc phần nó cần.

**Chia phiên theo việc.** Một phiên một mục tiêu, `/clear` khi đổi việc.

## 5. Chi phí

Context dài đồng nghĩa với nhiều token mỗi lượt. Vài cần gạt:

```text
/effort low        # giảm suy luận cho task đơn giản
/model             # đổi model phù hợp với độ khó
/context           # xem trước khi phình to
```

Trong headless, có thể chặn cứng:

```bash
claude -p --max-turns 3 --max-budget-usd 2.00 "sửa lỗi build"
```

## Bài tập

1. Đầu phiên chạy `/context`, ghi lại phân bổ. Đây là "chi phí cố định" của
   cấu hình hiện tại.
2. Tắt một MCP server bạn ít dùng, mở phiên mới, chạy lại `/context`. So sánh.
3. Làm một task tới khi context còn khoảng một phần tư, chạy
   `/compact giữ lại <điều quan trọng>`, rồi hỏi Claude tóm tắt xem nó còn nhớ gì.

## Kiểm tra hiểu bài

- Ba thứ đã chiếm context ngay trước khi bạn gõ chữ đầu tiên là gì?
- Sau `/compact`, hướng dẫn nào tự quay lại và hướng dẫn nào mất?
- Vì sao subagent tiết kiệm context cho phiên chính?

---

Trước: [04 — CLAUDE.md](04-claude-md-va-bo-nho.md) · Tiếp: [Trung cấp 01 — Permissions](../02-trung-cap/01-permissions-va-che-do.md)
