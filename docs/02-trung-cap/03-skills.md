# 03 — Skills: lệnh slash của riêng bạn

> Cấp độ: Trung cấp · Thời lượng: ~50 phút · Lab: [lab-02](../../labs/lab-02-skill-dau-tien/README.md)

Skill là cách đóng gói một quy trình lặp lại: hướng dẫn, tài liệu tham chiếu và
tự động hoá gói chung trong một thư mục. Điểm mạnh là **nạp theo nhu cầu** —
không chiếm context khi chưa dùng tới.

## Mục tiêu

- Viết được một skill chạy được.
- Hiểu progressive disclosure và vì sao nó quan trọng.
- Biết khi nào dùng skill thay vì CLAUDE.md hay subagent.

## 1. Cấu trúc thư mục

```
~/.claude/skills/           # cá nhân, mọi dự án
  ten-skill/
    SKILL.md                # bắt buộc
    reference.md            # tuỳ chọn, tài liệu bổ sung
    scripts/helper.py       # tuỳ chọn, script kèm theo

.claude/skills/             # dự án, chia sẻ qua git
  ten-skill/
    SKILL.md
```

**Tên thư mục trở thành tên lệnh**: `.claude/skills/deploy/` → `/deploy`.

## 2. SKILL.md

```markdown
---
name: summarize-changes
description: Tóm tắt thay đổi chưa commit và chỉ ra rủi ro. Dùng khi review diff hoặc viết commit message.
---

## Thay đổi hiện tại

!`git diff HEAD`

## Hướng dẫn

Tóm tắt thay đổi trên thành 2-3 gạch đầu dòng, rồi liệt kê rủi ro:
- Thiếu xử lý lỗi
- Giá trị hardcode
- Test cần cập nhật
- Thay đổi API gây breaking change

Nếu không có thay đổi nào, nói rõ như vậy.
```

Cú pháp `` !`lệnh` `` chạy lệnh **trước** khi Claude đọc nội dung, và chèn kết
quả vào prompt. Đây là điểm khiến skill mạnh hơn một đoạn text tĩnh.

## 3. Các trường frontmatter

| Trường | Tác dụng |
| --- | --- |
| `description` | Khi nào nên dùng skill. **Luôn nằm trong context** |
| `disable-model-invocation` | `true` = chỉ bạn gọi được bằng `/`, Claude không tự gọi |
| `user-invocable` | `false` = ẩn khỏi menu `/`, chỉ Claude gọi |
| `allowed-tools` | Duyệt trước các tool cho lượt này |
| `disallowed-tools` | Gỡ tool khi skill đang chạy |
| `argument-hint` | Gợi ý khi tự hoàn thành, ví dụ `[issue-number]` |
| `arguments` | Tên các tham số để thay thế bằng `$` |
| `context` | `fork` = chạy trong subagent tách biệt |
| `background` | Chạy subagent ở nền |
| `paths` | Chỉ kích hoạt với file khớp mẫu, ví dụ `*.ts` |

## 4. Progressive disclosure

Đây là ý tưởng cốt lõi:

1. **`description` luôn nạp** — Claude biết skill tồn tại. Tốn vài chục token.
2. **Toàn bộ `SKILL.md` chỉ nạp khi được gọi** — không lãng phí.
3. **File phụ chỉ nạp khi cần** — link tới chúng từ `SKILL.md`.

```markdown
## Tài liệu thêm

- [Tham chiếu API](reference.md) — chi tiết từng endpoint
- [Ví dụ](examples.md) — mẫu code cho các trường hợp thường gặp
```

Hệ quả: bạn có thể có 50 skill mà chi phí context vẫn nhỏ, miễn là mỗi
`description` viết ngắn gọn.

## 5. Tham số

```text
/fix-issue 123
```

`$ARGUMENTS` = `123`.

Nhiều tham số dùng vị trí:

```text
/migrate-component Button TypeScript Rust
```

`$0` = `Button`, `$1` = `TypeScript`, `$2` = `Rust`.

## 6. `allowed-tools`: duyệt trước

```yaml
---
name: commit-changes
description: Stage và commit theo chuẩn conventional commit
disable-model-invocation: true
allowed-tools: Bash(git add *) Bash(git commit *) Bash(git status *)
---
```

Trong lượt gọi skill này, ba lệnh trên chạy không cần hỏi. Quyền hết hiệu lực
khi bạn gửi tin nhắn tiếp theo. Lưu ý: nó **không giới hạn** tool khác — mọi
tool vẫn gọi được, chỉ là ba lệnh này khỏi phải duyệt.

## 7. Chọn giữa CLAUDE.md, rules, skill và subagent

| Bạn có | Dùng |
| --- | --- |
| Sự thật đúng ở mọi phiên (lệnh build, quy ước) | `CLAUDE.md` |
| Hướng dẫn chỉ liên quan tới một số file | `.claude/rules/` có `paths` |
| Quy trình nhiều bước bạn lặp lại | **Skill** |
| Việc ngốn nhiều context, chỉ cần kết luận | [Subagent](04-subagents.md) |
| Việc **bắt buộc** phải chạy đúng thời điểm | [Hook](../03-nang-cao/01-hooks.md) |

Đây là bảng đáng nhớ nhất của cấp độ 2.

## 8. Ví dụ trong repo này

Xem [`.claude/skills/on-tap/SKILL.md`](../../.claude/skills/on-tap/SKILL.md) và
[`.claude/skills/ghi-chu-buoi-hoc/SKILL.md`](../../.claude/skills/ghi-chu-buoi-hoc/SKILL.md).
Mở Claude Code trong repo rồi gõ `/on-tap` để thấy nó chạy.

## Bài tập

1. Viết skill `/review-nhanh` chạy `git diff` và rà theo checklist của riêng bạn.
2. Thêm `argument-hint` và dùng `$ARGUMENTS` để skill nhận tên file cụ thể.
3. Tách phần checklist dài ra `checklist.md` và link từ `SKILL.md`. Chạy
   `/context` trước và sau để thấy khác biệt.

Làm đầy đủ ở [lab-02](../../labs/lab-02-skill-dau-tien/README.md).

## Kiểm tra hiểu bài

- Phần nào của skill luôn nằm trong context, phần nào không?
- `disable-model-invocation: true` dùng cho loại skill nào? Cho ví dụ.
- `allowed-tools` có hạn chế Claude dùng tool khác không?

---

Trước: [02 — settings.json](02-settings-json.md) · Tiếp: [04 — Subagents](04-subagents.md)
