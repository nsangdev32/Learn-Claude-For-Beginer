# Lab 02 — Skill đầu tiên

> Sau bài [Trung cấp 03](../../docs/02-trung-cap/03-skills.md) · ~45 phút

## Mục tiêu

Viết một skill giải quyết đúng một việc bạn đang phải gõ lặp lại.

## Chọn việc gì

Nghĩ lại tuần vừa rồi: bạn đã gõ đoạn hướng dẫn nào cho Claude từ hai lần trở
lên? Vài ví dụ:

- "Review diff theo checklist của team"
- "Viết commit message theo chuẩn conventional commit"
- "Chuẩn bị mô tả PR từ các commit trên nhánh"
- "Tra một endpoint API trong tài liệu nội bộ"

## Các bước

### 1. Skill tối thiểu

`.claude/skills/review-nhanh/SKILL.md`:

```markdown
---
name: review-nhanh
description: Review thay đổi chưa commit theo checklist của dự án. Dùng trước khi commit hoặc mở PR.
---

## Thay đổi hiện tại

!`git diff HEAD`

## Checklist

Rà diff trên theo thứ tự sau và chỉ báo những gì thực sự có vấn đề:

1. Xử lý lỗi: có đường đi nào ném exception mà không ai bắt không?
2. Giá trị hardcode: URL, timeout, credential.
3. Test: thay đổi này có làm test nào cũ đi không?
4. API: có phá vỡ hợp đồng với caller không?

Với mỗi vấn đề, nêu `file:dòng` và cách sửa đề xuất. Không có vấn đề thì nói
ngắn gọn là sạch.
```

Chạy `/review-nhanh`.

### 2. Thêm tham số

```markdown
---
name: review-nhanh
description: Review thay đổi chưa commit theo checklist của dự án.
argument-hint: [đường dẫn file, để trống = toàn bộ diff]
---

## Thay đổi

!`git diff HEAD -- $ARGUMENTS`
```

Chạy `/review-nhanh src/api/handlers/user.ts`.

### 3. Tách phần dài ra file phụ

Khi checklist dài hơn 20 dòng, tách nó ra:

```
.claude/skills/review-nhanh/
├── SKILL.md
└── checklist.md
```

Trong `SKILL.md`:

```markdown
Rà theo [checklist đầy đủ](checklist.md). Đọc file đó trước khi bắt đầu.
```

Chạy `/context` trước và sau khi gọi skill để thấy tác dụng của progressive
disclosure.

### 4. Kiểm soát ai được gọi

Thêm `disable-model-invocation: true` nếu skill làm việc bạn muốn tự quyết định
thời điểm (deploy, commit, gửi thông báo).

### 5. Duyệt trước tool

Nếu skill luôn chạy cùng vài lệnh, khai báo:

```yaml
allowed-tools: Bash(git diff *) Bash(git log *)
```

Chạy lại và xác nhận không còn bị hỏi quyền.

## Tiêu chí hoàn thành

- [ ] Skill chạy được bằng `/tên-skill`.
- [ ] Có `description` dưới 2 dòng, nói rõ **khi nào** dùng.
- [ ] Dùng ít nhất một `` !`lệnh` `` để lấy dữ liệu động.
- [ ] Nhận tham số qua `$ARGUMENTS` hoặc `$0`.
- [ ] Đã tách nội dung dài ra file phụ.
- [ ] Skill đã commit vào `.claude/skills/` để cả nhóm dùng được.

## Câu hỏi suy ngẫm

- Nếu bạn có 30 skill, phần nào của chúng chiếm context và phần nào không?
- Skill này có nên chạy trong subagent (`context: fork`) không? Vì sao?
