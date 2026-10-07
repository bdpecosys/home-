const { chromium } = require('playwright');
(async () => {
  const url = process.argv[2];
  const b = await chromium.launch({ executablePath: 'process.env.CHROME_PATH || "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"', args:['--no-sandbox'] });
  const p = await b.newPage({ userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36' });
  const hosts = new Map();
  p.on('request', r => { try { const h = new URL(r.url()).host; hosts.set(h,(hosts.get(h)||0)+1);} catch{} });
  const re = /(qmatic|orchestra|jrni|bookingbug|timetrade|engageware|wavetec|qminder|qless|qflow|q-nomy|qnomy|lightning:?scheduler|salesforce.?scheduler|lxi?Scheduler|serviceappointment|ServiceTerritory|WorkTypeGroup|calendly|acuity|outlook\.office|bookings)/ig;
  const hits = new Map();
  p.on('response', async r => { try { const ct = r.headers()['content-type']||''; if(!/json|javascript|html/.test(ct)) return; const t = await r.text(); for (const m of t.matchAll(re)) hits.set(m[0].toLowerCase(), (hits.get(m[0].toLowerCase())||0)+1);} catch{} });
  try { await p.goto(url, { waitUntil: 'networkidle', timeout: 60000 }); } catch(e) { console.log('nav', e.message.slice(0,100)); }
  await p.waitForTimeout(5000);
  console.log('FINAL', p.url());
  console.log('HOSTS', [...hosts.entries()].sort((a,b)=>b[1]-a[1]).map(x=>x.join(':')).join(' '));
  console.log('HITS', JSON.stringify([...hits.entries()]));
  const txt = (await p.innerText('body').catch(()=>''))||''; console.log('TEXT', txt.replace(/\s+/g,' ').slice(0,1200));
  await b.close();
})();
