# 01 — Permissions và chế độ quyền

> Cấp độ: Trung cấp · Thời lượng: ~50 phút

Đây là lớp **cưỡng chế**: khác với `CLAUDE.md` chỉ định hướng, permission rules
được client thực thi bất kể Claude quyết định gì.

## Mục tiêu

- Đọc và viết được rule `Tool(specifier)`.
- Hiểu chính xác dấu `*` khớp cái gì.
- Chọn đúng permission mode cho từng hoàn cảnh.

## 1. Sáu permission mode

| Mode | Hành vi |
| --- | --- |
| `default` (Manual) | Hỏi lần đầu mỗi tool |
| `acceptEdits` | Tự duyệt sửa file và lệnh filesystem thông thường (`mkdir`, `mv`, `cp`) trong thư mục làm việc |
| `plan` | Chỉ đọc và chạy lệnh chỉ-đọc; không sửa source |
| `auto` | Tự duyệt, có bộ phân loại chạy nền kiểm tra hành động có khớp yêu cầu không |
| `dontAsk` | Tự **từ chối** trừ khi đã cho phép trước qua `permissions.allow` |
| `bypassPermissions` | Bỏ qua mọi lời hỏi |

Đổi bằng `Shift+Tab` trong phiên, hoặc `--permission-mode` khi khởi động, hoặc
`defaultMode` trong settings.

`bypassPermissions` bỏ qua cả ghi vào đường dẫn được bảo vệ như `.git` và
`.claude`. **Chỉ dùng trong container hoặc VM cách ly.**

Chặn hai mode nguy hiểm ở cấp tổ chức:

```json
{
  "permissions": {
    "disableBypassPermissionsMode": "disable",
    "disableAutoMode": "disable"
  }
}
```

## 2. Cú pháp rule

Dạng chung: `Tool` hoặc `Tool(specifier)`.

```json
{
  "permissions": {
    "allow": ["Bash(npm run *)", "Bash(git commit *)", "Read"],
    "ask":   ["Bash(docker *)"],
    "deny":  ["Bash(git push *)", "Read(./.env)"]
  }
}
```

- `deny` thắng `ask`, `ask` thắng `allow`.
- Tên tool trần (`Bash`, `Read`) khớp mọi lần dùng. `Bash(*)` tương đương `Bash`.
- Deny bằng tên tool trần sẽ **gỡ hẳn tool đó khỏi context** của Claude.

## 3. Dấu `*` khớp cái gì — phần dễ sai nhất

Claude Code khớp mọi thứ **trước dấu `*` đầu tiên** đúng nguyên văn.

| Bạn viết | Khớp | Không khớp |
| --- | --- | --- |
| `Bash(npm run build)` | `npm run build` | `npm run build --watch` |
| `Bash(npm run *)` | `npm run build`, `npm run test --watch`, `npm run` | `npm install` |
| `Bash(git log * main)` | `git log --oneline main`, `git log -5 main` | `git log main` |
| `Bash(git * main)` | `git merge main`, `git push origin main` | `git log` |
| `Bash(ls *)` | `ls -la`, `ls` | `lsof` |
| `Bash(ls*)` | `ls -la`, `lsof` | |

Ba luật rút ra:

1. **Đặt `*` sau subcommand.** `Bash(git *)` cho phép *mọi* lệnh git, kể cả
   `git push`. Ý bạn thường là `Bash(git log *)`.
2. **`*` ở cuối kèm dấu cách cũng khớp lệnh trần.** `Bash(ls *)` khớp cả `ls`.
3. **Dấu cách trước `*` là một phần của rule.** `Bash(ls *)` không khớp `lsof`,
   nhưng `Bash(ls*)` thì có.

Hậu tố `:*` tương đương `*` ở cuối: `Bash(ls:*)` giống `Bash(ls *)`.

Cảnh báo: rule có `*` **trước** subcommand, như `Bash(git * main)`, cho phép cả
`git -c core.fsmonitor=<script> diff main`, tức là chạy chương trình tuỳ ý.
Claude Code cảnh báo lúc khởi động khi thấy dạng này trong `allow`.

## 4. Rule theo từng tool

**Bash** — khớp toàn bộ chuỗi lệnh.

**Read / Edit** — khớp theo đường dẫn, dùng neo `//` (tuyệt đối), `~/` (home),
`./` (thư mục làm việc):

```json
{ "permissions": { "deny": ["Read(./.env)", "Read(./secrets/**)"] } }
```

**WebFetch** — `WebFetch(domain:example.com)`.

**MCP** — theo tên server:

```text
mcp__puppeteer                        # mọi tool của server puppeteer
mcp__puppeteer__*                     # tương đương
mcp__github__get_*                    # chỉ các tool bắt đầu bằng get_
```

Allow rule chỉ chấp nhận glob **sau** tiền tố `mcp__<server>__` cụ thể. Glob
kiểu `"*"` hay `"mcp__*"` trong `allow` bị bỏ qua kèm cảnh báo.

**Agent** — kiểm soát subagent:

```json
{ "permissions": { "deny": ["Agent(Explore)"] } }
```

**Theo tham số** (chỉ cho `deny` và `ask`):

```text
Agent(model:opus)              # gọi Agent có yêu cầu model tier opus
Bash(run_in_background:true)   # lệnh bash chạy nền
```

Không dùng được với trường nội dung chính (`command` của Bash, `file_path` của
Read/Edit/Write, `url` của WebFetch) — vì `Bash(command:rm *)` sẽ bị lách bằng
lệnh ghép. Dùng `Bash(rm *)` thay thế.

## 5. Cấu hình mẫu cho một dự án thật

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run test*)",
      "Bash(npm run lint*)",
      "Bash(git status)",
      "Bash(git diff *)",
      "Bash(git log *)",
      "Bash(git add *)",
      "Bash(git commit *)"
    ],
    "ask": [
      "Bash(npm install *)",
      "WebFetch"
    ],
    "deny": [
      "Bash(git push *)",
      "Bash(rm -rf *)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./**/credentials*)"
    ],
    "defaultMode": "acceptEdits"
  }
}
```

Đọc là: sửa file thoải mái, chạy test và thao tác git cục bộ không cần hỏi,
hỏi trước khi cài package hay lên mạng, và **tuyệt đối không** push hay đọc bí mật.

## 6. Thư mục làm việc

Claude đọc/sửa trong thư mục làm việc và các thư mục thêm bằng `--add-dir`
hoặc `permissions.additionalDirectories`. Lưu ý: thư mục thêm cho **quyền truy
cập file**, không tự động nạp cấu hình `CLAUDE.md` của thư mục đó.

## Bài tập

1. Viết rule chỉ cho phép `git log` và `git diff`, chặn mọi lệnh git khác.
   Kiểm chứng bằng cách nhờ Claude chạy `git status`.
2. Chặn đọc file `.env`, rồi thử yêu cầu Claude "đọc biến môi trường trong .env".
   Quan sát nó bị chặn thế nào.
3. Bật `dontAsk` trong một phiên và xem cái gì gãy. Đây là bài học tốt về việc
   allow list của bạn còn thiếu gì.

## Kiểm tra hiểu bài

- `Bash(git *)` có cho phép `git push` không? Vì sao?
- `Bash(ls *)` và `Bash(ls*)` khác nhau ra sao?
- Rule nào thắng khi một lệnh khớp cả `allow` lẫn `deny`?

---

Tiếp: [02 — settings.json](02-settings-json.md)
