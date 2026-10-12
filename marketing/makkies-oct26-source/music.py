import numpy as np, wave
SR=44100; DUR=15.0; BPM=120; B=60/BPM
N=int(SR*DUR); mix=np.zeros(N); rng=np.random.default_rng(7)
def add(sig,t,g=1.0):
    i=int(t*SR); j=min(N,i+len(sig))
    if i<N: mix[i:j]+=g*sig[:j-i]
def env(n,a=0.002,d=0.2):
    t=np.arange(n)/SR; return np.minimum(t/a,1)*np.exp(-t/d)
def kick():
    n=int(.35*SR);t=np.arange(n)/SR; f=45+110*np.exp(-t*30)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*env(n,.001,.12)
def clap():
    n=int(.25*SR); s=rng.standard_normal(n)
    e=np.zeros(n)
    for o in (0,.011,.022): k=int(o*SR); e[k:]+=env(n-k,.0005,.05 if o<.02 else .12)
    s=np.diff(np.concatenate([[0],s]))  # brighten
    return s*e*0.5
def hat(open_=False):
    n=int((.18 if open_ else .05)*SR); s=rng.standard_normal(n); s=np.diff(np.concatenate([[0],s]))
    return s*env(n,.0005,.06 if open_ else .012)*0.25
def logdrum(freq,l=.45):
    n=int(l*SR);t=np.arange(n)/SR; f=freq*(1+0.6*np.exp(-t*40))
    s=np.sin(2*np.pi*np.cumsum(f)/SR)+0.3*np.sin(4*np.pi*np.cumsum(f)/SR)
    return np.tanh(2.2*s*env(n,.002,.22))*0.55
def pluck(freq,l=.5):
    n=int(l*SR);t=np.arange(n)/SR
    s=sum(np.sin(2*np.pi*freq*h*t)/h for h in (1,2,3,4))
    return s*env(n,.003,.18)*0.12
def pad(freqs,l):
    n=int(l*SR);t=np.arange(n)/SR
    s=sum(np.sin(2*np.pi*f*t)+0.5*np.sin(2*np.pi*f*1.003*t) for f in freqs)
    a=np.minimum(t/.3,1)*np.minimum((l-t)/.3,1)
    return s*a*0.035
# A minor-ish: Am F C G progression, 2 beats each? use 4 beats (2s) per chord
nf=lambda m: 440*2**((m-69)/12)
chords=[[57,60,64],[53,57,60],[48,52,55],[55,59,62]]
bassroot=[45,41,48,43]
for bar in range(8):
    t0=bar*4*B; ch=chords[bar%4]; r=bassroot[bar%4]
    if t0>=DUR: break
    add(pad([nf(m) for m in ch],4*B),t0)
    for beat in range(4):
        tb=t0+beat*B
        if tb>=DUR: break
        intro = tb<2.0
        add(kick(),tb,0.9 if not intro else 0.6)
        if beat in (1,3): add(clap(),tb,0.8)
        for s in range(4):
            add(hat(s==2),tb+s*B/4, 0.9 if s%2 else 0.5)
    # log drum syncopation (amapiano style)
    for off,semi in [(0.75,0),(1.5,0),(2.25,7),(3.0,0),(3.5,12)]:
        if t0+off*B<DUR and t0>=1.5: add(logdrum(nf(r+12+semi-12)), t0+off*B)
    # plucks melody
    mel=[ch[2]+12,ch[1]+12,ch[0]+12,ch[1]+12]
    for k,m in enumerate(mel):
        tt=t0+(k*1+0.5)*B
        if tt<DUR and t0>=2.0: add(pluck(nf(m)),tt)
# impacts / whooshes
def impact():
    n=int(1.2*SR);t=np.arange(n)/SR
    s=np.sin(2*np.pi*np.cumsum(38+80*np.exp(-t*12))/SR)*env(n,.001,.4)
    return s+rng.standard_normal(n)*env(n,.001,.08)*0.4
def riser(l):
    n=int(l*SR);t=np.arange(n)/SR; s=rng.standard_normal(n)
    # crude band sweep via moving average shrinking
    out=np.zeros(n); w=np.linspace(40,2,n).astype(int); c=np.cumsum(s)
    idx=np.arange(n); lo=np.maximum(idx-w,0); out=(c[idx]-c[lo])/w
    return out*(t/l)**2*0.6
def whoosh():
    n=int(.35*SR); s=rng.standard_normal(n); c=np.cumsum(s); w=12
    o=np.concatenate([np.zeros(w),(c[w:]-c[:-w])/w]); t=np.arange(n)/SR
    return o*np.sin(np.pi*t/.35)**2*0.5
add(impact(),0.12,0.9)
for t in (2.0,3.0,4.0,5.0,6.0,12.0): add(whoosh(),t-0.12,0.7)
add(riser(1.0),7.0,0.8); add(impact(),8.0,0.8)
add(impact(),9.9,0.5)
# master
mix=np.tanh(mix*1.1); mix/=np.max(np.abs(mix))*1.08
fade=np.ones(N); fl=int(.6*SR); fade[-fl:]=np.linspace(1,0,fl); mix*=fade
st=np.stack([mix,mix],1)
with wave.open(f'{__import__("os").path.dirname(__file__)}/music.wav','wb') as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((st*32767).astype(np.int16).tobytes())
print('ok')
