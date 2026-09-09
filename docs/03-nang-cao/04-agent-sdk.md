# 04 — Claude Agent SDK

> Cấp độ: Nâng cao · Thời lượng: ~60 phút

Agent SDK cho phép nhúng chính vòng lặp agent của Claude Code vào ứng dụng của
bạn. Cùng một công cụ, cùng cơ chế permissions, hooks, MCP và skills — nhưng do
code của bạn điều khiển.

## Mục tiêu

- Dựng một agent chạy được bằng TypeScript hoặc Python.
- Hiểu quan hệ giữa `query`, `prompt` và `options`.
- Biết chọn bộ tool theo mức tự chủ mong muốn.

## 1. Cài đặt

**TypeScript**

```bash
npm init -y
npm pkg set type=module
npm install @anthropic-ai/claude-agent-sdk
npm install --save-dev tsx
```

**Python (uv)**

```bash
uv init
uv add claude-agent-sdk
```

**Python (pip)**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install claude-agent-sdk
```

Yêu cầu: Node.js 18+ hoặc Python 3.10+.

Cả hai SDK đóng gói sẵn binary Claude Code, nên thường không cần cài riêng.

## 2. Xác thực

```bash
export ANTHROPIC_API_KEY=your-api-key
```

SDK đọc key từ môi trường của tiến trình chạy agent; **nó không tự nạp file
`.env`**. Nếu bạn giữ key trong `.env`, tự nạp bằng `dotenv` trước khi gọi SDK.

Hỗ trợ cả Amazon Bedrock, Claude Platform on AWS, Google Cloud và Microsoft
Foundry qua các biến môi trường tương ứng.

> Đăng nhập kiểu claude.ai không dùng được cho sản phẩm bên thứ ba xây trên
> Agent SDK. Dùng API key.

## 3. Agent tối thiểu

**TypeScript** — `agent.ts`

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Rà utils.py tìm bug gây crash. Sửa những gì tìm được.",
  options: {
    allowedTools: ["Read", "Edit", "Glob"],
    permissionMode: "acceptEdits"
  }
})) {
  if (message.type === "assistant" && message.message?.content) {
    for (const block of message.message.content) {
      if ("text" in block) {
        console.log(block.text);
      } else if ("name" in block) {
        console.log(`Tool: ${block.name}`);
      }
    }
  } else if (message.type === "result") {
    console.log(`Done: ${message.subtype}`);
  }
}
```

Chạy: `npx tsx agent.ts`

**Python** — `agent.py`

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage


async def main():
    async for message in query(
        prompt="Rà utils.py tìm bug gây crash. Sửa những gì tìm được.",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Edit", "Glob"],
            permission_mode="acceptEdits",
        ),
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)
                elif hasattr(block, "name"):
                    print(f"Tool: {block.name}")
        elif isinstance(message, ResultMessage):
            print(f"Done: {message.subtype}")


asyncio.run(main())
```

Chạy: `uv run agent.py` hoặc `python agent.py`

## 4. Ba thành phần

| Thành phần | Vai trò |
| --- | --- |
| `query` | Điểm vào, tạo vòng lặp agent. Trả về async iterator |
| `prompt` | Việc bạn muốn làm. Claude tự chọn tool |
| `options` | Cấu hình: tool, permission mode, system prompt, MCP server... |

Vòng lặp `async for` chạy trong lúc Claude suy nghĩ, gọi tool, đọc kết quả và
quyết định bước tiếp. Mỗi vòng trả về một message. SDK lo điều phối, thực thi
tool, quản lý context và retry.

## 5. Bộ tool quyết định mức tự chủ

| Tool được cấp | Agent làm được gì |
| --- | --- |
| `Read`, `Glob`, `Grep` | Chỉ phân tích, không sửa |
| `Read`, `Edit`, `Glob` | Phân tích và sửa code |
| `Read`, `Edit`, `Bash`, `Glob`, `Grep` | Tự động hoá đầy đủ |

Đây là quyết định thiết kế quan trọng nhất. Cấp `Bash` nghĩa là agent chạy được
lệnh tuỳ ý trong môi trường của nó.

## 6. Tuỳ biến

```python
options = ClaudeAgentOptions(
    allowed_tools=["Read", "Edit", "Glob"],
    permission_mode="acceptEdits",
    system_prompt="Bạn là lập trình viên Python cấp cao. Luôn tuân thủ PEP 8.",
)
```

Các hướng mở rộng, tất cả đều có tài liệu riêng:

- **Permissions** — luật allow/deny và callback duyệt quyền tuỳ biến.
- **Hooks** — chạy code của bạn trước/sau mỗi tool call.
- **Sessions** — agent nhiều lượt, giữ context.
- **MCP servers** — nối database, browser, API.
- **Custom tools** — định nghĩa tool bằng chính code của bạn.
- **Structured outputs** — ép output theo JSON schema.

## 7. Chọn giữa CLI headless và SDK

| | `claude -p` | Agent SDK |
| --- | --- | --- |
| Ngôn ngữ | Bất kỳ, qua shell | TypeScript, Python |
| Kiểm soát từng bước | Không, chỉ có output cuối | Có, stream từng message |
| Tool tuỳ biến | Qua MCP server | Trực tiếp trong code |
| Hợp cho | Script, CI job | Sản phẩm có agent bên trong |

Quy tắc đơn giản: cần **chèn logic vào giữa vòng lặp** thì dùng SDK; chỉ cần
kết quả cuối thì `claude -p` gọn hơn.

## 8. Đưa lên production

Trước khi cho agent chạy tự động trong hệ thống thật:

- **Cách ly.** Container riêng, filesystem giới hạn, không có credential thừa.
- **Trần chi phí và số lượt.** Agent lỗi có thể lặp vô hạn.
- **Ghi log mọi tool call.** Có OpenTelemetry cho việc này.
- **Coi mọi đầu vào bên ngoài là dữ liệu**, không phải mệnh lệnh.
- **Con người duyệt** ở những chỗ hành động khó đảo ngược.

## Bài tập

1. Dựng agent tối thiểu theo mẫu trên và chạy được `Done: success`.
2. Đổi bộ tool sang chỉ-đọc và giao đúng việc đó lần nữa. Quan sát nó xử lý ra sao.
3. Thêm `system_prompt` bắt agent trả lời tiếng Việt và luôn trích dẫn đường dẫn file.
4. Thêm `Bash` và giao việc: "viết unit test cho utils.py, chạy, và sửa tới khi xanh".

## Kiểm tra hiểu bài

- `query` trả về cái gì, và vì sao phải lặp qua nó?
- SDK có tự đọc `.env` không?
- Khi nào dùng SDK thay vì `claude -p`?

---

Trước: [03 — Headless và CI](03-headless-va-ci.md) · Tiếp: [05 — Mô hình làm việc](05-mo-hinh-lam-viec.md)
