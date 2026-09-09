# 04 — CLAUDE.md và bộ nhớ

> Cấp độ: Cơ bản · Thời lượng: ~45 phút · Lab: [lab-01](../../labs/lab-01-claude-md/README.md)

Mỗi phiên Claude Code bắt đầu với context trống. Có hai cơ chế mang kiến thức
qua các phiên: **CLAUDE.md** do bạn viết, và **auto memory** do Claude tự ghi.

## Mục tiêu

- Biết đặt `CLAUDE.md` ở đâu và viết gì trong đó.
- Phân biệt CLAUDE.md với auto memory.
- Tách hướng dẫn dài ra `.claude/rules/` có phạm vi theo đường dẫn.

## 1. CLAUDE.md nằm ở đâu

Các vị trí, xếp theo thứ tự nạp từ rộng đến hẹp:

| Phạm vi | Vị trí | Dùng cho |
| --- | --- | --- |
| Tổ chức | `/etc/claude-code/CLAUDE.md` (Linux/WSL), `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) | Chuẩn của công ty, IT triển khai |
| Người dùng | `~/.claude/CLAUDE.md` | Sở thích cá nhân, áp cho mọi dự án |
| Dự án | `./CLAUDE.md` hoặc `./.claude/CLAUDE.md` | Chuẩn nhóm, commit vào git |
| Cá nhân trong dự án | `./CLAUDE.local.md` | Riêng bạn, thêm vào `.gitignore` |

Claude Code nạp `CLAUDE.md` từ thư mục làm việc và **mọi thư mục cha**. File
trong thư mục con nạp theo nhu cầu, khi Claude đọc file ở đó.

Chạy `/context` để xem file nào thực sự đã nạp, mục **Memory files**.

## 2. Viết gì trong CLAUDE.md

Nguyên tắc: **viết lại những gì bạn phải giải thích lần thứ hai.**

Thêm vào khi:

- Claude mắc lại đúng một lỗi lần thứ hai.
- Code review bắt được thứ đáng lẽ Claude phải biết.
- Bạn gõ lại đúng một câu chỉnh sửa như phiên trước.
- Người mới vào nhóm sẽ cần đúng thông tin đó.

Nội dung nên có: lệnh build/test, quy ước code, bố cục dự án, những luật
"luôn luôn làm X".

Ví dụ tối thiểu nhưng hữu ích:

```markdown
# CLAUDE.md

## Lệnh
- Test: `pnpm test` (không dùng npm, repo dùng pnpm)
- Lint: `pnpm lint --fix`

## Quy ước
- Thụt lề 2 space, không tab.
- API handler nằm ở `src/api/handlers/`.
- Không dùng `any` trong TypeScript; nếu buộc phải, kèm comment giải thích.

## Cạm bẫy
- `src/legacy/` sinh tự động, đừng sửa tay.
- Test cần Redis chạy sẵn ở cổng 6379.
```

## 3. Ba luật viết cho hiệu quả

**Ngắn.** Mục tiêu dưới 200 dòng. File dài tốn context và làm Claude tuân thủ
kém hơn. File trên 4 MiB bị bỏ qua hoàn toàn.

**Cụ thể đến mức kiểm chứng được.**

```text
✗ Format code cho đẹp
✓ Thụt lề 2 space

✗ Nhớ test
✓ Chạy `npm test` trước khi commit
```

**Không mâu thuẫn.** Nếu hai chỗ nói khác nhau, Claude chọn tuỳ tiện. Rà lại
định kỳ cả `CLAUDE.md` gốc, file trong thư mục con, và `.claude/rules/`.

## 4. Import file khác

```markdown
Xem @README để hiểu tổng quan và @package.json để biết các script npm.

# Hướng dẫn bổ sung
- quy trình git @docs/git-instructions.md
```

Đường dẫn tương đối tính từ file chứa import. Tối đa 4 tầng. Muốn nhắc một
đường dẫn mà **không** import, bọc trong backtick.

Lưu ý: import không giảm context — file được import vẫn nạp đầy đủ lúc khởi
động. Nó chỉ giúp tổ chức file gọn hơn.

## 5. `.claude/rules/` — hướng dẫn theo phạm vi

Với dự án lớn, tách hướng dẫn thành nhiều file trong `.claude/rules/`:

```
.claude/
├── CLAUDE.md
└── rules/
    ├── code-style.md
    ├── testing.md
    └── api-design.md
```

Điểm mạnh thật sự là **phạm vi theo đường dẫn**. Rule dưới đây chỉ nạp khi
Claude đụng vào file API:

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# Luật viết API

- Mọi endpoint phải validate input.
- Dùng format lỗi chuẩn của dự án.
- Kèm comment OpenAPI.
```

Rule không có `paths` thì nạp mọi phiên. Rule cá nhân cho mọi dự án đặt ở
`~/.claude/rules/`.

## 6. Auto memory

Song song với CLAUDE.md, Claude tự ghi chú vào
`~/.claude/projects/<project>/memory/`. Bốn loại: `user` (vai trò, thói quen
của bạn), `feedback` (những lần bạn sửa lưng Claude), `project` (việc đang làm,
quyết định), `reference` (nơi tra thông tin bên ngoài).

| | CLAUDE.md | Auto memory |
| --- | --- | --- |
| Ai viết | Bạn | Claude |
| Chứa gì | Luật và hướng dẫn | Bài học rút ra, sở thích |
| Chia sẻ | Qua git | Chỉ trên máy bạn |

Bật/tắt qua `/memory`, hoặc đặt `autoMemoryEnabled: false` trong settings.
Chỉ 200 dòng đầu (hoặc 25KB) của `MEMORY.md` được nạp mỗi phiên.

## 7. Khi Claude không nghe lời

CLAUDE.md là **context, không phải cấu hình bắt buộc**. Claude đọc và cố làm
theo, nhưng không có gì đảm bảo tuyệt đối.

Cách gỡ, theo thứ tự:

1. `/context` → kiểm tra file đã nạp chưa.
2. Viết cụ thể hơn.
3. Tìm hướng dẫn mâu thuẫn giữa các file.
4. Nếu là việc **bắt buộc phải chạy** đúng thời điểm (trước mỗi commit, sau
   mỗi lần sửa file) thì đó là việc của [hook](../03-nang-cao/01-hooks.md),
   không phải CLAUDE.md.

Đây là ranh giới quan trọng nhất của bài này:

> CLAUDE.md định hướng hành vi. Hook và permissions mới là lớp cưỡng chế.

## Bài tập

1. Chạy `/init` trong một dự án của bạn, đọc file sinh ra, xoá bớt những gì
   Claude tự suy ra được từ code.
2. Thêm một rule có `paths` cho thư mục test của dự án, rồi mở một file test và
   chạy `/context` để xác nhận rule đã nạp.
3. Chạy `/memory`, đọc thư mục auto memory, xoá một mục bạn thấy không đúng.

Làm đầy đủ ở [lab-01](../../labs/lab-01-claude-md/README.md).

## Kiểm tra hiểu bài

- File `CLAUDE.md` ở thư mục cha có được nạp không?
- Vì sao tách file bằng `@import` không tiết kiệm context?
- Bạn muốn ép chạy lint sau mỗi lần Claude sửa file: dùng CLAUDE.md hay hook?

---

Trước: [03 — Lệnh slash](03-lenh-slash-va-phim-tat.md) · Tiếp: [05 — Quản lý context](05-quan-ly-context.md)
