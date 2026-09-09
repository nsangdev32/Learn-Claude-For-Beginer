---
name: ghi-chu-buoi-hoc
description: Sinh file ghi chú cho buổi học Claude Code vừa xong, lưu vào notes/. Dùng khi người học nói "ghi chú lại", "tổng kết buổi học", hoặc kết thúc một bài.
disable-model-invocation: true
argument-hint: [tên bài, ví dụ "trung-cap-03-skills"]
---

## Mẫu ghi chú

@notes/_template.md

## Việc cần làm

1. Xác định bài học vừa xong. Nếu "$ARGUMENTS" có tên bài thì dùng nó; nếu
   không, suy ra từ hội thoại. Không suy ra được thì hỏi lại.
2. Tạo file `notes/<YYYY-MM-DD>-<ten-bai>.md` theo mẫu trên.
3. Điền các mục dựa trên **hội thoại thực tế** của buổi này:
   - Đã học được gì (3-5 gạch đầu dòng, cụ thể)
   - Chỗ còn lấn cấn
   - Lệnh/cấu hình đã thử và kết quả
   - Việc cần làm tiếp
4. Đừng bịa. Mục nào không có dữ liệu từ hội thoại thì để trống kèm dấu `_`.
5. Báo lại đường dẫn file đã tạo.
