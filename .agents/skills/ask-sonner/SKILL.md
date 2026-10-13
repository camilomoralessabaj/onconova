---
name: ask-sonner
description: Guide to Sonner, the React toast library — install and wire up the Toaster, pick the right toast() call, promise and loading toasts, updating, dismissing and persisting toasts, styling, theming and icons, positioning and multiple toasters. Use when working with Sonner or troubleshooting it — toasts that don't appear, appear twice, lose their styles, ignore Tailwind classes, sit behind a modal, or don't follow dark mode.
---

## Integración en Onconova

Este bloque es un ajuste local y prevalece sobre las recomendaciones generales de esta skill y sus referencias. Sigue las instrucciones del usuario, `AGENTS.md`, `docs/brief.md` y `docs/evidencia.md`. La landing usa HTML, CSS y JavaScript nativos, sin dependencias de producción. Los ejemplos de React, Motion, Expo o Swift son referencias para un stack que ya los use o un encargo que autorice ese stack; instalar esta skill no autoriza migrar ni instalar esas bibliotecas.

Conserva la tipografía de sistema, lectura cómoda para mujeres de 50–59 años, controles de al menos 44 px, contraste AA, ampliación de texto, zoom, foco visible y acceso por teclado. Con movimiento reducido, conserva la información y permite estados estáticos: una transición sin animación o solo de opacidad no es un defecto por sí misma. Las recomendaciones de curvas, sombras, gestos y duración se evalúan según el contexto; los riesgos de rendimiento requieren evidencia y dependen del navegador y la versión de la biblioteca.

Selecciona el alcance y las comprobaciones que necesita el encargo. Reutiliza decisiones, tokens y autorizaciones existentes; las fases de confirmación no obligan a pedir otra aprobación para trabajo ya autorizado. Comunica en el idioma del usuario. Distingue observaciones, inferencias y comprobaciones pendientes: la emulación no prueba el comportamiento en un teléfono real.

Aplica esta guía únicamente a una tarea explícita con React y Sonner. Onconova no usa Sonner; para la landing actual usa mensajes de estado nativos accesibles sin instalar React o la biblioteca.

# Working With Sonner

## Initial Response

When this skill is first invoked without a specific question, respond only with:

> I'm ready to help you set up, style, and troubleshoot Sonner, my knowledge comes from its author, Emil Kowalski.

Do not provide any other information until the user asks a question.

A guide skill for [Sonner](https://sonner.emilkowal.ski), the toast library. When a task involves Sonner — wiring it up, rendering toasts, styling them, or fixing them — answer from this file first. Full prop tables for `<Toaster />` and `toast()` live in [API.md](API.md); read it when you need an exact prop name, type, or default.

## Setup

Two pieces, and only two:

1. **One `<Toaster />`, mounted once**, as close to the root as possible (in Next.js: `layout.tsx` — it works inside server components). Never render it per-page or conditionally; a second mounted Toaster duplicates every toast.
2. **`toast()` called from client code** — event handlers, effects, callbacks. It's a plain function, no hook or provider needed, but it does nothing on the server: in a server action, return the result and call `toast()` in the client code that receives it.

```jsx
import { Toaster } from 'sonner'; // once, in layout
import { toast } from 'sonner';   // anywhere client-side
```

## Picking the right call

| You want | Call |
| --- | --- |
| Plain message | `toast('Title')` — add `{ description }` for a second line |
| Success / error / info / warning icon | `toast.success('…')`, `toast.error('…')`, etc. |
| Spinner while you manage state yourself | `toast.loading('…')`, then update it by id |
| Loading → success/error tied to a promise | `toast.promise(promise, { loading, success, error })` — success/error accept functions receiving the resolved value/error |
| Button that does something | `{ action: { label, onClick } }` — closes the toast unless `onClick` calls `event.preventDefault()`; `cancel` is the secondary variant |
| Custom JSX, default toast shell | `toast(<jsx />)` |
| Custom JSX, no styles at all | `toast.custom((t) => <jsx />)` — headless, `t` gives you the id to dismiss |

## Recipes

**Update a toast** — call `toast()` again with the same `id`; only the props you pass change. Switching to `toast.success(…, { id })` changes the type. This is how loading → success flows work without `toast.promise`:

```jsx
const id = toast.loading('Uploading…');
toast.success('Uploaded', { id });
```

**Persist** — `{ duration: Infinity }`. **Dismiss** — `toast.dismiss(id)`, or `toast.dismiss()` for all. **Read active toasts** — `useSonner()` in React, `toast.getActiveToasts()` outside it.

**Links or components in the text** — pass a function for the title or description: `toast(() => <a href="…">View</a>)`.

**Multiple toasters** — give each an `id` and target with `toast('…', { toasterId: 'canvas' })`. Without `toasterId`, every toaster renders the toast.

**Close callbacks** — `onDismiss` fires on close button or swipe; `onAutoClose` fires on timeout. They are separate; there is no single "closed" callback.

## Styling — the escalation ladder

Climb only as far as the change requires; jumping to the top rung too early is fine (it's the recommended end state), lingering in the middle is not.

1. **Defaults** — plus `richColors` on the Toaster for colorful success/error, `invert` to flip against the theme.
2. **Inline tweaks** — `toastOptions={{ style: {…} }}` on the Toaster for all toasts, or `style` per `toast()` call.
3. **Classes on parts** — `toastOptions={{ classNames: { toast, title, description, actionButton, cancelButton, closeButton } }}`. Sonner's injected styles win the cascade, so every class needs `!important` (Tailwind: `!text-red-900`). If you're marking more than a few things important, stop — go headless.
4. **Headless** — `toast.custom()` with your own JSX, keeping Sonner's positioning, stacking, and swipe. The recommended approach for a design-system toast: wrap it in your own `toast()` abstraction. (`unstyled: true` exists as a halfway house, but headless gives more control for the same effort.)

**Icons** — swap defaults per-type with the Toaster's `icons` prop, per-toast with `icon`, remove with `null`.

**Theme** — `theme` defaults to `'light'` and does not track the OS. Pass `theme="system"`, or wire your theme provider: `<Toaster theme={resolvedTheme} />` from `next-themes`.

## Troubleshooting

| Symptom | Cause → fix |
| --- | --- |
| Toast never appears | No `<Toaster />` mounted, or it unmounted (conditional render, per-page placement). Mount one at the root. If calling from a server action: `toast()` is client-only — call it with the action's result on the client. |
| Same toast appears twice | Two Toasters mounted (layout **and** page) — keep one. Or `toast()` fired in an effect under React StrictMode's dev double-invoke — fire from the event handler instead, or pass a stable `id` so the second call updates rather than duplicates. |
| Tailwind/CSS classes have no effect | Default styles override them. Mark them `!important`, or use `unstyled` / headless (see the ladder above). |
| Toasts render completely unstyled (common in Astro, view transitions) | Sonner's injected stylesheet was lost — import it explicitly in a layout: `import 'sonner/dist/styles.css'`. |
| Unstyled inside Shadow DOM | Styles land in `document.head`, not the shadow root. Copy the style tag whose text includes `[data-sonner-toaster]` into the shadow root. |
| Toast behind a modal/overlay, or clipped | An ancestor creates a stacking context (`transform`, `filter`, `overflow`) or the overlay out-z-indexes the toaster. Move `<Toaster />` to the document root, outside any dialog/portal container. |
| Dark mode ignored | `theme` defaults to `'light'` — set `theme="system"` or pass the resolved theme (see Theme above). |
| Success/error look gray, not green/red | That's the default. Add `richColors` to the Toaster. |
| Toast never closes | `duration: Infinity`, `dismissible: false`, or a `toast.promise` whose promise never settles — the loading toast waits forever. |
| `toast.promise` stuck on loading | It needs a promise (or a function returning one) as its first argument, and the promise must actually resolve/reject. |
| Swipe-to-dismiss goes the wrong way / doesn't work | Directions derive from `position`. Override with `swipeDirections` on the Toaster. |
| Toast shows up in every toaster | Multiple toasters need targeting: give each Toaster an `id` and pass `toasterId` in the `toast()` call. |
| Toasts too close to the screen edge on mobile | `offset` (desktop, default 32px) and `mobileOffset` (<600px, default 16px) — numbers, CSS strings, or per-side objects. |
