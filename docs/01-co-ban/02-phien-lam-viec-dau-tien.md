# 02 — Phiên làm việc đầu tiên

> Cấp độ: Cơ bản · Thời lượng: ~40 phút

## Mục tiêu

- Hiểu vòng lặp agent: Claude Code khác chatbot ở chỗ nào.
- Biết các tool tích hợp và khi nào chúng chạy.
- Dùng plan mode cho thay đổi lớn.
- Viết prompt đủ cụ thể để nhận kết quả dùng được.

## 1. Vòng lặp agent

Claude Code không chỉ trả lời. Mỗi lượt, nó lặp:

```
Bạn ra yêu cầu
   ↓
Claude chọn tool (đọc file, grep, chạy lệnh, sửa file)
   ↓
Tool trả kết quả về context
   ↓
Claude quyết định: gọi tool tiếp, hay trả lời xong
```

Hệ quả thực tế: **bạn không cần dán code vào chat**. Cứ mô tả vấn đề, Claude tự
đi tìm file. Dán code chỉ tốn context.

## 2. Các tool tích hợp

| Tool | Việc nó làm | Có hỏi phép không |
| --- | --- | --- |
| `Read`, `Glob`, `Grep` | Đọc và tìm trong file | Không, trong thư mục làm việc |
| `Edit`, `Write` | Sửa và tạo file | Có |
| `Bash` | Chạy lệnh shell | Có, trừ một số lệnh chỉ-đọc |
| `WebFetch`, `WebSearch` | Lấy nội dung web | Có |
| `Agent` | Giao việc cho subagent | Tuỳ cấu hình |
| `Skill` | Gọi một skill | Tuỳ cấu hình |

Chi tiết quyền hạn ở bài [Permissions](../02-trung-cap/01-permissions-va-che-do.md).

## 3. Plan mode

Với thay đổi lớn, đừng để Claude sửa ngay. Bấm `Shift+Tab` để chuyển chế độ,
hoặc khởi động bằng:

```bash
claude --permission-mode plan
```

Trong plan mode, Claude chỉ đọc file và chạy lệnh chỉ-đọc để khảo sát, rồi trình
bày kế hoạch. Bạn duyệt xong nó mới bắt đầu sửa. Dùng plan mode khi:

- Thay đổi chạm nhiều file hoặc nhiều module.
- Bạn chưa chắc cách làm nào đúng và muốn xem phương án trước.
- Bạn đang làm trên nhánh quan trọng.

## 4. Viết prompt cho ra kết quả

Ba nguyên tắc, xếp theo mức độ ảnh hưởng:

**Cụ thể hơn là ngắn gọn.**

```text
✗ sửa cái bug login
✓ sửa lỗi màn hình trắng sau khi nhập sai mật khẩu ở trang login
```

**Chia bước khi việc lớn.**

```text
1. tạo bảng user_profiles trong database
2. thêm endpoint GET/PATCH /api/profile
3. dựng trang cho phép user xem và sửa thông tin
```

**Cho Claude khảo sát trước khi sửa.**

```text
đọc qua schema database rồi cho tôi biết bảng nào đang lưu thông tin đơn hàng
```

## 5. Vòng lặp làm việc hằng ngày

```bash
cd ~/du-an-cua-ban
claude
```

Trong phiên:

```text
> tôi đã đổi gì so với main?
> viết test cho hàm calculateDiscount
> chạy test và sửa cho tới khi xanh
> commit với message mô tả rõ lý do
```

Các phím tắt cần nhớ:

| Phím | Tác dụng |
| --- | --- |
| `Shift+Tab` | Đổi permission mode |
| `↑` | Lịch sử lệnh |
| `Tab` | Tự hoàn thành lệnh `/` |
| `Esc` | Dừng Claude giữa chừng |
| `Ctrl+D` ×2 | Thoát |

## 6. Sai lầm thường gặp của người mới

| Sai lầm | Hậu quả | Cách sửa |
| --- | --- | --- |
| Dán nguyên file vào chat | Tốn context, Claude vẫn tự đọc được | Chỉ nói tên file |
| Yêu cầu quá mơ hồ | Claude đoán sai ý | Thêm ràng buộc, ví dụ đầu vào/đầu ra |
| Để một phiên chạy cả ngày | Context đầy, chất lượng giảm | `/clear` khi đổi việc |
| Duyệt mọi thứ không đọc | Thay đổi ngoài ý muốn lọt qua | Đọc diff trước khi duyệt |
| Không có `CLAUDE.md` | Lặp lại cùng một lời dặn mỗi phiên | Xem [bài 04](04-claude-md-va-bo-nho.md) |

## Bài tập

1. Mở một dự án cũ của bạn, hỏi `giải thích cấu trúc thư mục`. So sánh câu trả
   lời với hiểu biết của bạn.
2. Vào plan mode, yêu cầu một refactor vừa phải. Đọc kế hoạch, **từ chối**, và
   yêu cầu Claude làm cách khác.
3. Nhờ Claude thêm một test, chạy test đó, rồi commit. Toàn bộ trong một phiên.

## Kiểm tra hiểu bài

- Vì sao dán code vào chat thường là ý tồi?
- Plan mode ngăn Claude làm gì và cho phép nó làm gì?
- Bạn dừng Claude giữa chừng bằng phím nào?

---

Trước: [01 — Cài đặt](01-cai-dat-va-dang-nhap.md) · Tiếp: [03 — Lệnh slash](03-lenh-slash-va-phim-tat.md)
