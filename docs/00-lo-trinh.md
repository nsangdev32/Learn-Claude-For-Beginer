# Lộ trình học Claude Code

Ba cấp độ, mỗi cấp độ khoảng một tuần nếu học 1–2 giờ/ngày. Không nhảy cóc:
mỗi cấp độ giả định bạn đã làm lab của cấp độ trước.

## Cấp độ 1 — Cơ bản

Mục tiêu: dùng Claude Code hằng ngày mà không sợ nó phá code của bạn.

| # | Bài | Nội dung chính |
| --- | --- | --- |
| 01 | [Cài đặt và đăng nhập](01-co-ban/01-cai-dat-va-dang-nhap.md) | Cài CLI, xác thực, `/doctor`, các nền tảng khác |
| 02 | [Phiên làm việc đầu tiên](01-co-ban/02-phien-lam-viec-dau-tien.md) | Vòng lặp agent, đọc/sửa file, plan mode |
| 03 | [Lệnh slash và phím tắt](01-co-ban/03-lenh-slash-va-phim-tat.md) | Các lệnh built-in đáng nhớ |
| 04 | [CLAUDE.md và bộ nhớ](01-co-ban/04-claude-md-va-bo-nho.md) | Bộ nhớ dự án, `.claude/rules/`, auto memory |
| 05 | [Quản lý context](01-co-ban/05-quan-ly-context.md) | `/context`, `/compact`, `/clear`, chi phí |

Lab: [lab-01](../labs/lab-01-claude-md/README.md).

## Cấp độ 2 — Trung cấp

Mục tiêu: cấu hình Claude Code cho một dự án thật và chia sẻ cấu hình đó cho cả nhóm.

| # | Bài | Nội dung chính |
| --- | --- | --- |
| 01 | [Permissions và chế độ](02-trung-cap/01-permissions-va-che-do.md) | `allow`/`ask`/`deny`, 6 permission mode |
| 02 | [settings.json](02-trung-cap/02-settings-json.md) | 5 tầng cấu hình và thứ tự ưu tiên |
| 03 | [Skills](02-trung-cap/03-skills.md) | Tự viết lệnh `/` của riêng bạn |
| 04 | [Subagents](02-trung-cap/04-subagents.md) | Tách context, giới hạn tool, chọn model |
| 05 | [MCP](02-trung-cap/05-mcp.md) | Kết nối tool ngoài qua Model Context Protocol |

Lab: [lab-02](../labs/lab-02-skill-dau-tien/README.md),
[lab-03](../labs/lab-03-subagent-review/README.md),
[lab-05](../labs/lab-05-mcp-server/README.md).

## Cấp độ 3 — Nâng cao

Mục tiêu: biến Claude Code thành một phần của hạ tầng kỹ thuật, không chỉ là công cụ gõ tay.

| # | Bài | Nội dung chính |
| --- | --- | --- |
| 01 | [Hooks](03-nang-cao/01-hooks.md) | Chặn và can thiệp vòng đời agent |
| 02 | [Plugins](03-nang-cao/02-plugins.md) | Đóng gói và phân phối cấu hình |
| 03 | [Headless và CI](03-nang-cao/03-headless-va-ci.md) | `claude -p`, JSON output, GitHub Actions |
| 04 | [Agent SDK](03-nang-cao/04-agent-sdk.md) | Nhúng agent vào ứng dụng của bạn |
| 05 | [Mô hình làm việc nâng cao](03-nang-cao/05-mo-hinh-lam-viec.md) | Worktree, chạy song song, dự án lớn |

Lab: [lab-04](../labs/lab-04-hook-dinh-dang/README.md),
[lab-06](../labs/lab-06-headless-ci/README.md).

## Cách học có hiệu quả

1. **Đọc rồi làm ngay.** Mỗi bài kết thúc bằng bài tập chạy được trên máy bạn.
2. **Ghi lại cái sai.** Chỗ Claude làm sai chính là chỗ `CLAUDE.md` của bạn còn thiếu.
3. **Đối chiếu tài liệu gốc.** Claude Code phát hành rất nhanh; xem
   [nguồn tài liệu](tham-khao/nguon-tai-lieu.md) khi có gì không khớp.
4. **Đo bằng kết quả.** Sau mỗi cấp độ, thử làm một task thật trong dự án của
   bạn và so sánh với cách bạn làm trước đây.

## Tự đánh giá

Bạn xong cấp độ khi trả lời được, không cần mở tài liệu:

- **Cấp 1**: CLAUDE.md nằm ở đâu, khác auto memory chỗ nào, `/compact` làm gì?
- **Cấp 2**: `Bash(git log *)` khớp lệnh nào và không khớp lệnh nào? Skill khác
  subagent ra sao?
- **Cấp 3**: Hook `PreToolUse` chặn một lệnh bằng cách nào? Vì sao `-p` cần
  `--allowedTools`?
