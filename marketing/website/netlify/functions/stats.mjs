// Visitor numbers for the private stats page (/stats/#key). GET /api/stats?k=KEY&days=30
// Returns daily totals only (no visitor hashes leave the server).
import { getStore } from "@netlify/blobs";

const KEY = process.env.STATS_KEY || "-2CKCgD-4kBRPhnZ";

export default async (req) => {
  const u = new URL(req.url);
  if (u.searchParams.get("k") !== KEY) return new Response("Not found", { status: 404 });
  const days = Math.min(90, Math.max(1, parseInt(u.searchParams.get("days") || "30", 10)));
  const store = getStore({ name: "stats", consistency: "strong" });
  const now = Date.now() + 2 * 3600e3, out = [];
  const keys = [...Array(days).keys()].map((i) => new Date(now - i * 864e5).toISOString().slice(0, 10));
  const docs = await Promise.all(keys.map((d) => store.get("day-" + d, { type: "json" })));
  docs.forEach((s, i) => {
    if (!s) { out.push({ day: keys[i], visitors: 0, views: 0 }); return; }
    const { v, pv, ...rest } = s;
    out.push({ ...rest, visitors: Object.keys(v || {}).length, productViewers: Object.keys(pv || {}).length });
  });
  return Response.json(out.reverse(), { headers: { "cache-control": "no-store" } });
};

export const config = { path: "/api/stats" };
