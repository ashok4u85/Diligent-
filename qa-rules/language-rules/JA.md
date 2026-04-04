# Japanese (JA) — Language-Specific QA Rules

**Account:** Diligent Corporation
**Language:** Japanese (JA)
**Region:** Japan
**Register:** Teineigo — desu/masu forms
**Last updated:** April 2026

---

## Register and Politeness

- Use **teineigo** (丁寧語) throughout — desu (です) and masu (ます) forms
- Do not use keigo (敬語) unless source explicitly indicates honorific context
- Do not use casual plain forms (だ/である) in UI strings

---

## Loanwords — CRITICAL

This is a recurring error in Diligent jobs.

- All loanwords must be rendered in **katakana** — not hiragana or romaji
- Examples:

| Incorrect (hiragana) | Incorrect (romaji) | Correct (katakana) |
|---------------------|--------------------|--------------------|
| ぼーど | Bodo | ボード |
| だっしゅぼーど | Dasshubo-do | ダッシュボード |
| ゆーざー | Yu-za- | ユーザー |
| せっている | Settingu | セッティング |

---

## Punctuation — Full-Width Only

Never mix full-width and half-width punctuation in the same string.

| Full-width (correct) | Half-width (incorrect) |
|---------------------|----------------------|
| 。 | . |
| 、 | , |
| 「 」 | " " |
| ！ | ! |
| ？ | ? |
| … | ... |

---

## Line Breaks

- Do not introduce line breaks within a segment unless the source string has one
- Do not remove existing line breaks from source

---

## Placeholder Position

- Japanese sentence structure differs from English — verb comes at the end
- Placeholder position may shift to maintain natural Japanese grammar
- Verify that the translated string makes grammatical sense with the placeholder in its position
- Flag any case where placeholder reordering changes meaning

---

## Glossary — Key Diligent Terms (JA)

| English | Japanese (approved) |
|---------|-------------------|
| Board | 取締役会 / ボード |
| Meeting | 会議 |
| Minutes | 議事録 |
| User | ユーザー |
| Settings | 設定 |
| Permissions | 権限 |
| Notification | 通知 |
| Admin | 管理者 |
| Dashboard | ダッシュボード (untranslated product name) |

---

## Common Errors (Diligent Job History)

- Loanwords in hiragana instead of katakana
- Half-width punctuation mixed with full-width
- Plain form (だ) used instead of desu/masu
- Placeholder position not verified after reordering for grammar

---

*Refer to `qa-rules/global-rules.md` for placeholder and untranslated term standards.*
