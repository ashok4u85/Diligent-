# Chinese Simplified (ZH) — Language-Specific QA Rules

**Account:** Diligent Corporation
**Language:** Chinese Simplified (ZH)
**Region:** Mainland China
**Register:** Formal
**Last updated:** April 2026

---

## Character Set — CRITICAL

- **Simplified characters only** — traditional characters are not accepted
- Flag any traditional character immediately as a Critical error
- Common simplified vs traditional pairs to watch:

| Traditional (incorrect) | Simplified (correct) |
|------------------------|---------------------|
| 帳戶 | 账户 |
| 設置 | 设置 |
| 語言 | 语言 |
| 時間 | 时间 |
| 數據 | 数据 |

- **Glossary note:** Preferred term for "account" is **账户** — verify this is used consistently

---

## Punctuation — Full-Width Only

| Full-width (correct) | Half-width (incorrect) |
|---------------------|----------------------|
| ， | , |
| 。 | . |
| ！ | ! |
| ？ | ? |
| ： | : |
| ； | ; |

---

## Ellipsis Convention

- Chinese ellipsis = **……** (double, six dots) — not single `…`
- This is the standard ZH typographic convention — flag single ellipsis as an error

---

## Spacing Rules

- No space between Chinese characters and adjacent punctuation
- No space between Chinese characters and numbers
- No space between Chinese characters and English product names
  - Correct: `Diligent Boards用户` not `Diligent Boards 用户`

---

## Placeholders in Chinese Context

- Placeholder position may shift due to Chinese sentence structure
- Verify translated string reads naturally with placeholder in position
- Do not add spaces around placeholders unless source has them

---

## Glossary — Key Diligent Terms (ZH)

| English | Chinese (approved) |
|---------|-------------------|
| Board | 董事会 / Board |
| Meeting | 会议 |
| Minutes | 会议记录 |
| User | 用户 |
| Account | 账户 (preferred — not 帐户) |
| Settings | 设置 |
| Permissions | 权限 |
| Notification | 通知 |
| Admin | 管理员 |
| Dashboard | Dashboard (untranslated product name) |

---

## Common Errors (Diligent Job History)

- Traditional characters present in simplified Chinese job
- 帐户 used instead of approved term 账户
- Half-width punctuation used instead of full-width
- Single ellipsis … instead of double ……
- Spaces added between Chinese characters and English product names

---

*Refer to `qa-rules/global-rules.md` for placeholder and untranslated term standards.*
