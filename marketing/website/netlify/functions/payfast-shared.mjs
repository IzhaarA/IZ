// Shared PayFast settings and helpers (not a function endpoint itself).
export const MERCHANT = { id: "13835135", key: "tqd0ngvfg6lwy" };
export const SITE = "https://makkies.co.za";
export const PROCESS_URL = "https://www.payfast.co.za/eng/process";
export const VALIDATE_URL = "https://www.payfast.co.za/eng/query/validate";
// Same encoding PayFast uses (PHP urlencode): spaces as +, upper-case hex.
export const enc = (s) =>
  encodeURIComponent(String(s)).replace(/%20/g, "+").replace(/[!'()*~]/g, (c) => "%" + c.charCodeAt(0).toString(16).toUpperCase());
export const passphrase = () => (globalThis.Netlify?.env?.get("PAYFAST_PASSPHRASE") ?? process.env.PAYFAST_PASSPHRASE ?? "").trim();
