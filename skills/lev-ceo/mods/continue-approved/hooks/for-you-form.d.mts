// The types of for-you-form.mjs, for the type check of register.ts.
export type FormFault = { fault: 'bare_list' | 'item_incomplete', count?: number, missing?: string[], first: string }
export function checkForYouForm(text: string): { for_you_items: number, bare_questions: number, faults: FormFault[] }
