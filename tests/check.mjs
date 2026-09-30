import {readFileSync} from 'node:fs';
import {strict as assert} from 'node:assert';
import vm from 'node:vm';

const html = readFileSync(new URL('../public/index.html', import.meta.url), 'utf8');
const data = JSON.parse(html.match(/<script id="trip-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
scripts.forEach(m => new vm.Script(m[1]));
assert.equal((html.match(/class="day-card"/g) || []).length, 10);
assert.equal((html.match(/class="day-map"/g) || []).length, 10);
assert(!/<input|type=["']checkbox/.test(html), 'No device-local todo checkboxes');
assert(!/<script[^>]+src=|<link[^>]+href=["']https?:|<img[^>]+src=["']https?:/.test(html), 'No external rendering dependencies');
assert(!/[A-Z0-9._%+-]+@(?:qq|163|126)\.com/i.test(html), 'Personal account email addresses are absent');
assert(!/(?:订单编号|预订编号|护照号码|入住码)\s*[:：]\s*[A-Z0-9]{4,}/i.test(html), 'Private booking and identity codes are absent');
for (const e of data.events) {
  assert(/T\d\d:\d\d:\d\d[+-]\d\d:\d\d$/.test(e.at), 'Every event has an explicit offset');
  const formatted = new Intl.DateTimeFormat('en-CA', {timeZone:e.tz, hour:'2-digit',minute:'2-digit',hour12:false}).format(new Date(e.at));
  const expected = e.at.slice(11,16).replace(/^00:/,'24:');
  assert.equal(formatted.replace(/^00:/,'24:'), expected, 'IANA timezone agrees with offset');
}
for(const m of html.matchAll(/href="(https:\/\/www\.google\.com\/maps\/dir\/\?[^"<>]+)"/g)){
  const u=new URL(m[1].replaceAll('&amp;','&'));
  assert.equal(u.searchParams.get('api'),'1');
  assert(u.searchParams.get('destination'));
  const stops=u.searchParams.get('waypoints');
  assert(!stops || stops.split('|').length<=3, 'Mobile compatible waypoint limit');
}
const flight = data.events.find(e => e.title === '伦敦起飞 → 青岛');
assert.equal(Date.parse(flight.at),Date.parse('2026-10-09T21:05:00Z'));
const landing=data.events.find(e=>e.title==='抵达伦敦卢顿');
assert.equal(Date.parse(landing.at),Date.parse('2026-10-08T06:35:00Z'));
console.log(`Passed: 10 days, ${data.events.length} timezone-qualified events, private-data exclusion, embedded assets, and mobile Maps links.`);
