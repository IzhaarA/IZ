// PayFast's payment confirmation (ITN). PayFast calls this after every payment.
// We check the signature, confirm the payment with PayFast directly, record it and email the shop.
import crypto from "node:crypto";
import { getStore } from "@netlify/blobs";
import { MERCHANT, SITE, VALIDATE_URL, enc, passphrase } from "./payfast-shared.mjs";

export default async (req) => {
  if (req.method !== "POST") return new Response("OK");
  const raw = await req.text();
  const params = new URLSearchParams(raw);

  // 1) signature: every field up to "signature", in the order received
  let str = "";
  for (const [k, v] of params) { if (k === "signature") break; str += k + "=" + enc(v.trim()) + "&"; }
  str = str.slice(0, -1);
  const pass = passphrase();
  const check = crypto.createHash("md5").update(pass ? str + "&passphrase=" + enc(pass) : str).digest("hex");
  const sigOk = check === (params.get("signature") || "");

  // 2) ask PayFast to confirm this notification is genuine
  let valid = false;
  try {
    const r = await fetch(VALIDATE_URL, { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body: str });
    valid = (await r.text()).trim() === "VALID";
  } catch {}

  const ok = sigOk && valid && params.get("merchant_id") === MERCHANT.id;
  const status = params.get("payment_status") || "";
  const rec = {
    order_no: params.get("m_payment_id") || "",
    status: ok ? status : "NOT VERIFIED (" + status + ")",
    amount: params.get("amount_gross") || "",
    fee: params.get("amount_fee") || "",
    net: params.get("amount_net") || "",
    pf_payment_id: params.get("pf_payment_id") || "",
    customer: [params.get("name_first"), params.get("name_last")].filter(Boolean).join(" "),
    email: params.get("email_address") || "",
    paid_at: new Date().toISOString(),
  };

  // 3) keep a record (Netlify storage) and show it in Netlify Forms -> "payments"
  try { await getStore("payments").setJSON(rec.order_no + "-" + rec.pf_payment_id, rec); } catch {}
  try {
    await fetch(SITE + "/", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({ "form-name": "payments", ...rec }).toString() });
  } catch {}
  // 4) email the shop
  try {
    await fetch("https://formsubmit.co/ajax/orders@makkies.co.za", { method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json", Origin: SITE, Referer: SITE + "/" },
      body: JSON.stringify({ _subject: (ok && status === "COMPLETE" ? "PAID " : "PAYMENT " + rec.status + " ") + rec.order_no + " — R" + rec.amount,
        _template: "table", _captcha: "false", ...rec }) });
  } catch {}
  return new Response("OK");
};

export const config = { path: "/api/payfast-itn" };
