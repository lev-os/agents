# Device Code Verification UI

> The verification page is where users enter the code displayed by their CLI
> to link the CLI session to their web account. This page must work on phones,
> tablets, and desktops — because the user may be SSH'd into a server and
> opening the URL on a completely different device.

## Page Requirements

1. **Require authentication** — redirect to login first
2. **Accept code from URL** — `?code=ABCD1234` auto-fills and auto-submits
3. **Normalize input** — strip dashes, uppercase, ignore whitespace
4. **Instant feedback** — loading, success, error states
5. **Mobile-friendly** — the user may be typing on a phone while reading a terminal

## Route Structure

```
/verify/
├── page.tsx           # Server component: auth check + code from URL
└── VerifyCodeForm.tsx # Client component: form + mutation
```

## Server Component (page.tsx)

```tsx
import { redirect } from "next/navigation";
import { getAuthenticatedUser } from "@/lib/auth";
import { VerifyCodeForm } from "./VerifyCodeForm";

export default async function VerifyPage({
    searchParams,
}: {
    searchParams: Promise<{ code?: string }>;
}) {
    // Require authentication
    const user = await getAuthenticatedUser();
    if (!user) {
        const params = await searchParams;
        const code = params.code ?? "";
        redirect(`/login?next=/verify${code ? `?code=${code}` : ""}`);
    }

    const { code } = await searchParams;

    return (
        <main className="min-h-screen flex items-center justify-center p-4">
            <div className="w-full max-w-md space-y-6">
                <h1 className="text-2xl font-bold text-center">
                    Link Your CLI
                </h1>
                <p className="text-muted-foreground text-center">
                    Enter the code shown in your terminal
                </p>
                <VerifyCodeForm initialCode={code} />
            </div>
        </main>
    );
}
```

## Client Component (VerifyCodeForm.tsx)

```tsx
"use client";

import { useState, useEffect, useCallback } from "react";
import { useMutation } from "@tanstack/react-query";

function normalizeCode(input: string): string {
    return input.replace(/[^A-Za-z0-9]/g, "").toUpperCase();
}

function formatCode(normalized: string): string {
    if (normalized.length <= 4) return normalized;
    return `${normalized.slice(0, 4)}-${normalized.slice(4, 8)}`;
}

export function VerifyCodeForm({ initialCode }: { initialCode?: string }) {
    const [rawInput, setRawInput] = useState("");
    const [autoSubmitted, setAutoSubmitted] = useState(false);

    const mutation = useMutation({
        mutationFn: async (userCode: string) => {
            const response = await fetch("/api/v1/auth/device-verify", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_code: userCode }),
            });

            if (!response.ok) {
                const body = await response.json();
                throw new Error(body.error?.message ?? "Verification failed");
            }

            return response.json();
        },
    });

    const submit = useCallback(
        (code: string) => {
            const normalized = normalizeCode(code);
            if (normalized.length === 8 && !mutation.isPending) {
                mutation.mutate(normalized);
            }
        },
        [mutation]
    );

    // Auto-submit if code comes from URL
    useEffect(() => {
        if (initialCode && !autoSubmitted) {
            const normalized = normalizeCode(initialCode);
            if (normalized.length === 8) {
                setRawInput(formatCode(normalized));
                setAutoSubmitted(true);
                submit(normalized);
            }
        }
    }, [initialCode, autoSubmitted, submit]);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const normalized = normalizeCode(e.target.value);
        setRawInput(formatCode(normalized.slice(0, 8)));
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        submit(rawInput);
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            <input
                type="text"
                value={rawInput}
                onChange={handleChange}
                placeholder="ABCD-1234"
                className="w-full text-center text-3xl tracking-widest font-mono
                           border rounded-lg p-4 uppercase"
                maxLength={9} // 8 chars + 1 dash
                autoFocus
                autoComplete="off"
                spellCheck={false}
            />

            <button
                type="submit"
                disabled={normalizeCode(rawInput).length !== 8 || mutation.isPending}
                className="w-full py-3 bg-primary text-primary-foreground rounded-lg
                           font-semibold disabled:opacity-50"
            >
                {mutation.isPending ? "Verifying..." : "Verify Code"}
            </button>

            {mutation.isSuccess && (
                <div className="p-4 bg-green-50 border border-green-200 rounded-lg text-center">
                    <p className="font-semibold text-green-800">
                        CLI linked successfully!
                    </p>
                    <p className="text-sm text-green-600 mt-1">
                        Return to your terminal — it should log you in automatically.
                    </p>
                </div>
            )}

            {mutation.isError && (
                <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-center">
                    <p className="font-semibold text-red-800">
                        {mutation.error.message}
                    </p>
                    <p className="text-sm text-red-600 mt-1">
                        Check the code and try again, or run{" "}
                        <code className="font-mono">my-cli login</code> to get a new code.
                    </p>
                </div>
            )}
        </form>
    );
}
```

## UX Design Decisions

### Why auto-submit from URL?

When the CLI provides `verification_url_complete`, the user just clicks the link.
If the code is valid and they're logged in, it submits immediately with zero
interaction needed. This is the golden path for device code flow.

### Why large monospace input?

The user is reading a code from a terminal (possibly on another screen or device).
Large, monospace, widely-tracked characters minimize transcription errors.

### Why strip non-alphanumeric on input?

Users may type the dash from the formatted code. The dash is display-only.
By normalizing input, we accept `ABCD-1234`, `ABCD1234`, `abcd 1234`, `abcd.1234`, etc.

### Why uppercase?

The ambiguity-safe alphabet is all uppercase. Uppercasing input means the user
doesn't need to think about case. `abcd1234` works just as well as `ABCD1234`.

## Mobile Considerations

The verification page must work well on phones because:
- User is SSH'd into a remote server on their laptop
- They open the verification URL on their phone
- They type the 8-character code on a phone keyboard

Key mobile requirements:
- Large touch targets (minimum 44px)
- `inputMode="text"` (not `numeric` — code contains letters)
- Auto-capitalize on mobile keyboards
- No zoom on input focus (font-size >= 16px)
