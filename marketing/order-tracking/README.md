# Order tracking for makkies.co.za

Every checkout is saved to a Google Sheet:
- **Orders**: one row per order, with a Status dropdown (New, Paid, Packed, Sent, Collected, Cancelled).
- **Items**: one row per product bought.
- **Best sellers**: quantity and sales per product, plus sales per month. It updates itself.

## Set-up (about 10 minutes, once)

1. Go to sheets.new and name the sheet **Makkie Orders**.
2. Open **Extensions → Apps Script**, delete what's there, paste in all of `Code.gs`, and click **Save**.
3. Click **Deploy → New deployment**. Click the gear and choose **Web app**.
   - Execute as: **Me**
   - Who has access: **Anyone**
   - Click **Deploy**, then **Authorise access** and allow it. Google may show "unverified app": click Advanced, then Go to project.
4. Copy the **Web app URL**. It ends in `/exec`.
5. Make the website change in `website-snippet.js`: add the URL to CONFIG, paste the `logOrder` function, and add `logOrder(o);` in `placeOrder`.
6. Place a test order on the site. A row should appear in the sheet within a few seconds. Delete the test rows afterwards.

If you later edit `Code.gs`, use **Deploy → Manage deployments → Edit → New version** so the same URL keeps working.
