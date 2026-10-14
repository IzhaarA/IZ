import numpy as np
from PIL import Image, ImageDraw, ImageFilter
S=8; PAD=10; x0,y0=690-PAD,35
lab=np.pad(np.load('lab.npy'),((0,0),(PAD,0))); H,W=lab.shape
src=np.asarray(Image.open('x/im-001.png').convert('RGB')).astype(float)[y0:y0+H,x0:x0+W]
ban=np.asarray(Image.open('assets/banner.png').convert('RGBA'))[y0:y0+H,x0:x0+W]
wgt=np.clip((src.min(2)-40)/(230-40),0,1)          # how "white" each pixel is in the original
def dil(m,k):
    o=m.copy()
    for dy in range(-k,k+1):
        for dx in range(-k,k+1): o|=np.roll(np.roll(m,dy,0),dx,1)
    return o
def smooth(soft):     # soft 0..1 mask at 1x -> smooth binary mask at Sx
    im=Image.fromarray((soft*255).astype(np.uint8),'L').resize((W*S,H*S),Image.BICUBIC).filter(ImageFilter.GaussianBlur(S*0.7))
    return np.asarray(im)>127
letters=dil(lab==2,2)&~dil((lab==1)|(lab==3),2)
L=smooth(wgt*letters); T=smooth(wgt*(dil(lab==1,1)&~letters)); B=smooth(wgt*(dil(lab==3,1)&~letters))
yy,xx=np.mgrid[0:H*S,0:W*S]; X=xx/S+x0; Y=yy/S+y0
isM=L&(X<843)&(Y<212); isW=L&~isM
# oval: perfect ellipse fitted to the original black circle
ex0,ex1,ey0,ey1=687-x0,981-x0,44-y0,299-y0
print('oval bbox',ex0,ex1,ey0,ey1)
out=Image.new('RGBA',(W*S,H*S),(0,0,0,0)); d=ImageDraw.Draw(out)
d.ellipse((ex0*S,ey0*S,ex1*S-1,ey1*S-1),fill=(27,24,29,255))
o=np.asarray(out).copy()
# colours
logo=np.asarray(Image.open('assets/logo_new.png').convert('RGB')).astype(float)
col=logo[22:338,55]
def stripes(mask,y_from,y_to,c):
    idx=np.clip(((Y-y_from)/(y_to-y_from)*len(c)).astype(int),0,len(c)-1)
    return c[idx]
my0,my1=Y[isM].min(),Y[isM].max()
Mfill=stripes(isM,my0,my1+1/S,col)
bright=col[37:276]
ty0,ty1=Y[T].min(),Y[T].max()
Tfill=stripes(T,ty0,ty1+1/S,bright)
# W pattern at Sx
wx0,wy0=int(X[isW].min()),int(Y[isW].min())
tw,th=int(X[isW].max()-wx0+2)*S,int(Y[isW].max()-wy0+2)*S
tex=Image.new('RGB',(tw,th),(237,25,27)); td=ImageDraw.Draw(tex); P=21*S; K=(26,18,16)
for r,ty in enumerate(range(-4*S,th,P)):
    for dx in range(0,tw,8*S): td.rectangle((dx,ty,dx+4*S,ty+2*S),fill=K)
    off=0 if r%2==0 else 9*S
    for mx in range(-9*S+off,tw,18*S):
        td.rectangle((mx+3*S,ty+5*S,mx+6*S,ty+7*S),fill=K)
        td.rounded_rectangle((mx,ty+8*S,mx+9*S,ty+17*S),radius=2*S,fill=K)
tex=np.asarray(tex).astype(float)
Wfill=tex[np.clip(((Y-wy0)*S).astype(int),0,th-1),np.clip(((X-wx0)*S).astype(int),0,tw-1)]
# bottom ring: red with black dashes by angle (same as before)
cx,cy=841,172
ang=(np.degrees(np.arctan2(Y-cy,X-cx))+360)%360
Bfill=np.where(((ang%7)<2.4)[...,None]&((X>725)&(X<950))[...,None],np.array([26,18,16.]),np.array([237,25,27.]))
# white outline around the letters + seam between M and W
def dilS(m,r):
    im=Image.fromarray((m*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(2*r+1)); return np.asarray(im)>127
ring=T|B
outline=dilS(L,int(1.3*S)|1)&~L&~dilS(ring,S//2|1)
seamW=dilS(isM,int(0.9*S)|1)&isW
o=o.astype(float)
for m,f in ((T,Tfill),(B,Bfill)): o[m,:3]=f[m]; o[m,3]=255
o[outline,:3]=255; o[outline,3]=255
o[isW,:3]=Wfill[isW]; o[isM,:3]=Mfill[isM]
o[seamW,:3]=255
o[L,3]=255
im=Image.fromarray(o.astype(np.uint8),'RGBA').crop((ex0*S-2,ey0*S-2,ex1*S+2,ey1*S+2))
im.save('emblem_neat_8x.png'); print(im.size)
bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im)
bg.convert('RGB').resize((im.width//4,im.height//4),Image.LANCZOS).save('emblem_neat_chk.png')
