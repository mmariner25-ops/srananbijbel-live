import Reader from './Reader';

export default function Page() {
  return (
    <>
      <Reader />
      <footer className="border-t border-current/10 py-4 text-center text-xs text-current/45">
        <a
          href="/privacy"
          className="underline underline-offset-2 transition-opacity hover:opacity-80 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
          aria-label="Privacybeleid / Privacy Policy"
        >
          Privacybeleid / Privacy Policy
        </a>
      </footer>
    </>
  );
}
