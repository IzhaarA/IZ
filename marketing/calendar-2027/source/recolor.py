"""Fill the MW letters inside the 2026 banner circle with the new logo's colours."""
import numpy as np
from PIL import Image, ImageDraw
x0,y0=690,35
lab=np.load('lab.npy')
ban=np.asarray(Image.open('assets/banner.png')).copy()
H,W=lab.shape
def dil(m,k=2):
    o=m.copy()
    for dy in range(-k,k+1):
        for dx in range(-k,k+1):
            o|=np.roll(np.roll(m,dy,0),dx,1)
    return o
letters=dil(lab==2,2) & ~dil((lab==1)|(lab==3),2)
yy,xx=np.mgrid[0:H,0:W]; X=xx+x0; Y=yy+y0
isM=letters&(X<843)&(Y<212); isW=letters&~isM
# M stripes, sampled from the new logo's M (plum,yellow,blue,red,green,red,blue,yellow,plum)
logo=np.asarray(Image.open('assets/logo_new.png').convert('RGB')).astype(float)
col=logo[22:338,55]
my0,my1=Y[isM].min(),Y[isM].max()
def mcolor(y): return col[int((y-my0)/(my1-my0+1)*len(col))]
# W pattern: red with dashed lines and pot motifs
wx0,wx1,wy0,wy1=X[isW].min(),X[isW].max(),Y[isW].min(),Y[isW].max()
tex=Image.new('RGB',(wx1-wx0+1,wy1-wy0+1),(237,25,27)); d=ImageDraw.Draw(tex)
P=21; K=(26,18,16)
for r,ty in enumerate(range(-4,tex.height,P)):
    for dx in range(0,tex.width,8): d.rectangle((dx,ty,dx+4,ty+2),fill=K)
    off=0 if r%2==0 else 9
    for mx in range(-9+off,tex.width,18):
        d.rectangle((mx+3,ty+5,mx+6,ty+7),fill=K)
        d.rounded_rectangle((mx,ty+8,mx+9,ty+17),radius=2,fill=K)
tex=np.asarray(tex).astype(float)
out=ban.astype(float)
src=np.asarray(Image.open('x/im-001.png').convert('RGB')).astype(float)
for (yy_,xx_) in zip(*np.where(letters)):
    gx,gy=xx_+x0,yy_+y0
    wgt=np.clip((src[gy,gx].min()-40)/(230-40),0,1)
    if wgt<=0: continue
    fill=mcolor(gy) if isM[yy_,xx_] else tex[gy-wy0,gx-wx0]
    out[gy,gx,:3]=wgt*fill+(1-wgt)*out[gy,gx,:3]
# white outline around each letter (and between M and W) so they stand off the black circle
core=np.zeros((H,W),bool)
for (yy_,xx_) in zip(*np.where(letters)):
    core[yy_,xx_]=src[yy_+y0,xx_+x0].min()>120
coreM=core&isM; coreW=core&isW
seam=(dil(coreM,2)&coreW)|(dil(coreW,2)&coreM)
ring=(lab==1)|(lab==3)
outline=((dil(coreM,3)|dil(coreW,3))&~core&~dil(ring,1))|seam
for (yy_,xx_) in zip(*np.where(outline)):
    out[yy_+y0,xx_+x0,:3]=(255,255,255)
# soften: one-pixel halo at 50% for anti-aliasing
halo=(dil(outline,1)&~outline&~core&~dil(ring,1))
for (yy_,xx_) in zip(*np.where(halo)):
    out[yy_+y0,xx_+x0,:3]=0.5*out[yy_+y0,xx_+x0,:3]+0.5*255
Image.fromarray(out.astype(np.uint8),'RGBA').save('assets/banner_colour.png')
bg=Image.new('RGBA',ban.shape[1::-1],(192,145,30,255)); bg.alpha_composite(Image.open('assets/banner_colour.png'))
bg.convert('RGB').crop((650,20,1050,330)).resize((800,620)).save('circle_test.jpg')
