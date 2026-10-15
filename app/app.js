'use strict';
const data=window.ARCHDIAGRAM_GALLERY;
const $=id=>document.getElementById(id);
const familyNames={vision:'Vision',text:'Language & sequences',audio:'Audio & speech',multimodal:'Multimodal & video',agents:'Agentic systems','robotics-graphs':'Robotics & graphs'};
let selected=0,zoom=1,visible=[];
function notify(message){$('toast').textContent=message;$('toast').classList.add('visible');setTimeout(()=>$('toast').classList.remove('visible'),2400)}
async function copy(text){try{await navigator.clipboard.writeText(text);notify('Copied to clipboard')}catch{const field=document.createElement('textarea');field.value=text;document.body.append(field);field.select();const copied=document.execCommand('copy');field.remove();notify(copied?'Copied to clipboard':'Clipboard unavailable. Select and copy manually.')}}
function updateZoom(){const img=$('figure');if(zoom===1){img.style.width='100%';img.style.height='100%';img.style.objectFit='contain';$('zoom-label').textContent='Fit'}else{img.style.width=(zoom*100)+'%';img.style.height='auto';img.style.objectFit='initial';$('zoom-label').textContent=Math.round(zoom*100)+'%'}}
function update(){
 const item=data.examples[selected];if(!item)return;
 const base='gallery/atlas/'+item.id;
 $('figure').src=item.svg||base+'.svg';$('figure').alt=item.title+'. '+item.description;
 $('figure-title').textContent=item.title;$('figure-description').textContent=item.description;
 $('counts').textContent=(familyNames[item.family]||item.family)+' / '+item.id;
 $('caption').textContent=item.caption;
 $('assumption-list').replaceChildren(...(item.assumptions||[]).map(text=>{const li=document.createElement('li');li.textContent=text;return li}));
 $('source-list').replaceChildren(...(item.sources||[]).map(source=>{const li=document.createElement('li');const a=document.createElement('a');a.href=typeof source==='string'?source:source.url;a.textContent=typeof source==='string'?source:(source.title||source.url);a.target='_blank';a.rel='noopener noreferrer';li.append(a);return li}));
 for(const kind of ['svg','tex','pdf','png'])$('download-'+kind).href=item[kind]||base+'.'+kind;
 document.querySelectorAll('#examples button').forEach((b,i)=>{b.setAttribute('aria-selected',String(i===selected));b.tabIndex=i===selected?0:-1});
 updateZoom()
}
function filter(){
 const q=$('figure-search').value.toLowerCase().trim(),family=$('family-filter').value;
 visible=[];document.querySelectorAll('#examples button').forEach((button,i)=>{const item=data.examples[i];const show=(!family||item.family===family)&&(!q||(item.title+' '+item.description+' '+item.id+' '+(item.tags||[]).join(' ')).toLowerCase().includes(q));button.hidden=!show;if(show)visible.push(i)});
 $('result-count').textContent=visible.length+' / '+data.examples.length;
 if(visible.length&&!visible.includes(selected)){selected=visible[0];zoom=1;update()}
}
if(!data||!data.examples.length){$('figure-title').textContent='Build the atlas to load its figures.'}else{
 for(const family of Object.keys(data.families||familyNames)){const o=document.createElement('option');o.value=family;o.textContent=familyNames[family]||family;$('family-filter').append(o)}
 data.examples.forEach((item,index)=>{const b=document.createElement('button');b.type='button';b.role='tab';b.setAttribute('aria-controls','canvas');const number=document.createElement('b');number.textContent=String(index+1).padStart(3,'0');const label=document.createElement('span');label.textContent=item.title;b.append(number,label);b.addEventListener('click',()=>{selected=index;zoom=1;update()});b.addEventListener('keydown',event=>{if(['ArrowRight','ArrowDown','ArrowLeft','ArrowUp','Home','End'].includes(event.key)){event.preventDefault();const current=visible.indexOf(selected),step=['ArrowRight','ArrowDown'].includes(event.key)?1:-1;selected=event.key==='Home'?visible[0]:event.key==='End'?visible[visible.length-1]:visible[(current+step+visible.length)%visible.length];zoom=1;update();$('examples').children[selected].focus()}});$('examples').append(b)});filter();update()
}
$('figure-search').addEventListener('input',filter);$('family-filter').addEventListener('change',filter);
$('zoom-in').addEventListener('click',()=>{zoom=Math.min(4,zoom+.25);updateZoom()});
$('zoom-out').addEventListener('click',()=>{zoom=Math.max(1,zoom-.25);updateZoom()});
$('zoom-reset').addEventListener('click',()=>{zoom=1;updateZoom()});
$('copy-install').addEventListener('click',()=>copy('git clone https://github.com/Hisernberg/archdiagram-studio.git\ncd archdiagram-studio\npython scripts/install_skill.py --agent codex'));
$('copy-prompt').addEventListener('click',()=>{const brief=$('brief').value.trim();if(!brief){notify('Describe your architecture first.');$('brief').focus();return}copy('Use $draw-architecture to create an original black-and-white architecture diagram.\n\nArchitecture: '+brief+'\nAudience: '+$('audience').value+'.\nDeliverables: '+$('format').value+'.\n\nFind a suitable starting point in the 100-figure TikZ atlas. Use real LaTeX typography, thin rules, sparse gray fills, and meaningful mathematical or structural annotations. Adapt the architecture from my supplied evidence, not from a template alone. Record assumptions and unknown dimensions. Keep data, control, residual, and feedback paths explicit. Compile, inspect the figure at its intended size, fix collisions, and return the editable master, preview, caption, and checks actually performed.')});
