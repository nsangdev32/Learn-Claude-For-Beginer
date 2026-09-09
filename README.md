# Learn Claude Code — Từ cơ bản đến nâng cao

Dự án học tập và nghiên cứu **Claude Code**: từ cài đặt phiên đầu tiên cho tới
skills, subagents, hooks, MCP, plugins và tự động hoá trong CI.

Tài liệu viết bằng tiếng Việt, ví dụ và định danh code bằng tiếng Anh.

## Bắt đầu từ đâu

1. Đọc [lộ trình học](docs/00-lo-trinh.md) để biết thứ tự và thời lượng gợi ý.
2. Làm phần **Cơ bản** trong `docs/01-co-ban/`, mỗi bài kèm một bài tập nhỏ.
3. Sau mỗi bài lý thuyết, làm lab tương ứng trong [`labs/`](labs/README.md).
4. Ghi lại kết quả vào `notes/` theo mẫu [`notes/_template.md`](notes/_template.md).

## Cấu trúc

```
.
├── docs/
│   ├── 00-lo-trinh.md        # Lộ trình 3 cấp độ
│   ├── 01-co-ban/            # Cài đặt, phiên làm việc, CLAUDE.md, context
│   ├── 02-trung-cap/         # Permissions, settings, skills, subagents, MCP
│   ├── 03-nang-cao/          # Hooks, plugins, headless/CI, Agent SDK
│   └── tham-khao/            # Cheatsheet, nguồn tài liệu gốc
├── labs/                     # 6 bài thực hành có tiêu chí hoàn thành
├── notes/                    # Nhật ký học tập của bạn
├── scripts/check-links.py    # Kiểm tra liên kết nội bộ
├── .claude/                  # Cấu hình Claude Code của chính repo này
├── CLAUDE.md                 # Hướng dẫn cho Claude Code khi làm việc ở đây
└── README.md
```

## Repo này tự nó là một ví dụ

`.claude/` trong repo chứa một `settings.json` và hai skill mẫu. Bạn sẽ đọc,
sửa và mở rộng chúng khi học tới các bài tương ứng:

| Thành phần | Học ở bài |
| --- | --- |
| `CLAUDE.md` | [Cơ bản 04](docs/01-co-ban/04-claude-md-va-bo-nho.md) |
| `.claude/settings.json` | [Trung cấp 02](docs/02-trung-cap/02-settings-json.md) |
| `.claude/skills/` | [Trung cấp 03](docs/02-trung-cap/03-skills.md) |

Thử ngay: mở Claude Code trong thư mục này rồi gõ `/on-tap`.

## Yêu cầu

- Claude Code CLI đã cài và đăng nhập (xem [bài 01](docs/01-co-ban/01-cai-dat-va-dang-nhap.md)).
- Git.
- Node.js 18+ nếu bạn muốn làm lab về MCP và Agent SDK.

## Giấy phép

Nội dung học tập cá nhân. Trích dẫn tài liệu chính thức tại
[docs/tham-khao/nguon-tai-lieu.md](docs/tham-khao/nguon-tai-lieu.md).
