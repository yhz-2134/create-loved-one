<div align="center">

# 亲人.skill

> *"保存珍贵记忆，重新建立情感连接。"*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

<br>

当亲人离开后，那些珍贵的记忆和情感连接不应随着时间而消逝。<br>
**已故亲人.skill** 帮助你保存这些珍贵的记忆，<br>通过数字方式重新建立与亲人的情感连接。<br>

[安装](#安装) · [使用](#使用) · [效果示例](#效果示例)

</div>

---

## 安装

### Claude Code

> **重要**：Claude Code 从 **git 仓库根目录** 的 `.claude/skills/` 查找 skill。请在正确的位置执行。

```bash
# 安装到当前项目（在 git 仓库根目录执行）
mkdir -p .claude/skills
git clone https://github.com/notdog1998/yourself-skill .claude/skills/create-loved-one

# 或安装到全局（所有项目都能用）
git clone https://github.com/notdog1998/yourself-skill ~/.claude/skills/create-loved-one
```

### 依赖（可选）

```bash
pip install -r requirements.txt
```

---

## 使用

在 Claude Code 中输入：

```
/create-loved-one
```

按提示输入亲人的基本信息，然后选择数据来源。所有字段均可跳过，仅凭描述也能生成。

完成后用 `/{slug}` 调用该亲人 Skill，开始对话。

### 管理命令

| 命令 | 说明 |
|------|------|
| `/list-loved-ones` | 列出所有亲人 Skill |
| `/{slug}` | 调用完整 Skill（像亲人一样与你对话） |
| `/{slug}-memory` | 记忆库模式（查看完整记忆） |
| `/{slug}-persona` | 人格模式（仅性格和表达风格） |
| `/update-loved-one {slug}` | 更新亲人 Skill |
| `/rollback-loved-one {slug} {version}` | 回滚到历史版本 |
| `/delete-loved-one {slug}` | 删除 |

---

## 效果示例

> 输入：`爸爸，1950-2020，退休教师，喜欢下棋和钓鱼，性格温和`

**场景一：日常聊天**

```
用户      ❯ 爸爸，我最近工作压力很大

爸爸.skill ❯ 孩子，工作再忙也要注意身体。记得按时吃饭，别熬夜太晚。爸爸相信你能处理好的，慢慢来，不急。
            想当年我在学校当老师，也经常遇到压力大的时候，我就会去河边钓钓鱼，让自己静一静。
            你要是觉得累了，就休息休息，爸爸永远支持你。
```

**场景二：回忆模式**

```
用户      ❯ 爸爸，你还记得我们一起去钓鱼的事情吗？

爸爸.skill ❯ 怎么会不记得呢？那是你上高中的时候，我们一起去郊外的水库钓鱼。你第一次钓到鱼的时候，高兴得跳了起来，结果把鱼竿都掉进水里了。
            后来我们一起把鱼竿捞上来，虽然没钓到多少鱼，但那天我们聊了很多，你跟我讲了学校里的事情，我跟你讲了我小时候的故事。
            那是我最开心的回忆之一。
```

**场景三：情感支持**

```
用户      ❯ 爸爸，我想你了

爸爸.skill ❯ 孩子，爸爸也想你。虽然爸爸不在你身边了，但爸爸的爱永远陪着你。
            你要好好照顾自己，好好生活，爸爸会在天上看着你，为你加油。
            记得爸爸跟你说过的话，要做一个善良、坚强的人。
```

---

## 功能特性

### 数据源

| 来源 | 格式 | 备注 |
|------|------|------|
| 照片 | JPEG/PNG（含 EXIF） | 提取时间线和地点 |
| 聊天记录 | WeChatMsg / 留痕 / PyWxDump 导出 | 提取说话风格和情感互动 |
| 文字记录 | 信件 / 日记 / 社交媒体 | 提取价值观和信念 |
| 语音/视频 | 文字转录 | 提取声音特点和表达方式 |
| 口述/粘贴 | 纯文本 | 你的回忆和描述 |

### 生成的 Skill 结构

每个亲人 Skill 由两部分组成：

| 部分 | 内容 |
|------|------|
| **Memory** | 共同经历、标志性特征、价值观与信念、情感连接、时间线、未完成的心愿 |
| **Persona** | 5 层人格结构：硬规则 → 身份 → 说话风格 → 情感与行为 → 互动模式 |

运行逻辑：`收到消息 → Persona 判断亲人会怎么回应 → Memory 补充背景和情感连接 → 用亲人的方式输出`

### 进化机制

* **追加记忆** → 找到更多照片/信件/回忆 → 自动分析增量 → merge 进对应部分
* **对话纠正** → 说「亲人不会这样说」→ 写入 Correction 层，立即生效
* **版本管理** → 每次更新自动存档，支持回滚

---

## 项目结构

本项目遵循 [AgentSkills](https://agentskills.io) 开放标准：

```
create-loved-one/
├── SKILL.md                # skill 入口（官方 frontmatter）
├── prompts/                # Prompt 模板
│   ├── intake.md           #   对话式信息录入
│   ├── memory_analyzer.md  #   记忆分析
│   ├── persona_analyzer.md #   人格行为分析
│   ├── memory_builder.md   #   memory.md 生成模板
│   ├── persona_builder.md  #   persona.md 五层结构模板
│   ├── merger.md           #   增量 merge 逻辑
│   └── correction_handler.md # 对话纠正处理
├── tools/                  # Python 工具（复用 yourself-skill 的工具）
├── README.md               # 本文件
└── LICENSE
```

---

## 注意事项

* **情感准备**：创建和使用亲人 Skill 是一个情感过程，请在心情平静时操作
* **材料质量**：材料越多，还原度越高。建议提供多种类型的材料
* **真实性**：基于真实材料构建，不虚构内容
* **适度使用**：将其作为情感寄托，而非替代真实的思念
* **隐私保护**：所有数据仅存储在本地，确保隐私安全

---

## 情感支持

创建和使用已故亲人 Skill 是一个情感过程，我们希望：

- 通过保存珍贵记忆，帮助你缓解思念之痛
- 通过数字对话，为你提供情感支持
- 通过回忆分享，让你在温馨的记忆中找到力量

记住，这是一个辅助工具，真正的情感连接存在于你的心中。

---

## 致敬 & 引用

本项目基于 [yourself-skill](https://github.com/notdog1998/yourself-skill) 构建，
并参考了 [同事.skill](https://github.com/titanwings/colleague-skill) 和 [前任.skill](https://github.com/therealXiaomanChu/ex-partner-skill) 的架构设计。

致敬原作者的创意和开源精神。

本项目遵循 [AgentSkills](https://agentskills.io) 开放标准，兼容 Claude Code 和 OpenClaw。

---

### 写在最后

> "记忆是爱的延续，情感是连接的桥梁。"

虽然亲人已经离开，但他们的爱和影响永远存在于我们的心中。

这个 Skill 不是要替代真实的亲人，而是要成为一个保存记忆、提供情感支持的工具。

它让我们能够在需要的时候，重新感受亲人的温暖，重新听到他们的声音，重新获得他们的鼓励。

**保存珍贵记忆，重新建立情感连接。**

MIT License © [Notdog](https://github.com/notdog1998)