---
name: create-loved-one
description: "Preserve memories of your loved ones and reconnect through digital means. | 保存已故亲人的珍贵记忆，通过数字方式重新建立情感连接。"
argument-hint: "[name-of-loved-one]"
version: "1.0.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

> **Language / 语言**: This skill supports both English and Chinese. Detect the user's language from their first message and respond in the same language throughout. Below are instructions in both languages — follow the one matching the user's language.
> 
> 本 Skill 支持中英文。根据用户第一条消息的语言，全程使用同一语言回复。下方提供了两种语言的指令，按用户语言选择对应版本执行。

# 已故亲人.skill 创建器（Claude Code 版）

## 触发条件

当用户说以下任意内容时启动：
- `/create-loved-one`
- "帮我创建一个已故亲人的skill"
- "我想保存亲人的记忆"
- "新建亲人记忆"
- "给我做一个已故亲人的skill"

当用户对已有亲人 Skill 说以下内容时，进入进化模式：
- "我有新的回忆" / "追加记忆"
- "这不对" / "亲人不会这样说" / "应该是"
- `/update-loved-one {slug}`

当用户说 `/list-loved-ones` 时列出所有已生成的亲人 Skill。

---

## 工具使用规则

本 Skill 运行在 Claude Code 环境，使用以下工具：

| 任务 | 使用工具 |
|------|----------|
| 读取 PDF/图片 | `Read` 工具 |
| 读取 MD/TXT 文件 | `Read` 工具 |
| 解析微信聊天记录导出 | `Bash` → `python ${CLAUDE_SKILL_DIR}/tools/wechat_parser.py` |
| 解析 QQ 聊天记录导出 | `Bash` → `python ${CLAUDE_SKILL_DIR}/tools/qq_parser.py` |
| 解析社交媒体内容 | `Bash` → `python ${CLAUDE_SKILL_DIR}/tools/social_parser.py` |
| 分析照片元信息 | `Bash` → `python ${CLAUDE_SKILL_DIR}/tools/photo_analyzer.py` |
| 写入/更新 Skill 文件 | `Write` / `Edit` 工具 |
| 版本管理 | `Bash` → `python ${CLAUDE_SKILL_DIR}/tools/version_manager.py` |
| 列出已有 Skill | `Bash` → `python ${CLAUDE_SKILL_DIR}/tools/skill_writer.py --action list` |
| 合并生成 SKILL.md | `Bash` → `python ${CLAUDE_SKILL_DIR}/tools/skill_writer.py --action combine` |

**目标目录**：生成的 Skill 必须写入 `./.claude/skills/{slug}/`，这样 `/{slug}` 才能被 Claude Code 直接识别和调用。

> **Windows 用户注意**：如果你使用 Git Bash，`python3` 可能不可用，所有命令已统一使用 `python`。若运行时中文输出乱码，请在 Bash 中先执行 `export PYTHONIOENCODING=utf-8`。

---

## 主流程：创建新亲人 Skill

### Step 1：基础信息录入（4 个问题）

1. **亲人的姓名/昵称**（必填）
   - 示例：`爸爸` / `妈妈` / `爷爷` / `奶奶`
2. **生卒年份**（可选）
   - 示例：`1950-2020`
3. **与你的关系**（必填）
   - 示例：`父亲` / `母亲` / `祖父` / `祖母`
4. **基本背景**（一句话：职业、兴趣爱好、性格特点）
   - 示例：`退休教师，喜欢下棋和钓鱼，性格温和`

### Step 2：原材料导入

询问用户提供原材料，展示方式供选择：

```
请提供与亲人相关的原材料，材料越多，还原度越高。

  [A] 照片
      包含时间、地点信息的照片，会提取时间线和重要场景

  [B] 聊天记录
      与亲人的微信、QQ等聊天记录

  [C] 文字记录
      信件、日记、社交媒体内容等

  [D] 语音/视频
      亲人的语音或视频片段（请上传文字转录）

  [E] 口述回忆
      分享你对亲人的回忆和描述

可以混用，也可以跳过（仅凭手动信息生成）。
```

---

#### 方式 A：照片分析

```
python ${CLAUDE_SKILL_DIR}/tools/photo_analyzer.py \
  --dir {photo_dir} \
  --output /tmp/photo_out.txt
```

提取维度：
- EXIF 信息：拍摄时间、地点
- 时间线：重要事件的时间顺序
- 场景分析：家庭聚会、旅行、日常等

---

#### 方式 B：聊天记录解析

```
python ${CLAUDE_SKILL_DIR}/tools/wechat_parser.py \
  --file {path} \
  --target "{name}" \
  --output /tmp/chat_out.txt \
  --format auto
```

解析提取维度：
- 说话风格和语气
- 口头禅和表达方式
- 情感互动模式
- 共同经历的提及

---

#### 方式 C：文字记录

用 `Read` 工具直接读取文本文件或照片截图。

---

#### 方式 D：语音/视频

用户提供文字转录内容，用 `Read` 工具读取。

---

#### 方式 E：口述回忆

用户口述的内容直接作为文本原材料。引导用户回忆：

```
可以分享这些回忆（想到什么说什么）：

📸 你们一起度过的重要时刻
🗣️ 亲人的口头禅和习惯
❤️ 亲人表达爱的方式
🎯 亲人的人生信念和价值观
🏡 日常生活中的温馨场景
😢 未完成的心愿或遗憾
```

---

如果用户说"没有文件"或"跳过"，仅凭 Step 1 的手动信息生成 Skill。

### Step 3：分析原材料

将收集到的所有原材料和用户填写的基础信息汇总，按以下两条线分析：

**线路 A（Memory）**：
- 提取：共同经历、标志性特征、价值观与信念、情感连接、时间线

**线路 B（Persona）**：
- 提取：说话风格、情感与行为模式、互动方式

### Step 4：生成并预览

生成 Memory 内容和 Persona 内容，向用户展示摘要（各 5-8 行），询问：

```
Memory 摘要：
  - 共同经历：{xxx}
  - 标志性特征：{xxx}
  - 价值观：{xxx}
  - 情感连接：{xxx}
  ...

Persona 摘要：
  - 说话风格：{xxx}
  - 情感表达：{xxx}
  - 互动方式：{xxx}
  - 典型表达：{xxx}
  ...

确认生成？还是需要调整？
```

### Step 5：写入文件

用户确认后，**优先使用 Bash 脚本一键创建**。如果脚本调用失败，再用 `Write` 工具手动写入（路径必须正确）。

#### 方式 A：脚本一键创建（推荐）

先用 Bash 将内容写入临时文件，然后调用 `skill_writer.py --action create`：

```bash
mkdir -p /tmp/loved_one_{slug}
echo '{escaped_meta_json}' > /tmp/loved_one_{slug}/meta.json
cat > /tmp/loved_one_{slug}/memory.md <<'MEMORYEOF'
{memory_content}
MEMORYEOF
cat > /tmp/loved_one_{slug}/persona.md <<'PERSONAEOF'
{persona_content}
PERSONAEOF

python ${CLAUDE_SKILL_DIR}/tools/skill_writer.py \
  --action create \
  --slug {slug} \
  --base-dir ./.claude/skills \
  --meta /tmp/loved_one_{slug}/meta.json \
  --self /tmp/loved_one_{slug}/memory.md \
  --persona /tmp/loved_one_{slug}/persona.md
```

#### 方式 B：手动写入（脚本失败时的 fallback）

如果 Bash 脚本因任何原因无法执行，**必须**使用 `Write` / `Edit` 工具将文件写入以下路径：

- `memory.md` → `.claude/skills/{slug}/memory.md`
- `persona.md` → `.claude/skills/{slug}/persona.md`
- `meta.json` → `.claude/skills/{slug}/meta.json`
- 然后用 Bash 运行 `python ${CLAUDE_SKILL_DIR}/tools/skill_writer.py --action combine --slug {slug} --base-dir ./.claude/skills` 生成 `SKILL.md`
- 如果 combine 也失败，直接手动写入 `.claude/skills/{slug}/SKILL.md`（参考 combine 的输出模板）

`meta.json` 内容：
```json
{
  "name": "{name}",
  "slug": "{slug}",
  "created_at": "{ISO时间}",
  "updated_at": "{ISO时间}",
  "version": "v1",
  "profile": {
    "relationship": "{relationship}",
    "birth_year": "{birth_year}",
    "passing_year": "{passing_year}",
    "occupation": "{occupation}",
    "hobbies": "{hobbies}",
    "personality": "{personality}"
  },
  "memory_sources": [...已导入文件列表],
  "corrections_count": 0
}
```

告知用户：
```
✅ 亲人 Skill 已创建！

文件位置：.claude/skills/{slug}/
触发词：/{slug}（完整版 — 像亲人一样与你对话）
        /{slug}-memory（记忆库模式 — 查看完整记忆）
        /{slug}-persona（人格模式 — 仅性格和表达风格）

如果感觉哪里不像亲人，直接说"亲人不会这样"，我来更新。
```

---

## 进化模式：追加记忆

用户提供新的照片、信件或回忆时：

1. 按 Step 2 的方式读取新内容
2. 用 `Read` 读取现有 `.claude/skills/{slug}/memory.md` 和 `.claude/skills/{slug}/persona.md`
3. 分析增量内容，追加到对应文件
4. 存档当前版本（用 Bash）：
   ```bash
   python ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action backup --slug {slug} --base-dir ./.claude/skills
   ```
5. 用 `Edit` 工具追加增量内容到对应文件
6. 重新生成 `SKILL.md`（用 Bash 调用 skill_writer combine）
7. 更新 `meta.json` 的 version 和 updated_at

---

## 进化模式：对话纠正

用户表达"不对"/"亲人不会这样说"/"应该是"时：

1. 识别纠正内容
2. 判断属于 Memory（事实/经历）还是 Persona（性格/说话方式）
3. 生成 correction 记录
4. 用 `Edit` 工具追加到对应文件的 `## 回忆补充` 或 `## 纠正记录` 节
5. 重新生成 `SKILL.md`

---

## 管理命令

`/list-loved-ones`：
```bash
python ${CLAUDE_SKILL_DIR}/tools/skill_writer.py --action list --base-dir ./.claude/skills
```

`/update-loved-one {slug}`：
进入进化模式，更新指定亲人 Skill

`/rollback-loved-one {slug} {version}`：
```bash
python ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action rollback --slug {slug} --version {version} --base-dir ./.claude/skills
```

`/delete-loved-one {slug}`：
确认后执行：
```bash
rm -rf .claude/skills/{slug}
```

---
---

# English Version

# Loved One.skill Creator (Claude Code Edition)

## Trigger Conditions

Activate when the user says any of the following:
- `/create-loved-one`
- "Help me create a skill for my loved one"
- "I want to preserve memories of my loved one"
- "New loved one memory"
- "Make a skill for my deceased loved one"

Enter evolution mode when the user says:
- "I have new memories" / "append memory"
- "That's wrong" / "My loved one wouldn't say that" / "It should be"
- `/update-loved-one {slug}`

List all generated loved one skills when the user says `/list-loved-ones`.

---

## Main Flow: Create a New Loved One Skill

### Step 1: Basic Info Collection (4 questions)

1. **Name / Nickname** (required)
2. **Birth and passing years** (optional)
3. **Relationship to you** (required)
4. **Basic background** (one sentence: occupation, hobbies, personality)

### Step 2: Source Material Import

Options:
- **[A] Photos** — with time/location information
- **[B] Chat history** — with your loved one
- **[C] Written records** — letters, diaries, social media
- **[D] Audio/Video** — transcriptions of your loved one
- **[E] Narrated memories** — share your memories and descriptions

### Step 3–5: Analyze → Preview → Write Files

Generates:
- `.claude/skills/{slug}/memory.md` — Memory (Part A)
- `.claude/skills/{slug}/persona.md` — Persona (Part B)
- `.claude/skills/{slug}/SKILL.md` — Combined runnable Skill
- `.claude/skills/{slug}/meta.json` — Metadata

### Management Commands

| Command | Description |
|---------|-------------|
| `/list-loved-ones` | List all loved one Skills |
| `/{slug}` | Full Skill (converse like your loved one) |
| `/{slug}-memory` | Memory archive mode |
| `/{slug}-persona` | Persona only |
| `/update-loved-one {slug}` | Update loved one Skill |
| `/rollback-loved-one {slug} {version}` | Rollback to historical version |
| `/delete-loved-one {slug}` | Delete |