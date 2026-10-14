from PIL import Image
import numpy as np
logo=np.array(Image.open('logo2/logo_lines.png').convert('RGBA'))
solid=logo[:,:,3]>10; reg=np.zeros_like(solid); reg[150,700]=True
while True:
    d=reg.copy(); d[1:]|=reg[:-1]; d[:-1]|=reg[1:]; d[:,1:]|=reg[:,:-1]; d[:,:-1]|=reg[:,1:]; d&=solid
    if d.sum()==reg.sum(): break
    reg=d
for _ in range(3):
    d=reg.copy(); d[1:]|=reg[:-1]; d[:-1]|=reg[1:]; d[:,1:]|=reg[:,:-1]; d[:,:-1]|=reg[:,1:]; reg=d
logo[reg,3]=0; logo[214:,824:,3]=0
edge=(logo[:,:,3]<230)&(logo[:,:,3]>0); logo[edge,0:3]=(26,25,31)
base=Image.fromarray(logo)
em=Image.open('cal/emblem_neat_8x.png'); em1=em.resize((round(em.width/8),round(em.height/8)),Image.LANCZOS)
for tagf,out,bgc in [('logo2/tag_dark.png','logo2/logo_neat.png',(255,255,255,255)),('logo2/tag_white.png','logo2/logo_neat_navy.png',(38,34,32,255))]:
    b=base.copy(); b.alpha_composite(em1,(532,0))
    t=Image.open(tagf).resize((885,60),Image.LANCZOS); b.alpha_composite(t,(1715-885,228))
    b=b.crop(b.getbbox()); b.save(out)
    bg=Image.new('RGBA',b.size,bgc); bg.alpha_composite(b); bg.convert('RGB').save(out.replace('.png','_chk.png'))
print('logo ok')
