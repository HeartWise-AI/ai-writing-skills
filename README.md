# AI Writing Skills

A collection of skills for AI-assisted academic and research writing in medical AI, following the [Agent Skills specification](https://agentskills.io/specification).

## Skills

### 1. Protocol Writing (`protocol-writing/`)
Comprehensive guide for writing clinical research protocols for AI-based diagnostic studies, validation trials, and retrospective analyses.

**Includes:**
- 16-section protocol structure
- Style guidelines
- Section length reference
- Submission checklist

### 2. Manuscript Writing (`manuscript-writing/`)
Full section-by-section guide for writing a medical AI manuscript from scratch.

**Includes:**
- All sections: Title, Abstract, Introduction, Methods, Results, Discussion
- Threshold reporting requirements for binary classification models
- Table and figure templates
- Submission checklist

### 3. Manuscript Writing - TRIPOD-AI (`manuscript-writing-tripod/`)
Guidelines for writing AI papers following TRIPOD+AI reporting standards.

**Includes:**
- Results section structure
- Table templates with mandatory threshold reporting (Youden Index / binary classification)
- Visual presentation best practices
- Transparency requirements

### 4. Manuscript Review (`manuscript-review/`)
Section-by-section checklist for reviewing medical AI manuscripts.

**Includes:**
- Background, Methods, Results, Tables, Discussion, and Abstract checklists
- Success criteria for each section, including threshold reporting checks for binary classification
- Numerical formatting rules
- Forbidden patterns reference

### 5. CIHR Grant Writing (`cihr-grant-writing/`)
Section-by-section guide for writing CIHR Project Grant applications.

**Includes:**
- Full section-by-section structure (Need, Design, Management, General Considerations)
- Weighted scoring rubrics for each subsection
- Fill-in-the-blank templates
- Reference appendices for CIHR-specific language, study type adaptation, and common reviewer critiques

---

## Directory Structure

Each skill follows the [Agent Skills spec](https://agentskills.io/specification) format:

```
ai-writing-skills/
├── protocol-writing/
│   └── SKILL.md
├── manuscript-writing/
│   └── SKILL.md
├── manuscript-writing-tripod/
│   └── SKILL.md
├── manuscript-review/
│   └── SKILL.md
├── cihr-grant-writing/
│   ├── SKILL.md
│   └── references/
│       └── APPENDICES.md
└── README.md
```

Each `SKILL.md` contains:
- YAML frontmatter with `name` and `description`
- Markdown body with full skill instructions

---

## Installation

### Claude Code (Slash Commands)

Install as global slash commands available in every project.

**1. Create the commands directory:**

```bash
mkdir -p ~/.claude/commands
```

**2. Copy each skill's SKILL.md as a command file:**

```bash
cp protocol-writing/SKILL.md ~/.claude/commands/protocol-writing.md
cp manuscript-writing-tripod/SKILL.md ~/.claude/commands/manuscript-writing-tripod.md
cp manuscript-review/SKILL.md ~/.claude/commands/manuscript-review.md
cp cihr-grant-writing/SKILL.md ~/.claude/commands/cihr-grant-writing.md
```

**3. Use them anywhere in Claude Code:**

```
/protocol-writing
/manuscript-writing-tripod
/manuscript-review
/cihr-grant-writing
```

> **Note:** For project-specific commands, place the files in `.claude/commands/` inside your project directory instead.

### Claude Desktop / Claude.ai (Skills Upload)

**1.** Package each skill as a ZIP file:

```bash
zip -r protocol-writing.zip protocol-writing/
zip -r manuscript-writing-tripod.zip manuscript-writing-tripod/
zip -r manuscript-review.zip manuscript-review/
zip -r cihr-grant-writing.zip cihr-grant-writing/
```

**2.** In Claude, go to **Settings > Capabilities**.

**3.** Upload each ZIP file as a Skill.

**4.** Enable the skills and use them in conversations.

### Claude Desktop (Projects)

Claude Desktop uses **Projects** to store reusable instructions and knowledge.

**1.** Open Claude Desktop and go to **Projects** (left sidebar).

**2.** Create a new project (e.g., "Academic Writing Skills").

**3.** Add each skill's `SKILL.md` as project knowledge:
- Click **"Add content"** in the project knowledge section
- Select **"Add text content"** (or drag and drop the file)
- Add each `SKILL.md` as a separate knowledge entry

**4.** (Optional) Add project instructions:

```
You are an academic writing assistant specializing in medical AI research.
When the user asks you to write or review a protocol, manuscript, or grant,
use the relevant skill from the project knowledge to guide your output.
Always follow the structure, style guidelines, and checklists provided.
For manuscript reviews, use the section-by-section checklist approach.
```

**5.** Start a new conversation within that project to use the skills.

---

### ChatGPT / Codex (Custom GPTs or System Prompts)

#### Option A: Custom GPT (Persistent)

**1.** Go to [https://chat.openai.com/gpts/editor](https://chat.openai.com/gpts/editor)

**2.** Create a new GPT with the following settings:

- **Name:** Academic Writing Assistant
- **Description:** Helps write research protocols, TRIPOD-AI manuscripts, and CIHR grant applications
- **Instructions:** Paste the following system prompt:

```
You are an academic writing assistant specializing in medical AI research.
You have access to four writing skills as knowledge files.
When the user asks you to write or review a protocol, use "protocol-writing/SKILL.md".
When the user asks you to write a manuscript, use "manuscript-writing-tripod/SKILL.md".
When the user asks you to review a manuscript, use "manuscript-review/SKILL.md".
When the user asks you to write or review a CIHR grant, use "cihr-grant-writing/SKILL.md".
Always follow the structure, style guidelines, scoring rubrics, and checklists provided in each skill.
```

**3.** Upload the 4 `SKILL.md` files under the **"Knowledge"** section.

**4.** Save and use the GPT.

#### Option B: ChatGPT Projects (Simpler)

**1.** In ChatGPT, create a new **Project** (left sidebar).

**2.** Add each `SKILL.md` file to the project's **Files** section.

**3.** Add project instructions (same as the system prompt above).

**4.** Start a conversation within the project.

#### Option C: Paste into a Single Conversation

If you don't need persistence, simply paste the contents of the relevant `SKILL.md` file at the start of any ChatGPT conversation.

---

### Notion

#### Option A: Dedicated Database

**1.** Create a new Notion database called "AI Writing Skills".

**2.** Add the following properties:
- **Name** (Title) -- the skill name
- **Category** (Select) -- Protocol / Manuscript / Grant
- **Tags** (Multi-select) -- e.g., TRIPOD-AI, CIHR, Diagnostic AI

**3.** Create one page per skill:

| Name | Category | Tags |
|------|----------|------|
| Protocol Writing | Protocol | Diagnostic AI, Validation |
| TRIPOD-AI Manuscript Writing | Manuscript | TRIPOD-AI, Reporting |
| Manuscript Review | Review | Checklist, Quality Control |
| CIHR Grant Writing | Grant | CIHR, RCT, AI/Technology |

**4.** In each page, paste the full contents of the corresponding `SKILL.md` file.

#### Option B: Single Page with Toggles

**1.** Create a new Notion page called "AI Writing Skills".

**2.** Add 4 toggle headings:

- **Protocol Writing** -- paste contents of `protocol-writing/SKILL.md`
- **TRIPOD-AI Manuscript Writing** -- paste contents of `manuscript-writing-tripod/SKILL.md`
- **Manuscript Review** -- paste contents of `manuscript-review/SKILL.md`
- **CIHR Grant Writing** -- paste contents of `cihr-grant-writing/SKILL.md`

#### Option C: Notion AI Integration

If you have **Notion AI** enabled:

**1.** Add the skills as pages (Option A or B above).

**2.** When using Notion AI, reference the skill page:
- Type `@Protocol Writing` to link the page
- Then ask Notion AI to "write a protocol following the structure in @Protocol Writing"

---

## Packaging Skills as ZIP Files

To distribute or share individual skills:

```bash
# Package each skill directory into a ZIP
zip -r protocol-writing.zip protocol-writing/
zip -r manuscript-writing-tripod.zip manuscript-writing-tripod/
zip -r manuscript-review.zip manuscript-review/
zip -r cihr-grant-writing.zip cihr-grant-writing/
```

Each ZIP should contain the skill folder as its root:

```
protocol-writing.zip
  └── protocol-writing/
      └── SKILL.md

cihr-grant-writing.zip
  └── cihr-grant-writing/
      ├── SKILL.md
      └── references/
          └── APPENDICES.md
```

---

## Quick Reference

| Skill | Directory | Claude Code | Claude Skills | ChatGPT | Notion |
|-------|-----------|-------------|---------------|---------|--------|
| Protocol Writing | `protocol-writing/` | `/protocol-writing` | ZIP upload | GPT knowledge | Database page |
| TRIPOD-AI Manuscript | `manuscript-writing-tripod/` | `/manuscript-writing-tripod` | ZIP upload | GPT knowledge | Database page |
| Manuscript Review | `manuscript-review/` | `/manuscript-review` | ZIP upload | GPT knowledge | Database page |
| CIHR Grant Writing | `cihr-grant-writing/` | `/cihr-grant-writing` | ZIP upload | GPT knowledge | Database page |

---

## License

MIT License - HeartWise.AI

## Version

v2.0.0 - Refactored to Agent Skills spec format (SKILL.md + directory structure + ZIP packaging)
