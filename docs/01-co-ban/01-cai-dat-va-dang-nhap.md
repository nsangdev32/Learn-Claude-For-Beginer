# 01 — Cài đặt và đăng nhập

> Cấp độ: Cơ bản · Thời lượng: ~20 phút

## Mục tiêu

- Cài Claude Code CLI trên máy của bạn.
- Đăng nhập và hiểu các loại tài khoản được hỗ trợ.
- Biết dùng `/doctor` khi có gì đó không chạy.

## 1. Cài đặt

### macOS, Linux, WSL

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

### Windows PowerShell

```powershell
irm https://claude.ai/install.ps1 | iex
```

### Windows CMD

```batch
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

Nếu dấu `&&` báo lỗi "not a valid statement separator" nghĩa là bạn đang ở
PowerShell chứ không phải CMD. Dấu nhắc có `PS C:\` là PowerShell.

### Các cách khác

| Cách | Lệnh | Tự cập nhật |
| --- | --- | --- |
| Native installer | xem trên | Có |
| Homebrew | `brew install --cask claude-code` | Không, dùng `brew upgrade claude-code` |
| WinGet | `winget install Anthropic.ClaudeCode` | Không, dùng `winget upgrade Anthropic.ClaudeCode` |

Trên Windows, nên cài thêm [Git for Windows](https://git-scm.com/downloads/win)
để Claude Code dùng được Bash; nếu không, nó sẽ dùng PowerShell làm shell.

### Kiểm tra

```bash
claude --version
```

Lệnh in ra số phiên bản kèm `(Claude Code)`.

## 2. Đăng nhập

Chạy `claude` lần đầu, CLI sẽ yêu cầu đăng nhập qua trình duyệt.

```bash
claude
```

Đổi tài khoản về sau: gõ `/login` ngay trong phiên.

Các loại tài khoản dùng được:

- **Claude Pro, Max, Team, Enterprise** — khuyến nghị cho cá nhân và nhóm.
- **Claude Console** — trả tiền theo lượng dùng, hợp cho tự động hoá.
- **Amazon Bedrock, Google Cloud, Microsoft Foundry** — triển khai doanh nghiệp.

Nếu biến môi trường `ANTHROPIC_API_KEY` đã được đặt, Claude Code bỏ qua màn hình
đăng nhập và chỉ hỏi bạn duyệt key đó.

## 3. Không chỉ có terminal

Cùng một Claude Code chạy ở nhiều nơi, dùng chung cấu hình `.claude/`:

| Nơi chạy | Dùng khi |
| --- | --- |
| CLI trong terminal | Mặc định, đầy đủ tính năng nhất |
| VS Code / JetBrains | Muốn xem diff ngay trong editor |
| [claude.ai/code](https://claude.ai/code) | Máy yếu, hoặc chạy task dài trên cloud |
| Desktop app | Nhiều phiên song song, giao diện đồ hoạ |
| GitHub Actions / GitLab CI | Tự động review PR, sửa lỗi CI |

Bài [Headless và CI](../03-nang-cao/03-headless-va-ci.md) nói kỹ về hai dòng cuối.

## 4. Khi có sự cố

```bash
claude doctor        # kiểm tra cài đặt, cấu hình, kết nối
claude --debug       # bật log chi tiết
claude --safe-mode   # tắt mọi tuỳ biến để tìm nguyên nhân
```

`/doctor` chạy được cả bên trong phiên. Đây là lệnh đầu tiên nên gõ khi hook,
skill hay MCP server "im lặng" không hoạt động.

## Bài tập

1. Cài Claude Code và chạy `claude --version`.
2. Đăng nhập, sau đó chạy `claude doctor` và đọc hết output. Ghi lại mục nào
   báo cảnh báo.
3. `cd` vào một dự án bất kỳ của bạn và chạy `claude`, hỏi:
   `dự án này làm gì?`

## Kiểm tra hiểu bài

- Cách cài nào tự cập nhật nền, cách nào phải nâng cấp thủ công?
- Bạn đang đăng nhập bằng loại tài khoản nào, và nó ảnh hưởng gì tới chi phí?
- Khi một skill bạn viết không xuất hiện trong menu `/`, lệnh nào chạy trước tiên?

---

Tiếp theo: [02 — Phiên làm việc đầu tiên](02-phien-lam-viec-dau-tien.md)
