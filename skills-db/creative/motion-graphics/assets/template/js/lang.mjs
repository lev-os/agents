const LANG = /^[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})*$/;

export function safeLanguage(value) {
  const lang = String(value ?? '');
  if (lang.length > 35 || !LANG.test(lang)) throw new Error(`invalid language label: ${lang}`);
  return lang;
}

export function languageFromQuery(query = '') {
  const lang = new URLSearchParams(query).get('lang');
  return lang === null ? null : safeLanguage(lang);
}
