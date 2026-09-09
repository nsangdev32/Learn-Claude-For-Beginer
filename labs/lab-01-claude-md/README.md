# Lab 01 — CLAUDE.md và rules

> Sau bài [Cơ bản 04](../../docs/01-co-ban/04-claude-md-va-bo-nho.md) · ~45 phút

## Mục tiêu

Biến một dự án thật của bạn thành nơi Claude Code làm việc hiệu quả ngay từ
phiên đầu tiên.

## Chuẩn bị

Chọn một dự án bạn đang làm, đủ lớn để có quy ước riêng. Đừng dùng repo trống.

## Các bước

### 1. Sinh bản nháp

```bash
cd ~/du-an-cua-ban
claude
```

```text
/init
```

### 2. Cắt bỏ phần thừa

Mở file vừa sinh và xoá mọi thứ Claude **tự suy ra được từ code**: cây thư mục,
danh sách dependency, mô tả kiến trúc chung chung.

Giữ lại và bổ sung:

- Lệnh build, test, lint chính xác (kể cả package manager nào).
- Quy ước code khác với mặc định của công cụ.
- Cạm bẫy: thư mục sinh tự động, service cần chạy sẵn, file không được sửa tay.

Mục tiêu: **dưới 100 dòng**.

### 3. Thêm một rule theo đường dẫn

`.claude/rules/testing.md`:

```markdown
---
paths:
  - "**/*.test.ts"
  - "tests/**/*"
---

# Luật viết test

- <quy ước đặt tên test của dự án bạn>
- <mock cái gì, không mock cái gì>
- <lệnh chạy một test đơn lẻ>
```

### 4. Kiểm chứng

```text
/context
```

Xem mục **Memory files**: `CLAUDE.md` phải có mặt, `testing.md` thì chưa.

Giờ nhờ Claude đọc một file test:

```text
đọc file test đầu tiên trong dự án và cho tôi biết nó test cái gì
```

Chạy `/context` lại. Rule `testing.md` giờ đã nạp.

### 5. Kiểm tra bằng thực tế

Bắt đầu một phiên mới (`/clear`) và giao một task nhỏ đúng loại việc bạn hay
làm. Đếm số lần bạn phải sửa lưng Claude về **quy ước** (không tính lỗi logic).

Mỗi lần sửa lưng là một dòng còn thiếu trong `CLAUDE.md`. Thêm vào, làm lại.

## Tiêu chí hoàn thành

- [ ] `CLAUDE.md` dưới 100 dòng, không chứa thông tin Claude tự suy ra được.
- [ ] Có ít nhất một rule trong `.claude/rules/` với `paths:`.
- [ ] `/context` xác nhận rule chỉ nạp khi chạm file khớp mẫu.
- [ ] Chạy một task thật mà không phải nhắc lại quy ước nào.
- [ ] `CLAUDE.md` đã commit; `CLAUDE.local.md` (nếu có) đã trong `.gitignore`.

## Câu hỏi suy ngẫm

- Dòng nào trong `CLAUDE.md` của bạn thật sự thay đổi hành vi của Claude, và
  dòng nào chỉ là trang trí?
- Có quy ước nào bạn muốn ép buộc chứ không chỉ gợi ý? Đó là ứng viên cho
  [hook](../../docs/03-nang-cao/01-hooks.md).
