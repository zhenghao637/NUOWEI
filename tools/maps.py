"""Offline SVG maps from real OSM/Natural Earth geometry, in Web Mercator.

The prepared vector paths are deliberately embedded once and reused by the maps.
No map server, tile download, geocoder or routing service runs in a visitor's browser.
"""
from pathlib import Path
import json,math,html

ASSETS=json.loads(Path(__file__).with_name('map_assets.json').read_text())
E=html.escape

def project(ident,lon,lat):
    a=ASSETS[ident];x=lon;y=math.degrees(math.log(math.tan(math.pi/4+math.radians(lat)/2)))
    return a['width']/2+(x-a['center'][0])*a['scale'],a['height']/2-(y-a['center'][1])*a['scale']

def definitions():
    symbols=[]
    for ident,a in ASSETS.items():
        l=a['layers'];s=f'<symbol id="geo-{ident}" viewBox="0 0 680 420"><rect width="680" height="420" fill="var(--geo-water)"/>'
        s+=f'<path d="{l["land"]}" fill="var(--geo-land)" stroke="var(--geo-coast)" stroke-width=".7" fill-rule="evenodd"/>'
        if l['water']:s+=f'<path d="{l["water"]}" fill="var(--geo-water)" fill-rule="evenodd"/>'
        if l['rivers']:s+=f'<path d="{l["rivers"]}" fill="none" stroke="var(--geo-water)" stroke-width="2"/>'
        for key,width in [('roads',.8),('major',1.5)]:
            if l[key]:s+=f'<path d="{l[key]}" fill="none" stroke="var(--geo-{key})" stroke-width="{width}" stroke-linejoin="round"/>'
        symbols.append(s+'</symbol>')
    return '<svg width="0" height="0" aria-hidden="true" style="position:absolute;overflow:hidden"><defs>'+''.join(symbols)+'</defs></svg>'

def line_path(ident,coords):
    return 'M'+'L'.join(f'{x:.2f},{y:.2f}' for x,y in [project(ident,*c) for c in coords])

def map_svg(ident,keys,places,nav,color,instance,*,routes=None,labels=None,title=None):
    a=ASSETS[ident];ruler=a['scaleBar'];labels=labels or {}
    s=f'<svg id="map-{instance}" class="route-svg geographic-map" data-map="{ident}" viewBox="0 0 680 420" role="img" aria-label="{E(title or "真实地理底图与地点位置")}"><title>{E(title or "真实地理底图与地点位置")}</title><defs><clipPath id="clip-{instance}"><rect width="680" height="420" rx="12"/></clipPath></defs><g clip-path="url(#clip-{instance})"><use href="#geo-{ident}" width="680" height="420"/>'
    for path,paint,kind in routes or []:
        s+=f'<path d="{path}" fill="none" stroke="var(--paper)" stroke-width="7" stroke-linejoin="round"/>'
    for path,paint,kind in routes or []:
        dash=' stroke-dasharray="7 5"' if kind=='connection' else ''
        width=5.5 if len(routes or [])==2 and path==routes[0][0] else 2.8
        s+=f'<path class="geo-route {kind}" d="{path}" fill="none" stroke="{paint}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"{dash}/>'
    # Keep labels separate from exact coordinate markers. Leader lines can move labels,
    # but the marker itself is never offset to improve the layout.
    placed=[]
    for i,key in enumerate(keys):
        p=places[key];x,y=project(ident,p['lng'],p['lat'])
        if not (0<=x<=680 and 0<=y<=420):raise ValueError(f'{ident}: {key} outside map')
        name,dx,dy=labels.get(key,('',0,0));paint=color.get(key,'#276761') if isinstance(color,dict) else color
        s+=f'<a href="{E(nav(key))}" target="_blank" rel="noopener noreferrer" aria-label="导航至{E(p["name"])}"><title>{E(p["name"])}</title>'
        if name:
            lx=x+dx;ly=y+dy
            s+=f'<path d="M{x:.2f},{y:.2f}L{lx:.2f},{ly-4:.2f}" stroke="{paint}" stroke-width=".8" fill="none"/><circle data-place="{key}" data-lat="{p["lat"]}" data-lng="{p["lng"]}" cx="{x:.2f}" cy="{y:.2f}" r="4.5" fill="{paint}" stroke="var(--paper)" stroke-width="1.5"/>'
            anchor='end' if dx<0 else 'start'
            s+=f'<text class="geo-label" x="{lx:.2f}" y="{ly:.2f}" text-anchor="{anchor}" fill="var(--ink)" font-size="14" font-weight="600">{E(name)}</text>'
        else:
            candidates=[(0,0),(22,-20),(-22,-20),(22,20),(-22,20),(0,-34),(0,34),(38,0),(-38,0),(42,-30),(-42,30)]
            lx,ly=x,y
            for dx,dy in candidates:
                xx,yy=x+dx,y+dy
                if 14<xx<666 and 58<yy<366 and all(math.hypot(xx-px,yy-py)>27 for px,py in placed):
                    lx,ly=xx,yy;break
            placed.append((lx,ly))
            if (lx,ly)!=(x,y):s+=f'<path d="M{x:.2f},{y:.2f}L{lx:.2f},{ly:.2f}" stroke="{paint}" stroke-width="1" fill="none"/>'
            s+=f'<circle data-place="{key}" data-lat="{p["lat"]}" data-lng="{p["lng"]}" cx="{x:.2f}" cy="{y:.2f}" r="3.5" fill="{paint}" stroke="var(--paper)" stroke-width="1"/><circle cx="{lx:.2f}" cy="{ly:.2f}" r="10" fill="{paint}" stroke="var(--paper)" stroke-width="2"/><text x="{lx:.2f}" y="{ly+4:.2f}" text-anchor="middle" fill="white" font-size="11" font-weight="700">{i+1}</text>'
        s+='</a>'
    km=ruler['km'];length=ruler['pixels'];unit=f'{km:g} km' if km>=1 else f'{km*1000:g} m'
    s+=f'<rect x="12" y="12" width="35" height="38" rx="5" fill="var(--paper)" fill-opacity=".92"/><text x="29" y="28" text-anchor="middle" fill="var(--ink)" font-size="11">N</text><path d="M29 32V44M25 36L29 32L33 36" stroke="var(--ink)" fill="none" stroke-width="1.6"/>'
    s+=f'<rect x="12" y="376" width="{length+24:.1f}" height="33" rx="5" fill="var(--paper)" fill-opacity=".92"/><path d="M24 391V397H{24+length:.1f}V391" stroke="var(--ink)" stroke-width="1.5" fill="none"/><text x="24" y="387" fill="var(--ink)" font-size="10">{unit}</text></g></svg>'
    s+=f'<button class="map-expand" type="button" data-map-expand="map-{instance}">放大查看地图 ↗</button>'
    s+='<p class="map-attribution">'+('地理数据 © <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener noreferrer">OpenStreetMap contributors</a> · ODbL' if a['source']=='OpenStreetMap' else '地理数据：<a href="https://www.naturalearthdata.com/" target="_blank" rel="noopener noreferrer">Natural Earth</a>')+' · 北向上 · 墨卡托投影 · 比例尺以图中心为准</p>'
    return s

def route_keys(keys,places,link,color):
    return '<div class="map-key">'+''.join(f'<span><i style="background:{color}">{i+1}</i>{link(k)}</span>' for i,k in enumerate(keys))+'</div>'
