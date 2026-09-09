# 05 — Mô hình làm việc nâng cao

> Cấp độ: Nâng cao · Thời lượng: ~40 phút

Bài cuối. Ở đây không có tính năng mới, chỉ có cách ghép những gì đã học thành
quy trình làm việc thật sự nhanh hơn.

## Mục tiêu

- Chạy nhiều việc song song mà không giẫm chân nhau.
- Cấu hình Claude Code cho monorepo và codebase lớn.
- Có một checklist onboarding cho dự án mới.

## 1. Worktree: chạy song song không xung đột

Vấn đề: hai phiên Claude Code cùng sửa một working tree sẽ ghi đè lên nhau.

Giải pháp là git worktree — mỗi phiên một thư mục làm việc riêng, cùng một repo:

```bash
git worktree add ../du-an-feature-a -b feature/a
git worktree add ../du-an-feature-b -b feature/b

# hai terminal khác nhau
cd ../du-an-feature-a && claude
cd ../du-an-feature-b && claude
```

Subagent cũng dùng được worktree riêng bằng `isolation: worktree` trong
frontmatter.

Khi nào nên dùng: hai tính năng độc lập, hoặc một phiên chạy task dài trong khi
bạn làm việc khác.

## 2. Chạy nền và nhiều agent

```bash
claude --bg "chạy toàn bộ test suite và tóm tắt lỗi"
claude agents            # theo dõi và điều phối các phiên nền
claude attach <id>       # gắn vào một phiên nền
claude logs <id>         # xem output
claude stop <id>         # dừng
```

Mô hình dùng được: một phiên nền lo việc chậm (test toàn bộ, migration lớn),
phiên chính vẫn tương tác được.

## 3. Monorepo và codebase lớn

Ba vấn đề đặc trưng, ba cách xử lý:

**CLAUDE.md của đội khác lọt vào context.**

```json
{
  "claudeMdExcludes": [
    "/home/user/monorepo/other-team/.claude/rules/**"
  ]
}
```

Đặt trong `.claude/settings.local.json` để giữ riêng cho máy bạn.

**Hướng dẫn quá nhiều cho một file.** Tách theo package bằng `CLAUDE.md` lồng
trong thư mục con — chúng chỉ nạp khi Claude đọc file ở đó. Kết hợp
`.claude/rules/` có `paths` cho luật theo loại file.

**Khảo sát tốn context.** Đây là chỗ [subagent](../02-trung-cap/04-subagents.md)
có giá trị nhất. Một agent chỉ-đọc quét cả repo, phiên chính chỉ nhận kết luận.

## 4. Quy trình cho thay đổi lớn

```text
1. /plan  → mô tả yêu cầu, để Claude khảo sát và trình kế hoạch
2. Đọc kế hoạch. Sửa hoặc từ chối phần sai.
3. Duyệt → Claude thực hiện
4. /diff  → đọc thay đổi
5. /code-review high  → rà lỗi trước khi commit
6. Chạy test
7. Commit
```

Bước 2 là bước người mới hay bỏ qua. Sửa kế hoạch rẻ hơn sửa code rất nhiều.

## 5. Checklist onboarding một dự án mới

Khi bắt đầu dùng Claude Code cho một repo, làm theo thứ tự:

| Bước | Việc | Bài liên quan |
| --- | --- | --- |
| 1 | Chạy `/init`, dọn `CLAUDE.md` sinh ra | [Cơ bản 04](../01-co-ban/04-claude-md-va-bo-nho.md) |
| 2 | Viết `.claude/settings.json` với allow/deny, commit | [Trung cấp 01](../02-trung-cap/01-permissions-va-che-do.md), [02](../02-trung-cap/02-settings-json.md) |
| 3 | Thêm `.claude/rules/` cho luật theo đường dẫn | [Cơ bản 04](../01-co-ban/04-claude-md-va-bo-nho.md) |
| 4 | Viết 1-2 skill cho quy trình lặp lại nhiều nhất | [Trung cấp 03](../02-trung-cap/03-skills.md) |
| 5 | Thêm subagent chỉ-đọc cho việc khảo sát | [Trung cấp 04](../02-trung-cap/04-subagents.md) |
| 6 | Thêm hook cho việc bắt buộc (format, chặn lệnh nguy hiểm) | [Nâng cao 01](01-hooks.md) |
| 7 | Chạy `/context` và cắt bớt những gì không cần | [Cơ bản 05](../01-co-ban/05-quan-ly-context.md) |
| 8 | Đưa vào CI khi đã ổn định | [Nâng cao 03](03-headless-va-ci.md) |

Đừng làm cả tám bước ngay ngày đầu. Bước 1 và 2 đủ để bắt đầu; các bước sau
thêm vào khi bạn thấy đúng nhu cầu.

## 6. Dấu hiệu cấu hình của bạn đang có vấn đề

| Dấu hiệu | Nguyên nhân thường gặp |
| --- | --- |
| Phải sửa lưng Claude cùng một chuyện nhiều lần | `CLAUDE.md` thiếu luật đó |
| Phiên đầy context rất nhanh | MCP thừa, `CLAUDE.md` quá dài, không dùng subagent |
| Phải duyệt permission liên tục | `permissions.allow` chưa phản ánh cách bạn làm việc |
| Claude sửa file không nên sửa | Thiếu `deny` rule hoặc hook chặn |
| Kết quả kém đi giữa phiên dài | Cần `/compact` hoặc `/clear` |

## 7. Học tiếp

Claude Code phát hành rất nhanh. Hai việc nên làm định kỳ:

- Đọc [changelog và What's new](https://code.claude.com/docs/en/changelog).
- Chạy lại `/doctor` sau mỗi lần nâng cấp lớn, xem cấu hình còn hợp lệ không.

Danh sách nguồn đầy đủ ở [tham-khao/nguon-tai-lieu.md](../tham-khao/nguon-tai-lieu.md).

## Bài tập tổng kết

Chọn một dự án thật của bạn và chạy hết checklist ở mục 5, ít nhất tới bước 6.
Ghi lại vào `notes/` những gì bạn phải điều chỉnh so với tài liệu này.

## Kiểm tra hiểu bài

- Vì sao không nên chạy hai phiên Claude Code trên cùng một working tree?
- Trong monorepo, làm sao ngăn `CLAUDE.md` của đội khác lọt vào context?
- Bước nào của quy trình thay đổi lớn hay bị bỏ qua nhất, và vì sao nó quan trọng?

---

Trước: [04 — Agent SDK](04-agent-sdk.md) · Về [lộ trình](../00-lo-trinh.md)
