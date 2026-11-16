// Visitor tracking for makkies.co.za (no cookies, no personal details stored).
// POST /api/t  {e: event, p: page/product/category, q: search, r: referrer, u: utm_source}
// Events: view (page opened), product, cat, search, add, checkout, order, wa (WhatsApp button)
// A visitor is counted once per day from a one-way hash of IP + browser + date; the IP itself is never stored.
// Counts are kept per day in the "stats" blob store: one JSON document per day.
import { getStore } from "@netlify/blobs";

const BOT = /bot|crawl|spider|slurp|preview|facebookexternalhit|whatsapp\/|headless|lighthouse|pingdom|monitor|curl|python|wget|playwright/i;
const EVENTS = new Set(["view", "product", "cat", "search", "add", "checkout", "order", "wa"]);
const clip = (s, n = 80) => String(s || "").replace(/[\u0000-\u001f]/g, "").slice(0, n);

function source(ua, ref, utm) {
  if (utm) return clip(utm, 30).toLowerCase();
  if (/musical_ly|bytedance|tiktok/i.test(ua)) return "tiktok";
  if (/instagram/i.test(ua)) return "instagram";
  if (/FBAN|FBAV|FB_IAB/i.test(ua)) return "facebook";
  let h = "";
  try { h = new URL(ref).hostname.replace(/^www\./, ""); } catch (e) {}
  if (!h || h.endsWith("makkies.co.za")) return "direct / WhatsApp";
  if (/google\./.test(h)) return "google";
  if (/bing\.|duckduckgo|yahoo/.test(h)) return "other search";
  if (/facebook|fb\.com/.test(h)) return "facebook";
  if (/instagram/.test(h)) return "instagram";
  if (/tiktok/.test(h)) return "tiktok";
  if (/whatsapp|wa\.me/.test(h)) return "whatsapp";
  return clip(h, 40);
}

async function hash(s) {
  const b = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
  return [...new Uint8Array(b)].slice(0, 8).map((x) => x.toString(16).padStart(2, "0")).join("");
}

const inc = (o, k, n = 1) => { if (k) o[k] = (o[k] || 0) + n; };

export default async (req) => {
  if (req.method !== "POST") return new Response(null, { status: 405 });
  const ua = req.headers.get("user-agent") || "";
  if (BOT.test(ua)) return new Response(null, { status: 204 });
  let d = {};
  try { d = JSON.parse(await req.text()); } catch (e) { return new Response(null, { status: 400 }); }
  const e = String(d.e || "");
  if (!EVENTS.has(e)) return new Response(null, { status: 400 });

  // South African date (UTC+2)
  const day = new Date(Date.now() + 2 * 3600e3).toISOString().slice(0, 10);
  const ip = req.headers.get("x-nf-client-connection-ip") || req.headers.get("x-forwarded-for") || "";
  const vid = await hash(ip + "|" + ua + "|" + day + "|makkies");
  const mobile = /mobi|android|iphone/i.test(ua);

  const store = getStore({ name: "stats", consistency: "strong" });
  for (let attempt = 0; attempt < 8; attempt++) {
    const cur = await store.getWithMetadata("day-" + day, { type: "json" });
    const s = (cur && cur.data) || { day, views: 0, v: {}, src: {}, dev: {}, page: {}, product: {}, cat: {}, search: {}, add: {}, checkout: 0, order: 0, wa: 0, pv: {} };
    const isNew = !s.v[vid];
    if (isNew) { s.v[vid] = 1; inc(s.src, source(ua, d.r, d.u)); inc(s.dev, mobile ? "phone" : "computer"); }
    if (e === "view") { s.views++; inc(s.page, clip(d.p, 60) || "/"); }
    else if (e === "product") { inc(s.product, clip(d.p, 60)); s.pv[vid] = 1; }
    else if (e === "cat") inc(s.cat, clip(d.p, 60));
    else if (e === "search") inc(s.search, clip(d.q, 40).toLowerCase());
    else if (e === "add") inc(s.add, clip(d.p, 60));
    else if (e === "checkout") s.checkout++;
    else if (e === "order") s.order++;
    else if (e === "wa") s.wa++;
    const res = await store.setJSON("day-" + day, s, cur ? { onlyIfMatch: cur.etag } : { onlyIfNew: true });
    if (res.modified) return new Response(null, { status: 204 });
  }
  return new Response(null, { status: 503 });
};

export const config = { path: "/api/t" };
