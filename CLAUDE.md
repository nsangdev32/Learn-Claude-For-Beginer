# CLAUDE.md

Hướng dẫn cho Claude Code khi làm việc trong repository này.

## Bối cảnh

Đây là repo **học tập về Claude Code**, không phải ứng dụng chạy được. Sản phẩm
chính là tài liệu Markdown trong `docs/`, bài thực hành trong `labs/`, và ghi
chú của người học trong `notes/`.

## Cấu trúc

```
docs/00-lo-trinh.md   Lộ trình tổng thể, sửa khi thêm/bớt bài
docs/01-co-ban/       Cấp độ 1
docs/02-trung-cap/    Cấp độ 2
docs/03-nang-cao/     Cấp độ 3
docs/tham-khao/       Cheatsheet và danh sách nguồn
labs/lab-NN-*/        Mỗi lab một thư mục, có README.md riêng
notes/                Nhật ký học, người dùng tự viết
scripts/              Tiện ích bảo trì repo
.claude/skills/       Skill mẫu dùng để dạy học
```

## Lệnh thường dùng

Chưa có build/test. Kiểm tra tài liệu bằng:

```bash
python3 scripts/check-links.py    # tìm liên kết nội bộ bị gãy
```

## Quy ước viết tài liệu

- **Ngôn ngữ**: nội dung tiếng Việt; tên file, lệnh, key JSON, tên biến tiếng Anh.
- **Tên file**: chữ thường, không dấu, phân cách bằng `-`, có tiền tố số thứ tự.
- **Mỗi bài học** có đủ: mục tiêu, nội dung, ví dụ chạy được, bài tập, phần
  "Kiểm tra hiểu bài".
- **Không bịa tính năng**. Mọi cờ CLI, key settings, trường frontmatter phải
  đối chiếu với tài liệu chính thức tại `code.claude.com/docs`. Nếu không chắc,
  ghi rõ là chưa xác minh thay vì đoán.
- **Đường dẫn tương đối** khi liên kết giữa các file trong repo.

## Quy ước git

- **Nhánh**: phát triển trên nhánh tính năng, không commit thẳng vào `main`.
- **Commit**: thể mệnh lệnh, tiếng Việt được, mô tả *tại sao* thay đổi.
- **Bí mật**: không commit key, token hay `.env`.

## Lưu ý

- `notes/` là của người học. Không sửa hay dọn dẹp trừ khi được yêu cầu rõ ràng.
- Khi thêm một bài học mới, cập nhật cả `docs/00-lo-trinh.md` và bảng mục lục
  trong `README.md`.
