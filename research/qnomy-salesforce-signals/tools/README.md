# Tools for repeating the sweep

- `legistar_sweep.sh`: queries the Legistar Web API for council matters with "Salesforce" in the title, for each client in `legistar_clients.txt`. Edit the term and date in the script. Run it from the directory that contains `legistar_clients.txt`.
- `vendor_probe.js`: renders a booking page in headless Chromium and reports the hosts contacted and any queue/booking vendor signatures (Qmatic, JRNI, Engageware/TimeTrade, Qminder, QLess, Wavetec, Q-Flow, Salesforce Lightning Scheduler, Calendly, Bookings). Needs `npm i playwright`. Usage: `node vendor_probe.js <url>`.

Keep request rates low and respect site terms.
