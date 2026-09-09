# 03 — Lệnh slash và phím tắt

> Cấp độ: Cơ bản · Thời lượng: ~25 phút

## Mục tiêu

- Nhớ được nhóm lệnh `/` dùng hằng ngày.
- Biết lệnh nào giải quyết vấn đề nào.

Gõ `/` trong phiên để xem toàn bộ danh sách kèm mô tả. Bảng dưới là những lệnh
đáng thuộc lòng.

## Điều khiển phiên

| Lệnh | Tác dụng |
| --- | --- |
| `/clear [tên]` | Bắt đầu hội thoại mới, xoá context |
| `/resume` | Quay lại một hội thoại cũ |
| `/branch [tên]` | Rẽ nhánh hội thoại để thử hướng khác |
| `/fork [prompt]` | Sao chép hội thoại sang một phiên nền |
| `/export [file]` | Xuất hội thoại ra file văn bản |
| `/exit` | Thoát |

`/branch` rất hợp khi bạn muốn thử một cách làm mà không mất hội thoại hiện tại.

## Context và chi phí

| Lệnh | Tác dụng |
| --- | --- |
| `/context [all]` | Xem context đang bị chiếm bởi những gì |
| `/compact [ghi chú]` | Tóm tắt hội thoại để giải phóng chỗ |
| `/btw [câu hỏi]` | Hỏi ngoài lề, không đưa vào lịch sử |

Chi tiết ở [bài 05](05-quan-ly-context.md).

## Chất lượng và tốc độ

| Lệnh | Tác dụng |
| --- | --- |
| `/model [tên]` | Đổi model |
| `/effort [mức]` | Đổi mức suy luận: `low` → `max` |
| `/plan [mô tả]` | Vào plan mode cho thay đổi lớn |
| `/goal [điều kiện]` | Đặt mục tiêu, Claude làm tới khi đạt |

`/effort` là cần gạt đánh đổi giữa tốc độ và độ kỹ. Task đơn giản để `low`,
task khó để `high` trở lên.

## Code và git

| Lệnh | Tác dụng |
| --- | --- |
| `/diff` | Xem thay đổi trong working tree |
| `/code-review [mức] [--fix]` | Rà lỗi và điểm cần dọn trong diff |
| `/init` | Sinh `CLAUDE.md` cho dự án |
| `/memory` | Mở và sửa các file bộ nhớ |

## Cấu hình

| Lệnh | Tác dụng |
| --- | --- |
| `/config [key=value]` | Mở màn hình Settings hoặc đặt giá trị trực tiếp |
| `/permissions` | Quản lý quyền tool và auto mode |
| `/mcp` | Quản lý kết nối MCP server |
| `/doctor` | Kiểm tra cấu hình và chẩn đoán |
| `/debug [mô tả]` | Bật log gỡ lỗi |
| `/help` | Trợ giúp |

## Việc quy mô lớn

| Lệnh | Tác dụng |
| --- | --- |
| `/batch <yêu cầu>` | Điều phối thay đổi song song trên diện rộng |
| `/deep-research <câu hỏi>` | Tìm kiếm web nhiều nhánh, đối chiếu chéo |

## Phím tắt

| Phím | Tác dụng |
| --- | --- |
| `Shift+Tab` | Đổi permission mode |
| `Tab` | Tự hoàn thành lệnh |
| `↑` / `↓` | Lịch sử |
| `Esc` | Ngắt Claude giữa chừng |
| `Ctrl+D` ×2 | Thoát |

## Skill cũng là lệnh slash

Ngoài lệnh built-in, mọi **skill** đều xuất hiện dưới dạng `/tên-skill`. Repo này
có sẵn hai skill mẫu:

```text
/on-tap              # gợi ý bài học tiếp theo dựa trên notes/
/ghi-chu-buoi-hoc    # sinh ghi chú sau buổi học
```

Bạn sẽ tự viết skill ở [bài Trung cấp 03](../02-trung-cap/03-skills.md).

## Bài tập

1. Chạy `/context` ngay đầu phiên và ghi lại con số. Làm việc 15 phút rồi chạy
   lại, so sánh.
2. Dùng `/effort low` cho một câu hỏi đơn giản và `/effort high` cho một bài
   thiết kế. Ghi nhận khác biệt.
3. Mở repo này bằng Claude Code và chạy `/on-tap`.

## Kiểm tra hiểu bài

- `/clear` khác `/compact` chỗ nào?
- Bạn muốn thử một hướng giải khác mà vẫn giữ hội thoại cũ: dùng lệnh nào?
- Lệnh nào cho biết context đang bị chiếm bởi cái gì?

---

Trước: [02 — Phiên đầu tiên](02-phien-lam-viec-dau-tien.md) · Tiếp: [04 — CLAUDE.md](04-claude-md-va-bo-nho.md)
