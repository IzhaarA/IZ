"""Cut the oval bead necklaces out of their grey photo card onto white (for trio-beads). Usage: python3 cut_necklaces.py PBN-04 PBN-E23 ... (needs rembg)
Edit PUB to the deploy folder's public."""
import sys,os,json,re
from rembg import remove, new_session
from PIL import Image
PUB='/tmp/claude-0/-home-user-IZ/2fe381b0-b6e5-5442-ac73-431a50475247/scratchpad/deploy/public'
O='/home/user/IZ/marketing/category-ads-source/img/'
s=open(PUB+'/index.html',encoding='utf-8').read()
sess=new_session('isnet-general-use')
for pid in sys.argv[1:]:
    m=re.search(r'"id":"%s","name":"[^"]*".*?"img":"(images/[^"]+)"'%re.escape(pid),s)
    im=Image.open(PUB+'/'+m.group(1)).convert('RGB')
    cut=remove(im,session=sess)
    bg=Image.new('RGB',cut.size,'white'); bg.paste(cut,mask=cut.split()[3])
    bg.save(O+'t_n_'+pid.lower()+'_c.jpg',quality=92); print(pid,flush=True)
