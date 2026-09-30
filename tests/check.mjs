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
const maps=JSON.parse(readFileSync(new URL('../tools/map_assets.json',import.meta.url),'utf8'));
for(const svg of html.matchAll(/<svg[^>]+data-map="([^"]+)"[^>]*>([\s\S]*?)<\/svg>/g)){
  const map=maps[svg[1]];
  assert(map&&map.layers.land.length>30, 'Each map has a geographic base');
  for(const point of svg[2].matchAll(/data-place="([^"]+)" data-lat="([^"]+)" data-lng="([^"]+)" cx="([^"]+)" cy="([^"]+)"/g)){
    const p=data.places[point[1]],lat=Number(point[2]),lon=Number(point[3]);
    assert.equal(lat,p.lat);assert.equal(lon,p.lng);
    const x=340+(lon-map.center[0])*map.scale;
    const y=210-(Math.log(Math.tan(Math.PI/4+lat*Math.PI/360))*180/Math.PI-map.center[1])*map.scale;
    assert(Math.abs(Number(point[4])-x)<.02&&Math.abs(Number(point[5])-y)<.02,'Location markers match the base projection');
    assert(x>=0&&x<=680&&y>=0&&y<=420,'Location stays within map bounds');
  }
}
assert.equal(data.places.devil.lng,14.5979795,'Djevelporten is at its verified OSM position');
assert(maps.lofoten.layers.routes['4'].length>1000&&maps.lofoten.layers.routes['5'].length>1000,'Driving routes retain road geometry');
assert(html.includes('OpenStreetMap contributors')&&html.includes('Natural Earth'),'Map source attribution is visible');
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
