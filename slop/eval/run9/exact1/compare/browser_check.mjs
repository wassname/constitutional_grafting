// Browser checks for the recorded-reply viewer; no inference. -- PI/Sol
import fs from 'node:fs';
const target=(await (await fetch('http://127.0.0.1:9223/json/list')).json())[0];
const ws=new WebSocket(target.webSocketDebuggerUrl);
await new Promise((resolve,reject)=>{ws.onopen=resolve;ws.onerror=reject});
let id=0;const callbacks=new Map(),events=new Map();
ws.onmessage=event=>{const msg=JSON.parse(event.data);if(msg.id){const c=callbacks.get(msg.id);callbacks.delete(msg.id);msg.error?c.reject(msg.error):c.resolve(msg.result)}else if(events.has(msg.method)){events.get(msg.method)(msg.params);events.delete(msg.method)}};
function send(method,params={}){return new Promise((resolve,reject)=>{const n=++id;callbacks.set(n,{resolve,reject});ws.send(JSON.stringify({id:n,method,params}))})}
async function evaluate(expression){const r=await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value}
const deadline=setTimeout(()=>{throw Error('browser verification exceeded30seconds')},30000);
await send('Page.enable');
await send('Emulation.setDeviceMetricsOverride',{width:1600,height:1000,deviceScaleFactor:1,mobile:false});
const loaded=new Promise(resolve=>events.set('Page.loadEventFired',resolve));
await send('Page.navigate',{url:'http://127.0.0.1:8081/demo_compare.html'});await loaded;
const check=await evaluate(`(()=>{let cases=0;for(const q of DATA.questions){select.value=q.id;draw();if(document.querySelectorAll('#rows tr').length!==23)throw Error(q.id+' missing model');if(document.querySelector('#prompt').textContent!==q.prompt)throw Error('wrong prompt');for(const r of q.rows.filter(r=>!r.missing)){for(const f of Object.values(r.fragments))if(Array.from(r.reply).slice(f.start,f.end).join('')!==f.text)throw Error('nonverbatim excerpt')}cases++}select.value='panel_escaped_starwisp_t3';draw();const b=[...document.querySelectorAll('#rows button')].find(b=>b.title.includes('(r9e_stoic8)'));b.click();if(!dialog.open||!dialog.textContent.includes('Merge or Die'))throw Error('full reply inaccessible');dialog.close();return{questions:cases,models:23,all_quote_spans_exact:true,question_navigation:true,full_reply_opens:true,visible_rows:document.querySelectorAll('#rows tr').length,table_height:document.querySelector('.scroll').clientHeight,table_content_height:document.querySelector('table').clientHeight}})()`);
let screenshot=await send('Page.captureScreenshot',{format:'png'});fs.writeFileSync('slop/eval/run9/exact1/compare/viewer_desktop.png',Buffer.from(screenshot.data,'base64'));
await send('Emulation.setDeviceMetricsOverride',{width:1280,height:800,deviceScaleFactor:1,mobile:false});
screenshot=await send('Page.captureScreenshot',{format:'png'});fs.writeFileSync('slop/eval/run9/exact1/compare/viewer_laptop.png',Buffer.from(screenshot.data,'base64'));
check.laptop=await evaluate(`({viewport:innerHeight,table_height:document.querySelector('.scroll').clientHeight,table_content_height:document.querySelector('table').clientHeight})`);
fs.writeFileSync('slop/eval/run9/exact1/compare/browser_verification.json',JSON.stringify({author:'PI/Sol',...check},null,2)+'\n');console.log(check);clearTimeout(deadline);ws.close();
