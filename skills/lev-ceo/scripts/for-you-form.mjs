// The form of a question to JP: the "For you" part of the reply template in ~/.claude/CLAUDE.md.
// A program settles it, with no model. checkForYouForm(reply) finds two faults:
//   bare_list: two or more list lines that hold a question, outside a "For you" section.
//   item_incomplete: a "For you" item that lacks its question mark, its recommendation or its expert lines.
// It does not judge who a question is for, and it does not see an ask that is written as prose.
// This file imports nothing, so a mod can hold a copy of it: the stop hook mod continue-approved imports
// hooks/for-you-form.mjs, because a mod imports only its own files. After a change here, copy the file there.

const FOR_YOU = /^\s*(?:#{1,4}\s*)?\*{0,2}(?:For you|Your turn)\b[^\n]*$/i;
const NEXT_SECTION = /^\s*(?:#{1,4}\s+\S|\*\*[A-Z][^*\n]{1,60}:\*\*|---\s*$)/;
const LIST_QUESTION = /^\s*(?:[-*]|\d+[.)])\s+(?:.*\?\s*(?:\*\*)?\s*$|\*\*[^*\n]*\?\*\*)/;
const RECOMMEND = /\bI recommend\b|\bRecommended?:/i;
/** The label of the expert lines: "What 3 database experts say:", "What 2 products do (...)", "What top experts would do". */
const EXPERTS = /\bWhat\s+\d+\b[^\n]*\b(?:says?|do(?:es)?|shows?)\b|\bWhat\b.*\b(?:experts?|sources?)\b.*\b(?:say|do)\b/i;
const ITEM_START = /^\s{0,3}\d+[.)]\s+/;

/** The reply without fenced code and without quoted lines, so a question in a quote or a log is not counted. */
function plainLines(text) {
  return text.replace(/```[\s\S]*?```/g, "").split("\n").filter((line) => !/^\s*>/.test(line));
}

/**
 * @param {string} text one reply
 * @returns {{ for_you_items: number, bare_questions: number, faults: { fault: "bare_list" | "item_incomplete", count?: number, missing?: string[], first: string }[] }}
 */
export function checkForYouForm(text) {
  const faults = [];
  const items = [];
  const bare = [];
  let inForYou = false;
  let item = null;
  const close = () => { if (item) items.push(item); item = null; };
  for (const line of plainLines(text)) {
    if (FOR_YOU.test(line)) { close(); inForYou = true; continue; }
    if (inForYou && NEXT_SECTION.test(line) && !ITEM_START.test(line) && !/^\s*[-*]\s/.test(line) && !/^\s+\*\*/.test(line)) { close(); inForYou = false; }
    if (inForYou) {
      if (ITEM_START.test(line)) { close(); item = { question: line.trim(), recommend: RECOMMEND.test(line), experts: EXPERTS.test(line) }; continue; }
      if (item) {
        if (RECOMMEND.test(line)) item.recommend = true;
        if (EXPERTS.test(line)) item.experts = true;
      }
      continue;
    }
    if (LIST_QUESTION.test(line)) bare.push(line.trim());
  }
  close();
  if (bare.length >= 2) faults.push({ fault: "bare_list", count: bare.length, first: bare[0].slice(0, 90) });
  for (const it of items) {
    const missing = [!/\?/.test(it.question) && "question mark", !it.recommend && "recommendation", !it.experts && "expert lines"].filter(Boolean);
    if (missing.length) faults.push({ fault: "item_incomplete", missing, first: it.question.slice(0, 90) });
  }
  return { for_you_items: items.length, bare_questions: bare.length, faults };
}
