import math
# One fused pendant. Reference artwork; XY front and flat back at z=0.
w = param('pendant_width', 50.0)
h = param('pendant_body_height', 28.0)
t = param('pendant_base_thickness', 3.0)
cr = param('pendant_corner_radius', 4.0)
lug_d = param('pendant_lug_diameter', 8.0)
lug_x = param('pendant_lug_x', 0.0)
lug_y = param('pendant_lug_y', 16.0)
hole_d = param('pendant_hole_diameter', 4.0)
rel = param('pendant_relief_height', 0.8)
platform = param('pendant_platform_height', 0.4)
# Per-motif dimensions and independent centers.
ux = param('pendant_ultra_x', -6.0)
uy = param('pendant_ultra_y', 9.0)
us = param('pendant_ultra_font_size', 5.0)
sx = param('pendant_subtitle_x', -4.0)
sy = param('pendant_subtitle_y', 4.5)
ss = param('pendant_subtitle_font_size', 3.2)
lx = param('pendant_lightning_x', -19.0)
ly = param('pendant_lightning_y', 7.5)
ls = param('pendant_lightning_height', 7.0)
rx = param('pendant_refresh_x', 19.0)
ry = param('pendant_refresh_y', 8.0)
rr = param('pendant_refresh_radius', 2.5)
rs = param('pendant_refresh_stroke', 0.6)
vx = param('pendant_slider_x', 0.0)
vy = param('pendant_slider_y', -1.0)
vw = param('pendant_slider_width', 43.0)
vh = param('pendant_slider_height', 4.0)
vd = param('pendant_slider_recess_depth', 0.4)
kd = param('pendant_knob_diameter', 4.0)
koff = param('pendant_knob_offset', 18.0)
ex = param('pendant_effort_x', -8.0)
ey = param('pendant_effort_y', -9.0)
ew = param('pendant_effort_width', 28.0)
eh = param('pendant_effort_height', 6.0)
es = param('pendant_effort_font_size', 2.8)
mx = param('pendant_microphone_x', 10.0)
my = param('pendant_microphone_y', -9.0)
mh = param('pendant_microphone_height', 5.0)
ms = param('pendant_microphone_stroke', 0.55)
wx = param('pendant_wave_x', 18.8)
wy = param('pendant_wave_y', -9.0)
wd = param('pendant_wave_disk_diameter', 6.4)
wh = param('pendant_wave_height', 4.0)
ws = param('pendant_wave_bar_width', 0.55)
wp = param('pendant_wave_bar_pitch', 0.85)
assert 0 < platform < rel and lug_d > hole_d and lug_y-lug_d/2 < h/2
assert 0 < vd < t, 'Recess must leave a solid floor'
EPS = 0.04  # Boolean overlap only.
base_outline = RectangleRounded(w,h,cr) + Pos(lug_x,lug_y)*Circle(lug_d/2)
base_outline = base_outline - Pos(lug_x,lug_y)*Circle(hole_d/2)
body = extrude(base_outline,amount=t,dir=(0,0,1))

def raised(sketch,z,height):
    solid=Pos(0,0,z-EPS)*extrude(sketch,amount=height+EPS,dir=(0,0,1))
    assert abs(solid.bounding_box().max.Z-(z+height)) < 1e-5
    return solid

def stroke(a,b,width):
    dx,dy=b[0]-a[0],b[1]-a[1]
    return Pos((a[0]+b[0])/2,(a[1]+b[1])/2)*SlotOverall(math.hypot(dx,dy)+width,width,rotation=math.degrees(math.atan2(dy,dx)))

def text_shape(txt,size,x,y):
    return Pos(x,y)*Text(txt,size,font='Arial',font_style=FontStyle.BOLD,align=(Align.CENTER,Align.CENTER))

ultra=text_shape('Ultra',us,ux,uy)
subtitle=text_shape('GPT-6 Astra',ss,sx,sy)
assert subtitle.bounding_box().size.X < w*0.60
body=body+raised(ultra,t,rel)+raised(subtitle,t,rel)
u_end=ultra.bounding_box().max.X
q=us*0.26
chevron=stroke((u_end+q,uy+q),(u_end+2*q,uy),us*0.12)+stroke((u_end+2*q,uy),(u_end+q,uy-q),us*0.12)
body=body+raised(chevron,t,rel)
# Normalized reference silhouette; dimensions follow ls.
light_points=[(0.10,0.50),(-0.33,-0.06),(-0.06,-0.06),(-0.19,-0.50),(0.34,0.14),(0.04,0.14)]
light=Pos(lx,ly)*Polygon(*[(a*ls,b*ls) for a,b in light_points],align=None)
body=body+raised(light,t,rel)
# Counterclockwise arrowhead faces and explicit +Z extrusion avoid hidden tips.
for phase in (0,180):
    arc=SlotArc(CenterArc((0,0),rr,25+phase,130),rs)
    angle=math.radians(155+phase)
    px,py=rr*math.cos(angle),rr*math.sin(angle)
    tx,ty=-math.sin(angle),math.cos(angle)
    nx,ny=math.cos(angle),math.sin(angle)
    ah=rr*0.62
    tip=(px+tx*ah*0.35,py+ty*ah*0.35)
    inner=(px-tx*ah*0.6-nx*ah*0.5,py-ty*ah*0.6-ny*ah*0.5)
    outer=(px-tx*ah*0.6+nx*ah*0.5,py-ty*ah*0.6+ny*ah*0.5)
    head=Polygon(tip,inner,outer,align=None)
    body=body+raised(Pos(rx,ry)*arc,t,rel)+raised(Pos(rx,ry)*head,t,rel)
# User mark #1: recessed capsule, same circular knob XY footprint and top Z.
slider=Pos(vx,vy)*SlotOverall(vw,vh)
knob=Pos(vx+koff,vy)*Circle(kd/2)
assert abs(koff)+kd/2 <= vw/2 and kd <= vh
slot_cut=Pos(0,0,t-vd)*extrude(slider,amount=vd+EPS,dir=(0,0,1))
body=body-slot_cut
# Extend only the supporting circular material down to the new floor.
knob_solid=raised(knob,t-vd,rel+vd)
body=body+knob_solid
assert abs(knob_solid.bounding_box().max.Z-(t+rel))<1e-5
assert abs(knob_solid.bounding_box().size.X-kd)<1e-5
print('Slot floor Z:',t-vd,'Recess depth:',vd,'Knob diameter:',kd,'Knob top Z:',t+rel)
effort=Pos(ex,ey)*SlotOverall(ew,eh)
effort_text=text_shape('Select effort',es,ex-ew*0.08,ey)
assert effort_text.bounding_box().size.X < ew*0.78
body=body+raised(effort,t,platform)+raised(effort_text,t+platform,rel-platform)
cx=ex+ew*0.36
cq=eh*0.16
chevron_down=stroke((cx-cq,ey+cq*0.45),(cx,ey-cq*0.55),eh*0.085)+stroke((cx,ey-cq*0.55),(cx+cq,ey+cq*0.45),eh*0.085)
body=body+raised(chevron_down,t+platform,rel-platform)
scale_m=mh/5.0
cap=Pos(0,0.55*scale_m)*SlotOverall(2.8*scale_m,1.25*scale_m,rotation=90)
cradle=SlotArc(CenterArc((0,-0.2*scale_m),1.35*scale_m,180,180),ms)
cradle=cradle+stroke((-1.35*scale_m,-0.2*scale_m),(-1.35*scale_m,0.65*scale_m),ms)+stroke((1.35*scale_m,-0.2*scale_m),(1.35*scale_m,0.65*scale_m),ms)
stand=stroke((0,-1.55*scale_m),(0,-2.5*scale_m),ms)+stroke((-0.95*scale_m,-2.5*scale_m),(0.95*scale_m,-2.5*scale_m),ms)
body=body+raised(Pos(mx,my)*(cap+cradle+stand),t,rel)
disk=Pos(wx,wy)*Circle(wd/2)
body=body+raised(disk,t,platform)
for index,ratio in enumerate((0.375,0.7,1.0,0.7,0.375)):
    bar=Pos(wx+(index-2)*wp,wy)*SlotOverall(wh*ratio,ws,rotation=90)
    body=body+raised(bar,t+platform,rel-platform)
body=body.clean()
assert len(body.solids())==1,'Every relief must join the single base solid'
assert body.is_valid,'Invalid pendant geometry'
bb=body.bounding_box()
assert abs(bb.size.X-w)<1e-5 and abs(bb.size.Z-t-rel)<1e-5
assert abs(bb.min.Z)<1e-5
print('Pendant bbox mm:',bb.size.X,bb.size.Y,bb.size.Z)
print('Solid count:',len(body.solids()),'Lug radial ligament mm:',(lug_d-hole_d)/2)
print('Relief planes mm:',t,t+platform,t+rel)
publish('pendant',body,'浮雕吊牌')