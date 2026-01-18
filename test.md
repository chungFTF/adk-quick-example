ok 這邊是我在本地開發一個簡單的 adk 範例

我主要想表達的是，我在本地開發，以及測試 adk 的方式

首先想先跟大家介紹一下程式碼架構
我們可以看到我有一個 example agent
其中包含了 root agent，這邊我們能看到我有定義一個 Agent 實體
其中名稱是 root agent 他是我們整個 agent 的總調度者

這邊我可以定義他使用哪一種 model，這邊我使用 Gemini 不過這邊不管是 openai or claude 都可以使用

那再接著就是我前面提到的給 agent 一個 personality，也就是透過 instruction 希望他的行為會如何做
這邊就會去定義 root agent 如果遇到用戶query 是跟計算相關，就將任務派遣給 math agent

如果是翻譯問題，就 route 給 translation agent

而底下我在 sub_agent 參數去加上我另外兩個 subagent
----

接下來，我們可以進去看到 sub agent 的定義
那 sub agent 也一樣，我們指定他使用哪一種 LLM model 以及這個 agent 要做的事情
像是 math agent 就是做基本的算數

那在 translation agent 也是一樣，值得注意的是 instruction 的部分，我定義 agent 可以去根據特定的語言做翻譯，並且解釋使用方式

娜以上是整個 agent 的開發架構
----

接下來，我們開發好就可以簡單進行測試，這時候我們可以使用內建的指令
`adk web`
在終端機輸入之後，就會跳出來一個本地的網址
點進去之後，就會來到一個 adk 的 UI 測試介面
這邊意思就是把我們剛剛開發好的程式碼，打包成一個用戶友善的互動是介面，可以讓我們在開發完後，直接有一個地方進行測試

像我在這邊打 hi, 娜一開始 root agent 就會收到我輸入的訊息，並給我相應的回覆

接著我可以輸入數學運算式
8 - 3 + 11 = ?
root agent 接收到之後，會辨識這是一個數學問題
那麼他就會 transfer to math agent
接著由 math agent 告訴我結果，以及我們可以看到 math agent 有依照我前面定義的 instruction 一步一步計算給我結果

----

那我們點擊旁邊也可以看到一些 agent 圖像化圖示，了解到 agent 呼叫的 metadata details 以及花費的時間

而如果我們接續詢問 Do you know the 'How are you?' in German?

那麼 math agent 知道這是一個翻譯問題，那他就會把任務傳遞給 translation agent
translation agent 接收到任務之後，就會回覆給我們對應的答案

那我們也可以看到 agent 也會依照我定義的 instruction 給予回覆

所以大致來說這就是 adk 的基本概念跟運作



