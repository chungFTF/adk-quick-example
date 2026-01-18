# Agent 驗證指南

本指南說明如何驗證你的 multi-agent 系統是否正常運作。

## 快速開始

### 方法 1: 使用驗證腳本（推薦）

執行預設的測試套件：

```bash
cd adk-example
python validate_agent.py
```

這會執行一系列測試案例，包括：
- 數學計算測試（基本算術、百分比、平均數）
- 翻譯測試（多語言翻譯、單字解釋）
- 路由測試（混合查詢、不相關查詢）

### 方法 2: 互動式測試

如果你想手動測試特定的查詢：

```bash
python validate_agent.py --interactive
```

然後輸入你的查詢，輸入 `quit` 或 `exit` 結束。

### 方法 3: 使用 ADK Web UI

啟動開發介面：

```bash
adk web
```

在瀏覽器中打開 `http://localhost:8000`，選擇 `root_agent` 進行測試。

## 驗證項目

### 1. 路由功能驗證

確認 root_agent 能正確識別查詢類型並路由到適當的 sub-agent：

- ✅ 數學問題 → math_agent
- ✅ 翻譯問題 → translation_agent
- ✅ 混合問題 → 多個 agents
- ✅ 不相關問題 → root_agent 直接回應

**測試範例**：
```
"What is 25% of 480?" → 應該路由到 math_agent
"Translate 'Hello' to Spanish" → 應該路由到 translation_agent
"Calculate 10+20 and translate to French" → 應該路由到兩個 agents
```

### 2. Math Agent 驗證

測試數學計算功能：

- ✅ 基本算術運算
- ✅ 百分比計算
- ✅ 平均數和統計
- ✅ 步驟說明是否清晰

**測試範例**：
```
"What is 25% of 480?"
"Calculate the average of 10, 20, 30, 40, 50"
"如果一件商品原價 1000 元，打 8 折後是多少錢？"
```

### 3. Translation Agent 驗證

測試翻譯功能：

- ✅ 多語言翻譯準確性
- ✅ 單字解釋
- ✅ 文化背景說明（如果有的話）

**測試範例**：
```
"Translate 'Hello, how are you?' to Spanish"
"請將 '你好，很高興認識你' 翻譯成英文"
"What does 'serendipity' mean?"
```

### 4. 整合測試

測試多個 agents 協同工作：

- ✅ 混合查詢的處理
- ✅ State 管理（agents 之間的資訊共享）
- ✅ 回應的整合和連貫性

**測試範例**：
```
"Calculate the average of 10, 20, 30, 40, 50 and translate the result to French"
```

## 驗證指標

### 功能指標

- **路由準確率**: root_agent 是否正確識別查詢類型
- **回應品質**: 答案是否準確、清晰、有用
- **工具調用**: 如果有工具，是否正確調用
- **錯誤處理**: 遇到錯誤時是否優雅處理

### 效能指標（可選）

- **回應時間**: 一般應該在 30 秒內
- **Token 使用**: 監控 API 使用量

## 常見問題排查

### 問題 1: 導入錯誤

如果遇到 `ModuleNotFoundError`：

```bash
# 確保在正確的目錄
cd adk-example

# 確保依賴已安裝
pip install -r requirements.txt

# 檢查 Python 路徑
python -c "import sys; print(sys.path)"
```

### 問題 2: Agent 沒有回應

檢查：
1. 環境變數是否正確設置（`.env` 文件）
2. API 金鑰是否有效
3. 網路連線是否正常

### 問題 3: 路由不正確

如果查詢沒有路由到正確的 agent：
1. 檢查 root_agent 的 instruction 是否清晰
2. 確認 sub_agents 列表是否正確
3. 查看 agent 的 description 是否準確

## 下一步：RAG 驗證

當你完成 RAG 功能後，可以擴展驗證腳本來測試：

1. **檢索品質**：
   - 是否找到相關文件
   - 文件排名是否合理
   - 檢索到的內容是否與查詢相關

2. **生成品質**：
   - 回答是否基於檢索到的內容（groundedness）
   - 是否避免幻覺（hallucination）
   - 回答是否準確且有用

3. **整合測試**：
   - 端到端的 RAG 流程
   - 不同類型的查詢
   - 邊緣案例處理

## 擴展驗證腳本

你可以修改 `validate_agent.py` 來：

1. 添加更多測試案例
2. 添加 RAG 特定的測試
3. 添加自動化評估指標
4. 生成測試報告

範例：添加 RAG 測試

```python
{
    "name": "RAG 測試 - 知識檢索",
    "prompt": "根據你的知識庫，說明什麼是 RAG？",
    "expected_agent": "rag_agent",
    "check_retrieval": True  # 檢查是否檢索到相關文件
}
```

## 相關資源

- [ADK 文檔](https://ai.google.dev/adk)
- [TESTING_GUIDE.md](TESTING_GUIDE.md) - 其他測試範例
- [QUICK_START.md](QUICK_START.md) - 快速開始指南
