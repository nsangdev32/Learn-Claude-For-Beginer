# 02 — settings.json và thứ tự ưu tiên

> Cấp độ: Trung cấp · Thời lượng: ~30 phút

## Mục tiêu

- Biết đặt mỗi key vào đúng tầng cấu hình.
- Giải thích được vì sao một giá trị bạn đặt lại không có tác dụng.

## 1. Năm tầng, cao thắng thấp

| # | Tầng | File | Ai kiểm soát |
| --- | --- | --- | --- |
| 1 | Managed | `managed-settings.json`, MDM, console claude.ai | Tổ chức của bạn |
| 2 | Dòng lệnh | `claude --settings` | Bạn, cho một phiên |
| 3 | Project local | `.claude/settings.local.json` | Bạn, cho dự án này |
| 4 | Shared project | `.claude/settings.json` | Cả nhóm, qua git |
| 5 | User | `~/.claude/settings.json` | Bạn, mọi dự án |

Tầng 1 cao nhất. Managed settings thắng tất cả và không thể ghi đè.

**Ngoại lệ quan trọng:** các key kiểu danh sách (như `permissions.allow`,
`claudeMdExcludes`) **gộp lại** thay vì ghi đè. Rule cấm của tổ chức không bị
xoá bởi rule cho phép của bạn.

## 2. Key nào vào tầng nào

| Nội dung | Đặt ở |
| --- | --- |
| Quy ước và quyền của cả nhóm | `.claude/settings.json` (commit) |
| Đường dẫn máy bạn, token cá nhân | `.claude/settings.local.json` (gitignore) |
| Sở thích áp cho mọi dự án | `~/.claude/settings.json` |
| Chính sách bắt buộc của công ty | managed settings |

`.claude/settings.local.json` được Claude Code tự thêm vào `.gitignore`. Đừng
commit nó.

## 3. Các key hay dùng

```json
{
  "permissions": {
    "allow": ["Bash(npm run test*)"],
    "deny": ["Bash(git push *)", "Read(./.env)"],
    "defaultMode": "acceptEdits",
    "additionalDirectories": ["../shared-lib"]
  },
  "env": {
    "NODE_ENV": "test"
  },
  "hooks": {},
  "autoMemoryEnabled": true,
  "claudeMdExcludes": ["**/monorepo/other-team/CLAUDE.md"],
  "agent": "my-default-agent",
  "cleanupPeriodDays": 30
}
```

Danh sách đầy đủ ở [tài liệu All settings](https://code.claude.com/docs/en/settings-reference).
Đừng đoán tên key — key sai bị bỏ qua âm thầm.

## 4. Kiểm tra và gỡ rối

```bash
claude doctor          # xem cấu hình đã resolve, và rule nào bị bỏ qua
claude --debug         # log chi tiết
claude --safe-mode     # tắt hết tuỳ biến để khoanh vùng
```

Trong phiên: `/config` để xem và sửa, `/context` để xác nhận file bộ nhớ nào đã nạp.

Ba nguyên nhân phổ biến khiến một giá trị "không ăn":

1. Có tầng cao hơn đang đặt cùng key đó.
2. JSON sai cú pháp — cả file bị bỏ qua. `claude doctor` sẽ báo.
3. Tên key gõ sai. Không có lỗi, chỉ đơn giản là không có gì xảy ra.

## 5. Workspace trust

Rule `allow` trong file settings của dự án và hook trong settings chỉ có hiệu
lực sau khi bạn **tin tưởng thư mục đó**. Đây là hàng rào chống việc ai đó
commit một `settings.json` độc hại vào repo bạn vừa clone.

Hệ quả thực tế: lần đầu mở một repo lạ, hãy đọc `.claude/settings.json` của nó
trước khi bấm tin tưởng.

## Bài tập

1. Tạo `.claude/settings.json` cho một dự án của bạn với ít nhất 3 rule `allow`
   và 2 rule `deny`. Commit nó.
2. Đặt cùng một key ở cả `~/.claude/settings.json` và `.claude/settings.json`
   với giá trị khác nhau. Chạy `claude doctor` xem giá trị nào thắng.
3. Cố tình làm hỏng JSON (thiếu một dấu phẩy), khởi động lại, quan sát thông báo.

## Kiểm tra hiểu bài

- File nào nên commit, file nào phải gitignore?
- Vì sao `permissions.allow` của bạn không xoá được `deny` của tổ chức?
- Bạn đặt `defaultMode` nhưng phiên vẫn khởi động ở mode khác: kiểm tra gì đầu tiên?

---

Trước: [01 — Permissions](01-permissions-va-che-do.md) · Tiếp: [03 — Skills](03-skills.md)
