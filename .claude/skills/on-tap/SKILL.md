---
name: on-tap
description: Gợi ý bài học Claude Code tiếp theo dựa trên ghi chú trong notes/. Dùng khi người học hỏi "học gì tiếp", "ôn lại", hoặc mở đầu một buổi học.
argument-hint: [cap-do hoặc chủ đề]
---

## Ghi chú đã có

!`ls -1 notes/*.md 2>/dev/null | grep -v _template || echo "(chưa có ghi chú nào)"`

## Lộ trình

@docs/00-lo-trinh.md

## Việc cần làm

Dựa vào danh sách ghi chú ở trên và lộ trình, hãy:

1. Xác định người học đang ở đâu. Không có ghi chú nào nghĩa là bắt đầu từ
   Cơ bản 01.
2. Đề xuất **một** bài tiếp theo, kèm đường dẫn file và lý do ngắn gọn.
3. Đặt 2-3 câu hỏi ôn tập về bài **trước đó** để kiểm tra người học còn nhớ.
   Nếu chưa có bài trước, bỏ qua bước này.
4. Nếu người học nêu chủ đề cụ thể trong "$ARGUMENTS", ưu tiên chủ đề đó thay
   vì thứ tự mặc định.

Trả lời ngắn gọn, tiếng Việt. Đừng tóm tắt lại nội dung bài học — chỉ định
hướng.
