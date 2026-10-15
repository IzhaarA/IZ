// Builds the PayFast payment form fields and signs them on the server,
// so the passphrase (if one is set) never reaches the customer's browser.
import crypto from "node:crypto";
import { MERCHANT, SITE, PROCESS_URL, enc, passphrase } from "./payfast-shared.mjs";

// Fields PayFast accepts, in the order PayFast requires for the signature.
const ORDER = ["merchant_id", "merchant_key", "return_url", "cancel_url", "notify_url",
  "name_first", "name_last", "email_address", "cell_number",
  "m_payment_id", "amount", "item_name", "item_description", "custom_str1",
  "email_confirmation", "confirmation_address"];

export default async (req) => {
  if (req.method !== "POST") return new Response("Method not allowed", { status: 405 });
  let body;
  try { body = await req.json(); } catch { return new Response("Bad request", { status: 400 }); }
  if (!body || !Array.isArray(body.fields)) return new Response("Bad request", { status: 400 });

  const given = new Map();
  for (const f of body.fields) if (Array.isArray(f) && ORDER.includes(f[0])) given.set(f[0], String(f[1] ?? "").trim());
  // our own merchant account and confirmation address, whatever the browser sent
  given.set("merchant_id", MERCHANT.id);
  given.set("merchant_key", MERCHANT.key);
  given.set("notify_url", SITE + "/api/payfast-itn");
  if (!/^\d+(\.\d{2})$/.test(given.get("amount") || "") || Number(given.get("amount")) <= 0) return new Response("Bad amount", { status: 400 });

  const fields = ORDER.filter((k) => given.has(k) && given.get(k) !== "").map((k) => [k, given.get(k)]);
  let str = fields.map(([k, v]) => k + "=" + enc(v)).join("&");
  const pass = passphrase();
  if (pass) str += "&passphrase=" + enc(pass);
  const signature = crypto.createHash("md5").update(str).digest("hex");
  return Response.json({ action: PROCESS_URL, fields, signature });
};

export const config = { path: "/api/payfast-sign" };
